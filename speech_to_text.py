from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

class Speech_to_text():
    speechcreds = {}

    def __init__(self, url, username, password):
        self.speechcreds['url'] = url
        self.speechcreds['username'] = username
        self.speechcreds['password'] = password

        self.Speech_to_text = SpeechToText(
            username=self.speechcreds['username'],
            password=self.speechcreds['password'],
        )

    def speech_to_text(self, wavpath):
        print "speech to text"
        username = self.speechcreds['username']
        password = self.speechcreds['password']

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