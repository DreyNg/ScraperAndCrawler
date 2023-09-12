""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""

import pandas as pd
import json
from typing import Dict, List
import re

import requests
import bs4
import urllib
from robots import process_robots, check_link_ok

# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000

def get_root(string):
    # return the root URL:
    # example: https://edstem.org/au/courses/10326/lessons/31671/slides/230348
    # result: https://edstem.org
    regex = r"([^\/\"\'>]*[^\/]*\/[^\/]*\/[^\/|\'\"]*)[\"\']?[^>]*"
    matches = re.findall(regex, string, re.IGNORECASE)
    return matches[0] if matches else None


# Task 1 - Get All Links (3 marks)
def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    
    result = {} #output dictionary
    crawled_links = set() #to keep track of link crawled
    pages_visited = 0  
    visited = {}

    # Check website robot.txt to see what links we are allowed to crawl
    for seed_url in starting_links:
        # Get the root URL of the seed URL
        base_url = get_root(seed_url) 
        # Create URL for the robots.txt file of the website
        robots_items = '/robots.txt'
        robots_url = base_url + robots_items
        try:
            page = requests.get(robots_url)
            robot_rules = process_robots(page.text)
            if not check_link_ok(robot_rules, seed_url):
                        continue
        except:
            continue 

        # Initialize the list of links to crawl for the seed URL with the seed URL itself
        result[seed_url] = [seed_url]
        try:
            page = requests.get(seed_url)
        except:
            continue
        # Parse the HTML of the seed URL using BeautifulSoup
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        # Add the seed URL to the visited dictionary
        visited[seed_url] = True
        
        # Find all links in the HTML of the seed URL
        child_links = []
        new_links = soup.findAll('a')
        for new_link in new_links:
            # Skip the links that don't have href values (links that don't actually exist or don't lead anywhere)
            if "href" not in new_link.attrs:
                continue
            new_item = new_link['href']
            # Skip any links which has been asked us not to visit.
            if not check_link_ok(robot_rules, new_item):
                continue
            # Create an absolute URL for the link by concatenating it with the base URL
            new_url = urllib.parse.urljoin(seed_url, new_item)
            # Check it's not already in the list before adding it.
            if new_url not in visited and new_url not in child_links and base_url in new_url and "#" not in new_url:
                child_links.append(new_url)

        # Crawl child links until there are no more links or hitting safe limit
        while child_links and pages_visited <= SAFE_PAGE_LIMIT:
            current_link = child_links.pop(0)
            if current_link not in result[seed_url]:
                result[seed_url].append(current_link)
            try:
                page = requests.get(current_link)
            except:
                continue
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            visited[current_link] = True
            new_links = soup.findAll('a')
            for new_link in new_links:
                if "href" not in new_link.attrs:
                    continue
                new_item = new_link['href']
                if not check_link_ok(robot_rules, new_item):
                    continue
                new_url = urllib.parse.urljoin(seed_url, new_item)
                if new_url not in visited and new_url not in child_links and base_url in new_url and "#" not in new_url:
                    child_links.append(new_url)
            pages_visited = pages_visited + 1
    
    # appending result into a dict and sort
    result = dict(sorted(result.items(), key=lambda item: (item[0], item[1])))
            

    # creating json output file
    with open(json_filename, "w") as fp:
        json.dump(result,fp,indent = 4)
    
    return result





