# Project 2: Scraping eBay

## About the Project 

For Project 2, I created a python program called ebay-dl.py that collects product listings from eBay search results then saves them into JSON files, or at least I hope it does! 

The program takes a search term from the command line and goes through 10 pages of results! It uses Requests to download the pages and then Beautiful Soup to find information about each item. For each product, this beautiful program extracts each product's name, price, condition, shipping cost, free returns, and number of items sold! 

If a listing does not include certain information, the program saves it as null in the JSON file! 

## How to Run 

First, install the required Python libraries:

```bash
python -m pip install requests beautifulsoup4
```

## To Run the Scraper

To scrape live eBay search results:

```bash
python ebay-dl.py --search "garden tools"
```

If eBay blocks automated requests, use the provided practice HTML pages.

## Three Saved Searches

I used the practice HTML pages provided from the assignment to create my three JSON files: 

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages
python ebay-dl.py --search "drill press" --pages-dir practice-pages
```

These commands create the following: 

- `garden tools.json`
- `stuffed animal.json`
- `drill press.json`

Each file contains 30 listings from the 10 practice pages. The listings are not real, so the contents are the same even though the search terms are different. It ain't a live eBay result... that is above my pay grade. 

## Project Instructions

[CSCI 40 — Project 2: Scraping eBay](https://csci40.rtealwitter.com/topics/05_web_scraping/project.html)

## My Beautiful Extra Credit: CSV Files 

Since my quizzes have been making me look like a grandma asking her grandson to help her log into her yahoo account, I added a --csv option so the program can save the product listings as CSV files instead of JSON files!

These are the commands I used to create my three CSV files:

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages --csv
python ebay-dl.py --search "drill press" --pages-dir practice-pages --csv