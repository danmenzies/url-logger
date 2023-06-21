import os
import csv
import requests
import pandas as pd
from xml.etree import ElementTree as ET

def parse_sitemap(domain):
    """
    Parse a domain's sitemap.xml
    :param domain: Domain to parse
    """

    # Path for the data directory
    data_dir = './data'

    # CSV file path
    csv_file = f"../{data_dir}/{domain}.csv"

    # If the csv file already exists, load the existing URLs
    existing_urls = set()
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        existing_urls = set(df['url'].values)

    # Starting sitemap URL
    sitemap_url = f"https://{domain}/sitemap.xml"

    # A set to hold the parsed URLs
    parsed_urls = set()

    # Create a recursive function to handle possible sitemap indices
    def parse_sitemap_url(url):
        """
        Parse a sitemap URL and add URLs to parsed_urls
        :param url: Sitemap URL to parse
        """

        # Send a GET request to the sitemap URL
        response = requests.get(url)

        # If the status code is not 200, i.e., the sitemap is not accessible, exit the function
        if response.status_code != 200:
            return

        # Parse the XML content of the response
        tree = ET.fromstring(response.content)

        # Define the XML namespaces in a dictionary (some sitemaps use the "sitemap" namespace)
        namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Find all <url> tags in the XML - these contain the URLs
        urls = tree.findall('sitemap:url', namespaces)

        # If the <url> tags are not found, try to find <sitemap> tags - these contain the sitemap URLs
        if not urls:
            urls = tree.findall('sitemap:sitemap', namespaces)

        # Loop through each <url> or <sitemap> tag found
        for url in urls:

            # Find the <loc> tag - this contains the actual URL or sitemap URL
            loc = url.find('sitemap:loc', namespaces)

            # If the <loc> tag is not found, continue to the next iteration
            if loc is None:
                continue

            # Get the text content of the <loc> tag, i.e., the actual URL or sitemap URL
            loc_url = loc.text.strip()

            # If the URL is a sitemap URL (i.e., it ends with ".xml"), parse this sitemap URL
            if loc_url.endswith('.xml'):
                parse_sitemap_url(loc_url)

            # Else, add the URL to the parsed URLs set
            else:
                parsed_urls.add(loc_url)

    # Call the recursive function to parse the sitemap URL
    parse_sitemap_url(sitemap_url)

    # Write the parsed URLs to the CSV file, excluding the existing URLs
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)

        # If the file is empty, write the header
        if f.tell() == 0:
            writer.writerow(['url'])

        for url in parsed_urls:
            if url not in existing_urls:
                writer.writerow([url])
                print('Logged URL: ' + url)

if __name__ == '__main__':
    # Get domain from the user
    domain = input("Enter the domain: ")

    # Start parsing
    parse_sitemap(domain)
