# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from flask import Flask, jsonify, request
from discovery import Discovery
from speech_to_text import Speech_to_text
from getConfidence import NLC
import requests

app = Flask(__name__)

discovery = None
Speech = None
classifier = None

discovery_collection_id = "0cead13f-1bf4-438b-8c6b-e3f412d2eb3e"
discovery_configuration_id = "59aca88c-a9c2-4299-a6a2-be7e5e3eea6b"
discovery_environment_id = "67c3f67b-a49f-4156-a795-1ff97ad09e6d"

classifier_id = "ebd15ex229-nlc-54210"

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    if 'discovery' in vcap:
        discreds = vcap['discovery'][0]['credentials']
        disuser = discreds['username']
        dispassword = discreds['password']
        disurl = discreds['url']
        discovery = Discovery(disurl, disuser, dispassword,
                              discovery_collection_id,
                              discovery_configuration_id,
                              discovery_environment_id)

    if 'natural_language_classifier' in vcap:
        nlccreds = vcap['natural_language_classifier'][0]['credentials']
        nlcuser = nlccreds['username']
        nlcpassword = nlccreds['password']
        nlcurl = nlccreds['url']
        classifier = NLC(nlcurl, nlcuser, nlcpassword, classifier_id)

    if 'speech_to_text' in vcap:
        speechcreds = vcap['speech_to_text'][0]['credentials']
        speechuser = speechcreds['username']
        speechpassword = speechcreds['password']
        speechurl = speechcreds['url']
        Speech = Speech_to_text(speechurl, speechuser, speechpassword)

elif os.path.isfile('vcap-local-back.json'):
    with open('vcap-local-back.json') as f:
        vcap = json.load(f)

        discreds = vcap['discovery'][0]['credentials']
        disuser = discreds['username']
        dispassword = discreds['password']
        disurl = discreds['url']
        discovery = Discovery(disurl, disuser, dispassword,
                              discovery_collection_id,
                              discovery_configuration_id,
                              discovery_environment_id)

        speechcreds = vcap['speech_to_text'][0]['credentials']
        speechuser = speechcreds['username']
        speechpassword = speechcreds['password']
        speechurl = speechcreds['url']
        Speech = Speech_to_text(speechurl, speechuser, speechpassword)

        nlccreds = vcap['natural_language_classifier'][0]['credentials']
        nlcuser = nlccreds['username']
        nlcpassword = nlccreds['password']
        nlcurl = nlccreds['url']
        classifier = NLC(nlcurl, nlcuser, nlcpassword, classifier_id)


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')


@app.route('/audio')
def audiosend():
    return app.send_static_file('audio.html')


@app.route('/api/query', methods=['POST'])
def query_watson():
    query_obj = request.get_json()
    return jsonify(result=handle_input(query_obj))

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    request_obj = request.get_json()
    discovery_feedback(request_obj['query'], request_obj['document_id'], request_obj['feedback'])
    return jsonify(result={"response" : "Feedback submitted"})

def discovery_feedback(query, document_id, relevance):
    url = "https://gateway.watsonplatform.net/discovery/api/v1/environments/{0}/collections/{1}/training_data?version=2017-11-07".format(discovery_environment_id,discovery_collection_id)

    data = {
    "natural_language_query": query,
        "examples": [
            {
                "document_id": document_id,
                "relevance": relevance
            }
        ]
    }
    r = requests.post(url, auth=(discovery.creds['username'], discovery.creds['password']), json=data)
    print r

def handle_input(input_object):
    return_object = {'error': '', 'articles': [], 'categories': []}

    user_input = input_object['queryText']
    user_category = input_object['category']

    try:
        categories = []
        if not user_category:
            categories = nlc(user_input)
        else:
            categories.append(user_category)

        return_object['categories'] = categories

        if len(categories) == 1:
            matches = discovery.query(user_input, categories[0])
            for match in matches:
                return_object['articles'].append({'html': match['html'], 'document_id': match['id']})
    except:
        return_object['error'] = 'Error searching for request.'
    return json.dumps(return_object)


@app.route('/audio/blob', methods=['GET', 'POST'])
def get_blob():
    if request.method == 'POST':
        a = request.files['data']
        fname = os.path.join(os.getcwd()+"/static", "test.wav")
        a.save(fname)
        text = Speech.speech_to_text(fname)
        return text


def nlc(s):
    return classifier.classify(s)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
