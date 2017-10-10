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
#from forms import QueryForm
import discovery
import os
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

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

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

@app.route('/api/query/<query>')
def query_watson(query):
    return jsonify(result=handle_input(query))

def handle_input(user_input):
    return discovery.query(user_input)

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


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
