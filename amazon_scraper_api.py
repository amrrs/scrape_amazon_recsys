
import os
import json
import requests

os.environ['GEMINI_API_KEY'] = 'xxx'
os.environ['SCRAPER_API_KEY'] = 'xxx'



payload = {
  'api_key': os.environ.get("SCRAPER_API_KEY") , #add your API key here
  'query': 'non-fiction books for learning programming',
  'country': 'us'
}

#send your request to scraperapi
response = requests.get(
  'https://api.scraperapi.com/structured/amazon/search', params=payload)

products = response.json()

#export the JSON response to a file
with open('amazon-products.json', 'w') as f:
   json.dump(products, f)


