import os
import pandas as pd
from os import listdir
from docx import Document
import string
from nltk.stem import WordNetLemmatizer
# encoding: utf-8
from StringIO import StringIO
import pycurl
import certifi
import json
import re
import Utility.Word2numParser as wp
import requests

class Processor:
    word = 'liability'
    path = "C:\Enclave\Git projects\Python projects\CDATDevelop\Input Documents"
    l = list()

    outputpath = 'C:\\Enclave\\Git projects\\Python projects\\CDATDevelop\\Output Documents\\liability_section.csv'
    # path=os.pat
    # h.join(os.getcwd(),path)
    print(path)
    for f in listdir(path):
        l = list()
        section = list()
        if os.path.splitext(f)[1] in [".docx", ".doc", ".DOCX"]:
            doc = Document(path + "\\" + f)
            file = "C:\Enclave\Git projects\Python projects\CDATDevelop\Output Documents\\" + os.path.splitext(f)[
                0] + ".csv"
            sectionfile = "C:\Enclave\Git projects\Python projects\CDATDevelop\OutputSection\\" + os.path.splitext(f)[
                0] + "_" + word + "_section.csv"

            for i, paragraphs in enumerate(doc.paragraphs):
                text = (paragraphs.text)
                text = ''.join(x for x in (text.encode('utf-8').decode('latin-1')) if x in string.printable)
                if str(text):
                    l.append(str(text))
                if (str(text.lower()).__contains__(word)):
                    section.append(str(text))
            d = pd.DataFrame(l)
            sectiondf = pd.DataFrame(section)
            sectiondf.to_csv(sectionfile)
            d.to_csv(file)

    def AIEngineIntegrator(pipelineId):

        storage = StringIO()

        url = "https://aaie.accenture.com/aceapi/ace-pipeline-execution-service/execute/PipelineExecution/"
        filepath = 'C:\\Enclave\\Git projects\\Python projects\\CDATDevelop\\OutputSection\\liability_section.csv'
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        # c.setopt(c.HTTPHEADER, ['enctype : multipart/form-data', 'Content-Type: multipart/form-data'])

        c.setopt(c.USERPWD, '%s:%s' % ('ace', 'ace'))

        c.setopt(c.CAINFO, certifi.where())

        c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, filepath,
                                        c.FORM_CONTENTTYPE, 'multipart/form-data',
                                        )), ('ownerUserName', 's.b.karuppasamy'), ('ownerUserId', '130'),
                              ('executorUserName', 's.b.karuppasamy'), ('executorUserId', '130'),
                              ('pipelineId', pipelineId),
                              ('getStatusWithResponse', 'true'), ('input', ''), ('bulletHandler', 'true'),
                              ('extractText', 'true')

                              ])
        # writing output to storage NER '1041'
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        c.close()
        # Required content
        content = storage.getvalue()
        print content
        content_str = content.decode()
        data = json.loads(content_str)

        return data

    ClassifierResponse = AIEngineIntegrator('1079')
    print("Classifier response", ClassifierResponse)

    NERintegration = AIEngineIntegrator('1041')

    print("NER integration", NERintegration)

    Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']

    Target = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Target']

    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput']):
            duration = (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])

    # wp.words_to_num(duration.split('-')[0])

    # x=list()
    # for word in duration.split(' '):
    #     try:
    #         x.append(wp.words_to_num(word))
    #     except Exception as error:
    #         continue

    def resolveDuration(duration):
        x = list()
        for word in re.split(' |-', duration):
            try:
                if word.isdigit():
                    x.append(word)
                else:
                    x.append(wp.words_to_num(word))
            except Exception as error:
                continue
        return x

    x = resolveDuration(duration)

    def compareDuration(duration):
        ConfigPath = "C:\Enclave\Git projects\Text Analytics\CDAT Flask\CDAT Config.xlsx"
        ConfigTbl = pd.read_excel(ConfigPath)
        response = "No Gap"
        ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']
        StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Values"].values[0])
        if (duration != StandardDuration):
            return True, response
        else:
            response = str(ConfigTbl.loc[ConfigTbl['Response'] == 'Duration of liability']["Values"].values[0])
            return False, response

    def get_answer_json(path, question):
        csvdata = pd.read_csv(
            "C:\Enclave\Git projects\Text Analytics\CDAT Flask\OutputSection\--benchmarking--_section.csv", header=None,
            names=['No', 'text'])
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

        request_input["passage"] = text
        request_input["question"] = question
        request_input_json = json.dumps(request_input)

        url = 'http://13.126.249.116/text-analysis-accelerator-agent/aaip/machinecomprehension/service/'
        response = requests.post(url, data=request_input_json, headers={"Content-Type": "application/json"})

        print(str(response.json()))
        jSonOutput = response.json()

        return str(response.json()["message"]['msg'])

    def resolveDuration(duration):
        x = list()
        duration=re.sub('[(){}<>]', '', duration)
        for word in re.split(' |-', duration):
            if word.isdigit():
                x.append(word)

        return x[0]

    def get_notice_period(path):
        question="what is the duration of notice period of benchmarking?"
        notice_period=get_answer_json(path,question)
        notice_period=resolveDuration(notice_period)

        return notice_period

    def get_initial_period(path):
        question="what is the duration of initial period of benchmarking?"
        initial_period=get_answer_json(path,question)
        initial_period=resolveDuration(initial_period)

        return initial_period


#
# import zipfile
# document = zipfile.ZipFile("Benchmarking -  AI sample 1.docx")
# xml_content = document.read('word/{}'.format("document.xml"))

