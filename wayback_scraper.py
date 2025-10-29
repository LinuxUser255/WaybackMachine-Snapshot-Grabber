#!/usr/bin/env python3
"""
Wayback Machine Snapshot Scraper
Scrapes ALL available snapshots of a website
from the Internet Archive's Wayback Machine.
"""

import requests
import time
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class WaybackScraper:
    """Scraper for Wayback Machine snapshots."""

    CDX_API = "https://web.archive.org/cdx/search/cdx"
    WAYBACK_URL = "https://web.archive.org/web/{timestamp}/{url}"

    def __init__(self, url: str, output_dir: str = "snapshots", delay: float = 1.0):
        """
        Initialize the scraper.

        Args:
            url: The URL to scrape snapshots for
            output_dir: Directory to save snapshots
            delay: Delay between requests in seconds (be respectful!)
        """
        self.url = url
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_snapshots(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Retrieve ALL available snapshots for the URL.

        Args:
            limit: Maximum number of snapshots to retrieve

        Returns:
            List of snapshot metadata dictionaries
        """
        print(f"Fetching snapshot list for: {self.url}")

        params = {
            'url': self.url,
            'output': 'json',
            'collapse': 'timestamp:8',  # One per day
            'filter': 'statuscode:200',  # Only successful captures
        }

        if limit:
            params['limit'] = limit

        try:
            response = requests.get(self.CDX_API, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # First row is headers
            if len(data) < 2:
                print("No snapshots found!")
                return []

            headers = data[0]
            snapshots = []

            for row in data[1:]:
                snapshot = dict(zip(headers, row))
                snapshots.append(snapshot)

            print(f"Found {len(snapshots)} snapshots")
            return snapshots

        except requests.RequestException as e:
            print(f"Error fetching snapshots: {e}")
            return []

    def download_snapshot(self, timestamp: str, original_url: str) -> Optional[str]:
        """
        Download a single snapshot.

        Args:
            timestamp: Wayback timestamp (YYYYMMDDhhmmss)
            original_url: Original URL that was captured

        Returns:
            Path to saved file or None if failed
        """
        wayback_url = self.WAYBACK_URL.format(timestamp=timestamp, url=original_url)

        # Create filename from timestamp
        dt = datetime.strptime(timestamp[:14], '%Y%m%d%H%M%S')
        filename = f"{dt.strftime('%Y-%m-%d_%H-%M-%S')}.html"
        filepath = self.output_dir / filename

        try:
            print(f"Downloading snapshot from {dt.strftime('%Y-%m-%d %H:%M:%S')}...", end=" ")
            response = requests.get(wayback_url, timeout=30)
            response.raise_for_status()

            # Save the content
            with open(filepath, 'wb') as f:
                f.write(response.content)

            print(f"✓ Saved to {filepath}")
            return str(filepath)

        except requests.RequestException as e:
            print(f"✗ Failed: {e}")
            return None

    def scrape_all(self, limit: Optional[int] = None, save_metadata: bool = True):
        """
        Scrape all snapshots for the URL.

        Args:
            limit: Maximum number of snapshots to download
            save_metadata: Whether to save metadata JSON file
        """
        snapshots = self.get_snapshots(limit)

        if not snapshots:
            print("No snapshots to download.")
            return

        # Save metadata
        if save_metadata:
            metadata_file = self.output_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump({
                    'url': self.url,
                    'total_snapshots': len(snapshots),
                    'scraped_at': datetime.now().isoformat(),
                    'snapshots': snapshots
                }, f, indent=2)
            print(f"Metadata saved to {metadata_file}\n")

        # Download each snapshot
        successful = 0
        failed = 0

        for i, snapshot in enumerate(snapshots, 1):
            print(f"[{i}/{len(snapshots)}] ", end="")

            result = self.download_snapshot(
                snapshot['timestamp'],
                snapshot['original']
            )

            if result:
                successful += 1
            else:
                failed += 1

            # Be respectful - add delay between requests
            if i < len(snapshots):
                time.sleep(self.delay)

        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Snapshots saved to: {self.output_dir.absolute()}")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape all Wayback Machine snapshots for a URL'
    )
    parser.add_argument(
        'url',
        help='URL to scrape snapshots for'
    )
    parser.add_argument(
        '-o', '--output',
        default='snapshots',
        help='Output directory (default: snapshots)'
    )
    parser.add_argument(
        '-l', '--limit',
        type=int,
        help='Limit number of snapshots to download'
    )
    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )

    args = parser.parse_args()

    scraper = WaybackScraper(
        url=args.url,
        output_dir=args.output,
        delay=args.delay
    )

    scraper.scrape_all(limit=args.limit)


if __name__ == '__main__':
    main()
