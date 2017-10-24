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
        username = self.speechcreds['username']
        password = self.speechcreds['password']

        speech_to_text = SpeechToText(username=username,
                                      password=password)

        result = ""
        fname = wavpath

        try:
            with open(fname, 'rb') as audio_file:
                result = speech_to_text.recognize(audio_file,
                                                  content_type='audio/wav')

            text = result['results'][0]['alternatives'][0]['transcript']
            return text
        except:
            return "Something went wrong. Please try again."
