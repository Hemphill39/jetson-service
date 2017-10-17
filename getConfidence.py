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
        print "built nlc obj"

    def classify(self, queryString):
        print "using classify"
        classes = NLC.classify(self.api_ids['classifier_id'], queryString)
        print "maybe here"
        classes = classes['classes']
        print "setup classes"
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
            for result in results:
                if result[1] > threshold:
                    potentials.append(result)
            
            results = []
            for element in potentials:
                results.append(element)
            print "returning results"
            return results
