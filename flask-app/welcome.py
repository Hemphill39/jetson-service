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
from flask import Flask, jsonify, render_template, request, redirect, url_for
from forms import QueryForm
import discovery


app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)


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


def handle_input(user_input):

    results = discovery.query(user_input)
    matches = results['matching_results']

    ret_str =  "<p><b>Matching results:</b> " + str(matches)+'<br>'
    for passage in results['passages']:
        ret_str += 'Passage:<br>'
        ret_str +=  passage['passage_text'].replace('\n',' ') + '<br>'
        ret_str += '<br>'
    ret_str += "</p>"
    return ret_str

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
