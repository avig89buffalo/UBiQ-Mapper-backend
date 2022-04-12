import requests
from pprint import pprint
DB_CONFIG = 'http://127.0.0.1:5000'
city = 'Buffalo'
response = requests.get(DB_CONFIG+'/cityWay',params={'city':city})


segments_data = response.json()
pprint(segments_data)