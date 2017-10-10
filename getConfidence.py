import json
import sys
from watson_developer_cloud import NaturalLanguageClassifierV1

'''
natural_language_classifier = NaturalLanguageClassifierV1(
  username="04875829-47ad-4cd1-9fca-e7af9ec9fe2a",
  password="wqaF6RR7Qpe2")
'''

natural_language_classifier = NaturalLanguageClassifierV1(
  username="ae471795-0c8d-4a97-bf01-b6fd7cf44c64",
  password="Ex0swaM8kdB6")


classes = natural_language_classifier.classify('ebd44cx231-nlc-23722', sys.argv[1])
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
for result in results:
  if result[1] > threshold:
    potentials.append(result)

for element in potentials:
  print element[0]