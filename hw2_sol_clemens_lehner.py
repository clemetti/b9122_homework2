# -*- coding: utf-8 -*-
"""
Computing for Business Research - Homework Assignment #1

This version: October 9th 

@author: Clemens Lehner (cl4471) 
"""


#-----------------------------------------------------------------------------#
# Question 1.1
#-----------------------------------------------------------------------------#

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Initialize variables
seed_url = "https://press.un.org/en"
max_urls_to_search = 10
press_release_count = 0
press_release_urls = []
press_release_texts = []

look_for = "/en/press-release"

# Function to check if a page is a press release
def is_press_release(soup, look_for):
    press_release_link = soup.find('a', href=look_for, hreflang="en")
    return press_release_link is not None

# Function to check if a press release contains the word "crisis"
def contains_crisis(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find(class_="col-md-9 mb-2 panel-panel radix-layouts-main-column") 
    current_text = element.get_text()
    return "crisis" in current_text.lower()

# Function to extract press release content
def extract_press_release_content(url):
    global press_release_count
    press_release_count += 1
    print(f"Extracting Press Release {press_release_count}")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.find(class_="col-md-9 mb-2 panel-panel radix-layouts-main-column") 
    current_text = element.get_text()
    press_release_texts.append(current_text)

# Initialize list of URLs to visit
urls_visited = [seed_url]

# Crawl the website
while urls_visited and len(press_release_urls) < max_urls_to_search:
    current_url = urls_visited.pop(0)
    
    try:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if is_press_release(soup, look_for):
            if contains_crisis(current_url):
                press_release_urls.append(current_url)
                extract_press_release_content(current_url)
                
        else:
            # If it's not a press release, find links and add to urls_visited
            links = soup.find_all('a', href=True)
            for link in links:
                absolute_url = urljoin(seed_url, link['href'])
                if absolute_url.startswith(seed_url) and absolute_url not in urls_visited:
                    urls_visited.append(absolute_url)
        
    except Exception as e:
        print(f"Error processing {current_url}: {e}")

print("\nPress Releases Extracted:")
for url in press_release_urls:
    print(url)
    



#-----------------------------------------------------------------------------#
# Question 1.2
#-----------------------------------------------------------------------------#


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Initialize variables
seed_url = "https://www.europarl.europa.eu/news/en/press-room"
max_urls_to_search = 10
press_release_count = 0
press_release_urls = []
press_release_texts = []


# Function to check if a page contains the word "crisis"
def contains_crisis(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return "crisis" in text.lower()

# Function to extract press release content
def extract_press_release_content(url):
    global press_release_count
    press_release_count += 1
    print(f"Extracting Press Release {press_release_count}")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check if the press release is related to plenary sessions
    if soup.find("span", class_="ep_name", text="Plenary session"):
        text = soup.get_text()
        #content = soup.find("div", class_="content").text

    # Check if the word "crisis" is in the content
    if "crisis" in text.lower():
        press_release_texts.append(text)
        

# Initialize list of URLs to visit
urls_visited = [seed_url]

# Crawl the website
while urls_visited and len(press_release_urls) < max_urls_to_search:
    current_url = urls_visited.pop(0)
    
    try:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if contains_crisis(current_url):
                press_release_urls.append(current_url)
                extract_press_release_content(current_url)
                             
        else:
            # If it's not a press release, find links and add to urls_visited
            links = soup.find_all('a', href=True)
            for link in links:
                absolute_url = urljoin(seed_url, link['href'])
                if absolute_url.startswith(seed_url) and absolute_url not in urls_visited:
                    urls_visited.append(absolute_url)
       
    except Exception as e:
        print(f"Error processing {current_url}: {e}")

print("\nPress Releases Extracted:")
for url in press_release_urls:
    print(url)
    
    
    
    





    