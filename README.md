# Python URL Logger

A simple python script to extract URL endpoints from a website. One of a number of tools in my arsenal
for helping migrate websites between platforms, with little to no SEO penalty.

This script will extract all URLs from a website, and log them to a CSV file; making it easier to plan
the URL structure for your new website

## Setup

1. Clone the repo to your local machine `git clone git@github.com:danmenzies/url-logger.git`
2. Create a virtual environment `python3 -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install the requirements `pip install -r requirements.txt`

## Usage

Once either of these scripts has finished, see the `./data` directory for the CSV file containing the URLs

**Crawler:**

1. Open the `./scripts/` directory
2. Run the script `python manual-crawl.py`
3. Enter the domain (or subdomain) of the website you want to extract URLs from
4. Grab a coffee, this may take a while...

**Sitemap Grabber:**

1. Open the `./scripts/` directory
2. Run the script `python convert-sitemap.py`
3. Enter the domain (or subdomain) of the website you want to extract URLs from

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
You are also welcome to fork the repo and make your own changes, if you prefer; and I welcome any requests to merge
back into the main branch.

Feedback is also welcome, if you have any suggestions for improvements, please open an issue.

## Disclaimer

Please only scrape sites you have been authorised to scrape! I take no responsibility for any misuse of this script.
