import argparse
import csv
import json
import time

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--search', required=True)
parser.add_argument('--pages-dir')
parser.add_argument('--csv', action='store_true')
args = parser.parse_args()

def download_page(search_term, page_number):
    response = requests.get(
        'https://www.ebay.com/sch/i.html',
        params={'_nkw': search_term, '_pgn': page_number},
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=10,
    )
    response.raise_for_status()
    return response.text

def extract_listings(html):
    soup = BeautifulSoup(html, 'html.parser')
    listings = []

    for item in soup.select('.s-item'):
        title = item.select_one('.s-item__title')
        name = title.get_text(strip=True) if title else None

        price_element = item.select_one('.s-item__price')

        if price_element:
            price_text = price_element.get_text(strip=True)
            first_price = price_text.split(' to ')[0]
            clean_price = first_price.replace('$', '').replace(',', '')
            dollars, cents = clean_price.split('.')
            price = int(dollars) * 100 + int(cents)
        else:
            price = None

        status_element = item.select_one('.SECONDARY_INFO')
        status = status_element.get_text(strip=True) if status_element else None

        shipping_element = item.select_one('.s-item__shipping')

        if shipping_element:
            shipping_text = shipping_element.get_text(strip=True)

            if 'free shipping' in shipping_text.lower():
                shipping = 0
            else:
                shipping_price = shipping_text.split()[0]
                dollars, cents = shipping_price.replace('$', '').replace(',', '').split('.')
                shipping = int(dollars) * 100 + int(cents)
        else:
            shipping = None

        returns_element = item.select_one('.s-item__free-returns')

        if returns_element:
            returns_text = returns_element.get_text(strip=True).lower()
            free_returns = 'free returns' in returns_text
        else:
            free_returns = None

        sold_element = item.select_one('.s-item__hotness')

        if sold_element:
            sold_text = sold_element.get_text(strip=True)
            items_sold = int(sold_text.split()[0])
        else:
            items_sold = None

        listings.append({
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': free_returns, 
            'items_sold': items_sold
        })

    return listings

all_listings = []

for page_number in range(1, 11):
    if args.pages_dir:
        filename = f"{args.pages_dir}/page-{page_number}.html"

        with open(filename, encoding='utf-8') as file:
            html = file.read()
    else:
        html = download_page(args.search, page_number)
        time.sleep(1)

    page_listings = extract_listings(html)
    all_listings.extend(page_listings)

if args.csv:
    output_filename = f"{args.search}.csv"

    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                'name', 'price', 'status',
                'shipping', 'free_returns', 'items_sold'
            ]
        )
        writer.writeheader()
        writer.writerows(all_listings)

else:
    output_filename = f"{args.search}.json"

    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(all_listings, file, indent=4)