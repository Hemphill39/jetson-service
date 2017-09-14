from watson_developer_cloud import DiscoveryV1
import json

creds = {
  "url": "https://gateway.watsonplatform.net/discovery/api",
  "username": "d63aaeac-5cb8-4abc-9da6-ee8cfa5aaf46",
  "password": "3kmLV1UWHTKG"
}

api_ids ={
	'collection_id': '505c434f-dfe8-4386-b58e-7ff03b409df6',
	'configuration_id': 'a914a697-b804-480d-9048-918a13cf856a',
	'environment_id': 'a8471367-179f-4548-b53c-7a184b5dd10d'
}


discovery = DiscoveryV1(
  username=creds['username'],
  password=creds['password'],
  version='2017-09-01'
)

collections = discovery.list_collections(api_ids['environment_id'])
print(json.dumps(collections, indent=2))



qopts = {'natural_language_query':'Microwaves that turn on', 'passages':'true', 'highlight':'true', 'text':'true', 'html':'true',
			'return':'text,html'
		}
my_query = discovery.query(api_ids['environment_id'], api_ids['collection_id'], qopts)

results = my_query
matches = results['matching_results']

print "Matching results:", matches
for passage in results['passages']:
	print 'Passage:'
	print passage['passage_text'].replace('\n',' ')
	print
	print

#print(json.dumps(my_query, indent=2))