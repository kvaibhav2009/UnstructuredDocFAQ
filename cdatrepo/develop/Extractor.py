import pandas as pd
from docx import Document
import string
import json
import requests


def preprocess(text):
    dictword = {"twice": "200%", "thrice": "300%"}
    for word in text.split():
        if (word in dictword.keys()):
            text=text.replace(word, dictword[word])

    return text

word='liability'
words = ['liability', 'liable']
# import Processor.Processor as pp
# duration=pp.x
filepath="Input Documents/AI Sample amount conflict1.docx"
filename="--AMountCoflict--"
print("File")
f=filepath
# f.save((f.filename))
doc = Document(f)
print("Document")
l = list()
section = list()
print("File" + str(filename))
file = "Output Documents\\" + str(filename) + ".csv"
sectionfile = "OutputSection\\" + str(filename) + "_section.csv"
x=list()
for i, paragraphs in enumerate(doc.paragraphs):
    text = (paragraphs.text)
    text = ''.join(x for x in (text.encode('utf-8').decode('latin-1')) if x in string.printable)
    if str(text):
        l.append(str(text))
    for x in words:
        if (str(text.lower()).__contains__(x)):  # if [s for s in (text.lower()).split() if any(xs in s for xs in words)]:
            text=preprocess(text)
            section.append(str(text))

            l.append(i)
            break;

d = pd.DataFrame(l)
sectiondf = pd.DataFrame(section)
sectiondf.to_csv(sectionfile)
d.to_csv(file)

text="Both the Party  will not be liable for the acts or omissions of the liable Party (or, as the case may be,\
its Affiliate), including any indemnity,   or in any manner related to arising from or in connection with\
this Agreement, for damages which will not in the aggregate exceed an amount equal to the 100% of \
the charge for Services paid to Accenture under the SOW giving rise to such liability during the\
twelve-month (12) period immediately preceding the most recent event giving rise to the claim.\
"




# Jobj=dict
# Jobj={'Data':[{'Start_End': 'StartEnd', 'Gap_outcome': 'outcome', 'Gap_outcome1': 'outcome', 'Response': 'Response'}]}
# Jobj
# {'Data': [{'Gap_outcome1': 'outcome', 'Start_End': 'StartEnd', 'Response': 'Response', 'Gap_outcome': 'outcome'}]}
# Jobj['Data'].append(data1)
# Jobj
# {'Data': [{'Gap_outcome1': 'outcome', 'Start_End': 'StartEnd', 'Response': 'Response', 'Gap_outcome': 'outcome'}, {'Start_End': 'StartEnd', 'Gap_outcome': 'outcome', 'Gap_outcome1': 'outcome', 'Response': 'Response'}]}
# Jobj
# {'Data': [{'Gap_outcome1': 'outcome', 'Start_End': 'StartEnd', 'Response': 'Response', 'Gap_outcome': 'outcome'}, {'Start_End': 'StartEnd', 'Gap_outcome': 'outcome', 'Gap_outcome1': 'outcome', 'Response': 'Response'}]}
# Jobj['Data'][0]
# {'Gap_outcome1': 'outcome', 'Start_End': 'StartEnd', 'Response': 'Response', 'Gap_outcome': 'outcome'}
# Jobj['Data'][1]
# {'Start_End': 'StartEnd', 'Gap_outcome': 'outcome', 'Gap_outcome1': 'outcome', 'Response': 'Response'}
# Jobj
# {'Data': [{'Gap_outcome1': 'outcome', 'Start_End': 'StartEnd', 'Response': 'Response', 'Gap_outcome': 'outcome'}, {'Start_End': 'StartEnd', 'Gap_outcome': 'outcome', 'Gap_outcome1': 'outcome', 'Response': 'Response'}]}



def get_answer_json(path,question):
    csvdata=pd.read_csv("C:\Enclave\Git projects\Text Analytics\CDAT Flask\OutputSection\--benchmarking--_section.csv", header=None, names=['No','text'])
    text = str()
    for x in csvdata['text'][2:]:
        text = text + " " + (x) + " "

    print(text)

    request_input = {
        "passage": "",
        "question": "",
        "text_type": "freetext",
        "file_path": "samples/contract.docx",
        "sessionParam": {"contextId": "24e81a62e5d045a22b0ff175d3c10e3cd273f4649f61d165a8bdb7929367a3c6",
                         "SenderId": "textanalysis", "SenderName": "textanalysis"}
    }

    request_input["passage"]=text
    request_input["question"]=question
    request_input_json = json.dumps(request_input)

    url='http://13.126.249.116/text-analysis-accelerator-agent/aaip/machinecomprehension/service/'
    response = requests.post(url, data=request_input_json,headers={"Content-Type": "application/json"})

    print(str(response.json()))
    jSonOutput=response.json()

    return str(response.json()["message"]['msg'])


request_input = {
        "passage": "",
        "question": "",
        "text_type": "freetext",
        "file_path": "samples/contract.docx",
        "sessionParam": {"contextId": "24e81a62e5d045a22b0ff175d3c10e3cd273f4649f61d165a8bdb7929367a3c6",
                         "SenderId": "textanalysis", "SenderName": "textanalysis"}
    }

request_input["passage"] = text
request_input["question"] = question
request_input_json = json.dumps(request_input)

url = 'http://13.126.249.116/text-analysis-accelerator-agent/aaip/machinecomprehension/service/'
response = requests.post(url, data=request_input_json, headers={"Content-Type": "application/json"})
