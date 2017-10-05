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

app = Flask(__name__)

discovery = None

discovery_collection_id="c31902df-8069-4ea2-9c75-746336721525"
discovery_configuration_id="2d31d73a-5679-49a6-9730-63d3519b6a74"
discovery_environment_id="0cfdc99b-3b1e-4b0b-b5ec-bfebf5d250dd"

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    if 'discovery' in vcap:
        print 'Found VCAP_SERVICES'
        creds = vcap['discovery'][0]['credentials']
        user = vcap['username']
        password = creds['password']
        url = creds['url']
        discovery = Discovery(url, user, password, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print 'Found local VCAP_SERVICES'
        creds = vcap['discovery'][0]['credentials']
        user = vcap['username']
        password = creds['password']
        url = creds['url']
        discovery = Discovery(url, user, password, discovery_collection_id, discovery_configuration_id,
                              discovery_environment_id)


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/api/query/<query>')
def query_watson(query):
    return jsonify(result=handle_input(query))

def handle_input(user_input):
    discovery = Discovery(app.config['discovery_url'], app.config['discovery_username'], app.config['discovery_password'], app.config['discovery_collection_id'], app.config['discovery_configuration_id'], app.config['discovery_environment_id'])
    return discovery.query(user_input)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
