# Wayback Machine Scraper Bot

A Python bot that will scrape and DOWNLOAD ALL AVAILABLE SNAPSHOTS of a website from the Internet Archive's Wayback Machine.

<br>

## Features

- Fetches all available snapshots for a given URL
- Downloads snapshot content (HTML)
- Saves snapshots with timestamps
- Saves metadata JSON with snapshot information
- Respects rate limits with configurable delays
- Filters for successful captures (200 status code)
- Collapses to one snapshot per day to avoid duplicates

<br>

## Installation

```bash
pip install -r requirements.txt
```

<br>

## Usage

### Basic usage:
```bash
python wayback_scraper.py https://example.com
```

### With custom output directory:
```bash
python wayback_scraper.py https://example.com -o my_snapshots
```

### Limit number of snapshots:
```bash
python wayback_scraper.py https://example.com -l 10
```

### Adjust delay between requests:
```bash
python wayback_scraper.py https://example.com -d 2.0
```

### All options:
```bash
python wayback_scraper.py https://example.com -o output_dir -l 100 -d 1.5
```

## Arguments

- `url` (required): The URL to scrape snapshots for
- `-o, --output`: Output directory (default: `snapshots`)
- `-l, --limit`: Limit number of snapshots to download
- `-d, --delay`: Delay between requests in seconds (default: 1.0)

## Output

The bot creates:
- A directory containing all downloaded snapshots as HTML files
- A `metadata.json` file with information about all snapshots
- Filenames formatted as: `YYYY-MM-DD_HH-MM-SS.html`

## Example: python.org

```bash
python wayback_scraper.py https://python.org -l 20
```

<br>

This will:
1. Fetch up to 20 snapshots of python.org
2. Save them to the `snapshots/` directory
3. Create a `metadata.json` file with snapshot details

<br>

## Notes

- Be respectful of the Wayback Machine's resources
- The default 1-second delay between requests is recommended
- Snapshots are collapsed to one per day to avoid duplicates
- Only successful captures (HTTP 200) are downloaded

<br>
