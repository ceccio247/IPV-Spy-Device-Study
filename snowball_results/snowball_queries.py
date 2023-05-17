# This code was given to me courtesy of Sophie Stephenson
from datetime import datetime
from time import sleep

import requests
from query_generator import generate_seed_queries, generate_detectors_seed_queries
from good_bad_list import passes_badlist, passes_goodlist
import json

import random

def randsleep():
    sleep(4*60 + random.randrange(2*60))

SEARCH_ENGINE = 'bestbuy'
SNOWBALL_FILENAME = SEARCH_ENGINE + '-snowball.txt'
SKIPPED_FILENAME = SEARCH_ENGINE + '-skipped.txt'


MAX_QUERIES = 4000

# set to -1 to retry forever
MAX_RETRIES = -1

google_url = "https://suggestqueries.google.com/complete/search"
google_params = {"client": "chrome", "hl": "en"}

#
# send a GET request to the google suggestion API
#
def get_google_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1

        google_params["q"] = q
        r = requests.get(google_url, params=google_params)
        if r.status_code == 200:
            return r.json()[1]

        # if an issue happens, it's probably because google is blocking us
        # wait a bit
        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []

google_shopping_url = "https://shopping.google.com/complete/search"
google_shopping_params = {"hl": "en", "client": "products-cc"}
def get_google_shopping_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1

        google_shopping_params["q"] = q
        r = requests.get(google_shopping_url, params=google_shopping_params)
        if r.status_code == 200:
            # TODO try and find a better API for google shopping
            # because this is terrible
            try:
                json_str = r.text[len("window.google.ac.h("):][:-1]
                suggestions = json.loads(json_str)[0]
                return [suggestion[0].replace("<b>","").replace("</b>","") 
                        for suggestion in suggestions]
            except Exception as e:
                print(r.text)
                print(e)
                return []

        # if an issue happens, it's probably because google is blocking us
        # wait a bit
        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []

amazon_url = "http://completion.amazon.com/search/complete"
amazon_params = {"search-alias": "aps", "client": "amazon-search-ui", "mkt": "1"}

def get_amazon_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1

        amazon_params["q"] = q
        r = requests.get(amazon_url, params=amazon_params)
        if r.status_code == 200:
            return r.json()[1]


        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []



walmart_url = "https://www.walmart.com/typeahead/v3/complete"
walmart_params = {}

def get_walmart_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1
        walmart_params['term'] = q
        r = requests.get(walmart_url, params=walmart_params)
        if r.status_code == 200:
            return [query['displayName'] for query in r.json()['queries']]

        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []

bestbuy_url = "https://www.bestbuy.com/suggest/v1/fragment/suggest/www"
bestbuy_params = {}

def get_bestbuy_suggestions(q):
    sleep(1)
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1
        bestbuy_params['query'] = q
        r = requests.get(bestbuy_url, params=bestbuy_params,
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'})
        if r.status_code == 200:
            try:
                return [sugg['term'] for sugg in r.json()['suggestionResponse']['suggestions']]
            except:
                return []

        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []


ebay_url = "https://www.ebay.com/autosug"
ebay_params = {'sId': 0, 'callback': 0}
def get_ebay_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1
        ebay_params['kwd'] = q
        r = requests.get(ebay_url, params=ebay_params)
        if r.status_code == 200:
            try:
                return r.json()['res']['sug']
            except:
                # if there are no results, the above will keyerror
                return []

        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []


homedepot_url = "https://www.thdws.com/TA2/search"
def get_homedepot_suggestions(q):
    num_tries = 0
    while num_tries != MAX_RETRIES:
        num_tries += 1
        r = requests.get(homedepot_url, params={'term': q})
        if r.status_code == 200:
            return [sugg['t'] for sugg in r.json()['r']]

        print("request issue: status code", r.status_code)
        print("sleeping at", datetime.now().strftime("%H:%M:%S") + "...")
        randsleep()
    return []

#
# gets suggested queries using the seed queries, then gets suggested queries
# from those queries, etc. until no new queries emerge or we hit MAX_QUERIES
#
def snowball_queries(get_suggestions, generator):
    # create list of seed queries
    seed_queries = generator()
    final_list = seed_queries
    skipped = []

    # add queries to the snowball until there are no new queries
    while len(seed_queries) > 0 and len(final_list) < MAX_QUERIES:
        print(
            "-----------",
            len(final_list),
            "queries so far; now testing",
            len(seed_queries),
            "more seeds -----------",
        )

        # for each q, get suggestions and add new ones to our list
        new_queries = []
        stop = False
        for q in seed_queries:
            for s in get_suggestions(q):
                goodlist_result = passes_goodlist(s)
                passed_goodlist = goodlist_result[0]
                badlist_result = passes_badlist(s)
                passed_badlist = badlist_result[0]
                if ((passed_goodlist or passed_badlist) and s not in final_list and s not in new_queries):
                    new_queries.append(s)
                    print(q, "->", s)
                    if len(new_queries + final_list) >= MAX_QUERIES:
                        stop = True
                        print("MAX QUerieS reACHED")
                        break
                elif not passed_badlist:
                    if s not in skipped:
                        skipped.append(s + ', ' + badlist_result[1])
            if stop:
                break

        # update list of all queries and update seeds
        final_list += new_queries
        seed_queries = new_queries

    print("----------------------------------------------")
    print("-----------", len(final_list), "queries in total -----------")
    print("----------------------------------------------")

    # write queries to txt file & return
    f = open(SNOWBALL_FILENAME, "w")
    for q in final_list:
        f.write(q + "\n")
    f.close()

    f = open(SKIPPED_FILENAME, "w")
    for q in skipped:
        f.write(q + "\n")
    f.close()

    return final_list


ENGINE_TO_FXN = {
            'google': get_google_suggestions,
            'google-shopping': get_google_shopping_suggestions,
            'amazon': get_amazon_suggestions,
            'bestbuy': get_bestbuy_suggestions,
            'ebay': get_ebay_suggestions,
            'walmart': get_walmart_suggestions,
            'homedepot': get_homedepot_suggestions,
        }

if __name__ == "__main__":
    snowball_queries(ENGINE_TO_FXN[SEARCH_ENGINE], generate_detectors_seed_queries)
