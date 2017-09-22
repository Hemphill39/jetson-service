from watson_developer_cloud import DiscoveryV1
import json

creds ={
  "url": "https://gateway.watsonplatform.net/discovery/api",
  "username": "7317fa1e-f710-4671-b25a-6b4c866e0d9c",
  "password": "lZseA0CjIFnQ"
}

api_ids ={
	'collection_id': 'c31902df-8069-4ea2-9c75-746336721525',
	'configuration_id': '2d31d73a-5679-49a6-9730-63d3519b6a74',
	'environment_id': '0cfdc99b-3b1e-4b0b-b5ec-bfebf5d250dd'
}


discovery = DiscoveryV1(
  username=creds['username'],
  password=creds['password'],
  version='2017-09-01'
)

def query(queryString):
	collections = discovery.list_collections(api_ids['environment_id'])

	qopts = {'natural_language_query':queryString, 'passages':'true', 'text':'true', 'html':'true', 'return':'text,html'}
	my_query = discovery.query(api_ids['environment_id'], api_ids['collection_id'], qopts)

	matches = my_query['results']

	topMatch = matches[0]['html']
	return topMatch
