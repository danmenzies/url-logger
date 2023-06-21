import os
import csv
import time
import chardet
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def find_urls(domain):
    """
    Find all URLs in a domain
    :param domain: Domain to crawl
    :return: Number of URLs found
    """

    # Log the number of URLs found
    urls_found = 0
    urls_crawled = 0

    # Path for the data directory
    data_dir = './data'

    # Create 'data' directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # CSV file path
    csv_file = f"../{data_dir}/{domain}.csv"

    # If the csv file already exists, load the existing URLs
    existing_urls = set()
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        existing_urls = set(df['url'].values)

    # URLs to be crawled
    urls_to_crawl = [f"https://{domain}"]

    # URLs already crawled
    crawled_urls = set()

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)

        # If the file is empty, write the header
        if f.tell() == 0:
            writer.writerow(['url'])

        while urls_to_crawl:
            url = urls_to_crawl.pop(0)

            if url in crawled_urls or url in existing_urls:
                continue

            response = requests.get(url)
            encoding = chardet.detect(response.content)['encoding']
            response.encoding = encoding

            if response.status_code == 200:
                crawled_urls.add(url)
                writer.writerow([url])

                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:

                        # Construct full URL. Takes care of inconsistent domain links, relative paths, and root paths.
                        full_url = urljoin(url, href)
                        parsed = urlparse(full_url)

                        # Ensure the url is not external
                        if parsed.netloc == domain:
                            urls_to_crawl.append(full_url)
                            print('Found URL: ' + full_url)

                    # Increment the counter
                    urls_found += 1

            # Increment the counter
            urls_crawled += 1

            # Wait 1 second before the next request
            time.sleep(1)

    print(f"Found {urls_found} URLs")
    print(f"Crawled {urls_crawled} URLs")

if __name__ == '__main__':
    # Get domain from the user
    domain = input("Enter the domain: ")

    # Start crawling
    find_urls(domain)