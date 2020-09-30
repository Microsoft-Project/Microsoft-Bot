import enchant
import requests

dictionary = enchant.Dict("en_US")


def fetch():
    bug = requests.get('https://api.github.com/repos/opencv/opencv/issues?labels=bug')
    doc = requests.get('https://api.github.com/repos/opencv/opencv/issues?labels=documentation')
    wontfix = requests.get('https://api.github.com/repos/opencv/opencv/issues?labels=wontfix')

    data_bug = bug.json()
    data_doc = doc.json()
    data_wontfix = wontfix.json()

    bug_list = []
    doc_list = []
    wontfix_list = []

    for i in data_bug:
        bug_list.append(i['body'])

    for j in data_doc:
        doc_list.append(j['body'])

    for k in data_wontfix:
        wontfix_list.append(k['body'])

    map = dict({'bug': bug_list, 'documentation': doc_list, 'wontfix': wontfix_list})

    return map

# print(len(bug_list), len(doc_list), len(wontfix_list))
# print(map)
