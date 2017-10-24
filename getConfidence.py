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
        classes = self.nlc.classify(self.api_ids['classifier_id'], queryString)['classes']

        maxVal = max(classes, key=lambda cat: cat['confidence'])['confidence']
        threshold = maxVal - 0.4
        potentials = [cat['class_name'] for cat in classes if cat['confidence'] > threshold]

        return potentials[:3]
