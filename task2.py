"""
COMP20008 Semester 1
Assignment 1 Task 2
"""

import json

import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok




# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here

    result = {}
    page = requests.get(link_to_extract)
    page.encoding = page.apparent_encoding
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    # find all 'mw-content-text' div
    mw_content_text_divs = soup.findAll('div', {'id': 'mw-content-text'})
    text = ""
    for div in mw_content_text_divs:
        # remove elements th with class infobox-label
        for tag in div.find_all('th', {'class': 'infobox-label'}):
                tag.extract()
        # remove elements div with class printfooter
        for tag in div.find_all('div', {'class': 'printfooter'}):
            tag.extract()
        # remove elements with id of toc
        for tag in div.find_all('div', {'id': 'toc'}):
            tag.extract()
        # remove table elements with class of ambox
        for tag in div.find_all('table', {'class': 'ambox'}):
            tag.extract()
        # remove div elements with class of asbox
        for tag in div.find_all('div', {'class': 'asbox'}):
            tag.extract()
        # remove span elements with class of mw-editsection
        for tag in div.find_all('span', {'class': 'mw-editsection'}):
            tag.extract()
        text += div.get_text(separator=' ', strip=True)

    # change all characters to their case folded form 
    # then normalize to NFKD form
    text = text.casefold()
    text = unicodedata.normalize('NFKD', text)

    # Convern non-alphpabetical characters to single space
    # Convert all spacing characters such as tabs and newlines into single-space characters
    pattern = r'[^a-zA-Z\s\\]'
    text = re.sub(pattern, ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s(?=\S)', ' ', text)
    tokens = text.split(' ')

    # remove all stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    # remove all tokens less than 2 characters 
    tokens = [token for token in tokens if len(token) >= 2]

    # Each token should then be converted to its Porter stemming algorithm stemmed form.    
    porterStemmer = PorterStemmer()
    stemmed_token = [porterStemmer.stem(w) for w in tokens]
    result[link_to_extract] = stemmed_token


    with open(json_filename, 'w') as fp:
        json.dump(result, fp, indent=4)
    return result

