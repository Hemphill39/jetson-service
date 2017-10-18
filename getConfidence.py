import json
from watson_developer_cloud import NaturalLanguageClassifierV1

class NLC():
    creds = {}
    api_ids = {}

    def __init__(self, url, username, password, classifier_id):
        self.creds['url'] = url
        self.creds['username'] = username
        self.creds['password'] = password

        self.api_ids['classifier_id'] = classifier_id

        self.nlc = NaturalLanguageClassifierV1(
            username=self.creds['username'],
            password=self.creds['password']
        )

    def classify(self, queryString):
        classes = self.nlc.classify(self.api_ids['classifier_id'], queryString)
        classes = classes['classes']
        results = []
        maxVal = 0
        for cat in classes:
            name = cat['class_name']
            val = cat['confidence']
            if val > maxVal:
                maxVal = val
                results.append((name, val))

        potentials = []
        threshold = maxVal-0.4
        for cat in classes:
            if cat > threshold:
                potentials.append(cat)

        return potentials[0:3]
