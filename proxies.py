# Copyright (C) 2026 PeruvianWizard.
# All Rights Reserved.
# It may be used however you want as long as it doesn't break a law.

import requests
from bs4 import BeautifulSoup
import queue
import threading

# Function that parses through the free-proxy-list.net/en/ html content 
# using beautiful soup and returns a queue with all the extracted US proxies.
# column[0] = IP Address
# column[1] = port
# column[2] = Code
# column[3] = Country
def extract_proxies():
    url = "https://free-proxy-list.net/en/"
    site_html_data = requests.get(url).text
    soup = BeautifulSoup(site_html_data, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')

    list_proxies = queue.Queue()
    
    # Get the 10 first proxies
    for row in rows[1:15]:
        column = row.find_all('td')
        proxy = f"{column[0].get_text()}:{column[1].get_text()}"
        if column[3].get_text() == "United States":
            list_proxies.put(proxy)
    
    return list_proxies

# Returns a list of valid proxy addresses
def get_valid_proxies():
    possible_proxies = extract_proxies()
    valid_proxies = queue.Queue()

    # check_proxies() - gets a proxy address from the queue and tests its connection.
    # if the connection succeeds, the proxy address is added to a queue of valid proxy addresses.
    def check_proxies():
        nonlocal possible_proxies
        nonlocal valid_proxies
        while not possible_proxies.empty():
            try:
                proxy = possible_proxies.get()
                r = requests.get("http://ipinfo.io/json", 
                                proxies={"http": proxy, "https": proxy})
            except:
                continue
            
            if r.status_code == 200:
                valid_proxies.put(proxy)

    # The proxies will be tested using multiple threads
    threads = []
    for _ in range(10):
        t = threading.Thread(target=check_proxies)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return list(valid_proxies.queue)