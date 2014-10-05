search-google
=============

Scrape Google search results with Selenium. No obfuscation other than random Firefox user-agents, just a simple scraper that returns however many pages of results you want. 1 page = 100 results. 

Dependencies
-------
* python 2.7
* Selenium


Installation
-------
```shell
pip install --user selenium
git clone https://github.com/DanMcInerney/search-google
cd search-google
```


Usage
-----
```shell
python search-google.py -p 3 -s '"Dan McInerney"'
```

Will open an instance of Firefox and search 3 pages of 100 results each for "Dan McInerney" (quotes included) in Google then print the title and url of each result.

