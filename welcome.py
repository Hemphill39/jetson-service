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
from flask import Flask, jsonify, render_template, request, redirect, url_for
from discovery import Discovery
from speech_to_text import Speech_to_text
from getConfidence import NLC
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
import json

app = Flask(__name__)

discovery = None
Speech = None
classifier = None

discovery_collection_id="c31902df-8069-4ea2-9c75-746336721525"
discovery_configuration_id="2d31d73a-5679-49a6-9730-63d3519b6a74"
discovery_environment_id="0cfdc99b-3b1e-4b0b-b5ec-bfebf5d250dd"

classifier_id="ebd15ex229-nlc-54210"

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    if 'discovery' in vcap:
        print 'Found VCAP_SERVICES'
        discreds = vcap['discovery'][0]['credentials']
        disuser = discreds['username']
        dispassword = discreds['password']
        disurl = discreds['url']
        discovery = Discovery(disurl, disuser, dispassword, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)
    
    if 'natural_language_classifier' in vcap:
        print 'Found VCAP_SERVICES'
        nlccreds = vcap['natural_language_classifier'][0]['credentials']
        nlcuser = nlccreds['username']
        nlcpassword = nlccreds['password']
        nlcurl = nlccreds['url']
        classifier = NLC(nlcurl, nlcuser, nlcpassword, classifier_id)
    
    if 'speech_to_text' in vcap:
        print 'Found VCAP_SERVICES'
        speechcreds = vcap['speech_to_text'][0]['credentials']
        speechuser = speechcreds['username']
        speechpassword = speechcreds['password']
        speechurl = speechcreds['url']
        Speech = Speech_to_text(speechurl, speechuser, speechpassword)

elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print 'Found local VCAP_SERVICES'
        
        discreds = vcap['discovery'][0]['credentials']
        disuser = discreds['username']
        dispassword = discreds['password']
        disurl = discreds['url']
        discovery = Discovery(disurl, disuser, dispassword, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)

        speechcreds = vcap['speech_to_text'][0]['credentials']
        speechuser = speechcreds['username']
        speechpassword = speechcreds['password']
        speechurl = speechcreds['url']
        Speech = Speech_to_text(speechurl, speechuser, speechpassword)


        nlccreds = vcap['discovery'][0]['credentials']
        nlcuser = nlccreds['username']
        nlcpassword = nlccreds['password']
        nlcurl = nlccreds['url']
        classifier = NLC(nlcurl, nlcuser, nlcpassword, classifier_id)

# test with selenium        
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

# test with selenium
@app.route('/audio')
def audiosend():
    return app.send_static_file('audio.html')

@app.route('/api/query/<query>')
def query_watson(query):
    return jsonify(result=handle_input(query))

def handle_input(user_input):
    return discovery.query(user_input)

@app.route('/audio/blob', methods=['GET', 'POST'])
def get_blob():
    if request.method == 'POST':
        a = request.files['data']
        fname = os.path.join(os.getcwd()+"/static", "test.wav")
        a.save(fname)
        text = Speech.speech_to_text(fname)
        return text
    else:
        print 'Error saving blob'

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
