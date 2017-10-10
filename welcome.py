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
<<<<<<< HEAD
from discovery import Discovery
=======
#from forms import QueryForm
import discovery
import os
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
>>>>>>> 74cbf05e12146ad287a246a54266d0e76b687b6f

app = Flask(__name__)

discovery = None

discovery_collection_id="c31902df-8069-4ea2-9c75-746336721525"
discovery_configuration_id="2d31d73a-5679-49a6-9730-63d3519b6a74"
discovery_environment_id="0cfdc99b-3b1e-4b0b-b5ec-bfebf5d250dd"

<<<<<<< HEAD
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    if 'discovery' in vcap:
        print 'Found VCAP_SERVICES'
        creds = vcap['discovery'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = creds['url']
        discovery = Discovery(url, user, password, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print 'Found local VCAP_SERVICES'
        creds = vcap['discovery'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = creds['url']
        discovery = Discovery(url, user, password, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)
=======
@app.route('/audio')
def audiosend():
    return app.send_static_file('audio.html')

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)
>>>>>>> 74cbf05e12146ad287a246a54266d0e76b687b6f


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/api/query/<query>')
def query_watson(query):
    return jsonify(result=handle_input(query))

def handle_input(user_input):
    discovery = Discovery(app.config['discovery_url'], app.config['discovery_username'], app.config['discovery_password'], app.config['discovery_collection_id'], app.config['discovery_configuration_id'], app.config['discovery_environment_id'])
    return discovery.query(user_input)

<<<<<<< HEAD
=======
@app.route('/audio/blob', methods=['GET', 'POST'])
def get_blob():
    print "sup"
    if request.method == 'POST':
        print request.data[:100]
        print len(request.data)
        print request.files
        a = request.files['data']
        fname = os.path.join(os.getcwd()+"/static", "test.wav")
        a.save(fname)
        text = speech_to_text(fname)
        return text
    else:
        print "nah"





def speech_to_text(wavpath):
    print "speech to text"
    username = "d6e16a25-d29e-43da-9ad4-d16724f0257b"
    password = "BW7AseahEZnx"
    speech_to_text = SpeechToText(username=username,
    password=password)

    # This is all I need
    result = ""
    print "File name"
    fname = wavpath
    print fname

    try:
        with open(fname, 'rb') as audio_file:
            print "getting result"
            result = speech_to_text.recognize(audio_file, content_type='audio/wav')
            print "got result"

        text = result['results'][0]['alternatives'][0]['transcript']
        print 'What was the text?'
        print text
        return text
    except:
        return "Something went wrong. Please try again."


"""
@app.route('/query', methods=['GET', 'POST'])
def query():
    print "hey"
    form = QueryForm()
    print "sup"
    if request.method == 'POST':
        print "post"
        return handle_input(request.form['query'])
    elif request.method == 'GET':
        print "get"
        print type(render_template)
        return render_template('query.html', form=form)
"""


>>>>>>> 74cbf05e12146ad287a246a54266d0e76b687b6f
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
