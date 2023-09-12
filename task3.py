""" 
COMP20008 Semester 1
Assignment 1 Task 3
"""

from typing import Dict, List
import pandas as pd
import json
import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok


# Task 3 - Producing a Bag Of Words for All Pages (2 Marks)
def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here

    # Empty dataframe to demonstrate output data format.
    dataframe = pd.DataFrame()
    row = []
    for seed_url, all_link_url in link_dictionary.items():
        for link_url in all_link_url:
            result = {}
            page = requests.get(link_url)
            page.encoding = page.apparent_encoding
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
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


            # If no tokens are retrieved after pre-processing, the words string should be an empty string ''.
            if not stemmed_token:
                words = ''
            else:
                words = ' '.join(stemmed_token)

            # The rows in the csv file should be in ascending order of link_url 
            # and then (where the link_url is the same for two or more pages) seed_url.
            result['link_url'] = link_url
            result['words'] = words
            result['seed_url'] = seed_url
            row.append(result)
    dataframe = pd.DataFrame(row)
    dataframe = dataframe.sort_values(by=['link_url', 'seed_url'])
    dataframe.to_csv(csv_filename, index=False)



    return dataframe

