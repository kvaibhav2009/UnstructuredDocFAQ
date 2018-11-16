from PyPDF2.utils import readNonWhitespace
from flask import Flask,jsonify
from flask import *
import csv

#from werkzeug import secure_filename
from docx import Document
import pandas as pd
import string
import os
import requests
import pycurl
from StringIO import StringIO
import certifi
from numpy.testing.tests.test_utils import my_cacw

import Utility.Word2numParser as wp
import re
import Processor as p
from flask import render_template
import sys
from flask_cors import CORS, cross_origin
import page_num_extraction as pg_num
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
import os

import Doc2PDF_abi_word as abi_doc2pdf
# initializing a variable of Flask
#app = Flask(__name__)
app = Flask(__name__, static_url_path='',template_folder='templates')

app.config['CORS_HEADERS'] = 'CONTENT-TYPE'
cors = CORS(app, resources={r"/*": {"origins": "localhost"}},headers="Content-Type")


# decorating index function with the app.route
@app.route('/')
def index():
   #print("Index")
   return render_template("index.html")

#
# @app.route('/templates/')
# def root():
#     return app.send_static_file('index1.html')

def options(self, *args, **kwargs):
    self.response.headers['Access-Control-Allow-Origin'] = '*'
    self.response.headers[
        'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'


@app.route('/router', methods=['GET','POST','OPTIONS'])
def router():
    x = {
        'Path': 'https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT_Flask/outputExcel/SOW- AI for Benchmarking-Cost-3_man - Copy.docx_output.xlsx',
        'Data': [{'page_nos': '-- & Section --', 'Confidence': '0.875',
                  'Start_End': '1.We could not find the notice period in the upload document 2.2 Benchmarking    The Client may launch a Benchmarking project no more often than once per calendar year, but not before 14 months have passed from the Transition Projects Final Acceptance.',
                  'Gap_outcome': 'No gap',
                  'Reason': 'We could not find the benchmarking notice period in the uploaded SOW.The initial period is present in the benchmarking section.Benchmarking section is present with initial period as per Accenture guidelines,hence it is no gap',
                  'Checkvalue': 'Benchmarking',
                  'Response': 'The Initial period where no benchmarking is permitted should be greater than an year and minimum 30-60 days notice period before invoking benchmarking should be provided.',
                  'Clause': [
                      {'passage': 'We could not find the notice period in the upload document', 'section_no': '--',
                       'Entity_Substring': '', 'page_no': '--', 'Entity': 'Notice period'}, {
                          'passage': '2 Benchmarking    The Client may launch a Benchmarking project no more often than once per calendar year, but not before 14 months have passed from the Transition Projects Final Acceptance.',
                          'section_no': '16.2', 'Entity_Substring': '14 months', 'page_no': '17',
                          'Entity': 'Initial period'}]}]}
    #return (json.dumps(x))

    print("Router")
    word = 'liability'
    words = ['liability', 'liable']
    words=['benchmarking','benchmark']
    print(request.form)
    f = request.files['file']
    print("Printing checkboxes")
    print(request.form.getlist('keys[]'))
    print(request.form.getlist('downloadfile'))

    print("File type "+str(type(f)))
    # f.save((f.filename))
    #
    print("Document")
    l = list()
    section = list()
    CheckboxValue=request.form.getlist('keys[]')
    print("CheckboxValue "+str(CheckboxValue))
    print("Type: "+str(type(CheckboxValue)))
    json_response = {'Path':'','Data': []}
    fname=f.filename
    fname=str("".join(fname.split('.')[:-1]))+".docx"
    print("Filename "+fname)
    type(f)
    filename = os.getcwd() + "\\OutputFile\\" + f.filename
    filename=os.path.join(os.getcwd(),"OutputFile",f.filename)
    #filename=filename.replace("\\","/")
    print("Saving " + filename)
    f.save((filename))
    print("Filename " + filename)


    if(os.name=='nt'):
        import Doc2PDF_pg_num as doc2pdf
        if (str(filename.split('.')[-1]) == 'doc'):
            docxpath = doc2pdf.doc2docx(filename)
        else:
            docxpath = filename
        filename = doc2pdf.Doc2PDFConverter(filename)
    else:
        docxpath = filename
        filename = abi_doc2pdf.doc2Pdf(filename)


    pg_num.paraindex=[]
    for word in CheckboxValue:
        print("Word is "+word)
        print("Boolean: "+str(word is 'Benchmarking'))
        if(str(word)=='Benchmarking'):
            print("It is benchmarking")
            words = ['benchmarking', 'benchmark']
            ClassifierPipelineID='1096'
            NERPipelineID = '1097'
        if(str(word)=='Liability'):
            print("It is liability")
            words=['liability']
            ClassifierPipelineID = '1079'
            NERPipelineID='1041'

        sectionFile,indexfilename=pg_num.createSectionFile(filename,docxpath, words)
        print("Section filename "+sectionFile)
        print("Indexfilename "+indexfilename)
        indexfileAbspath=os.getcwd()+"\\"+indexfilename
        indexfileAbspath=os.path.join(os.getcwd(),indexfilename)
        #indexfileAbspath=indexfileAbspath.replace("\\","/")
        page_nos,sector_no=get_pagenumbers(indexfileAbspath)
        print("Page Number "+page_nos)
        print("Section Number " + sector_no)
        section_address=page_nos+" & Section "+sector_no
        print("")
        start = time.time()
        ClassifierResponse = AIEngineIntegrator(ClassifierPipelineID, sectionFile)
        done = time.time()
        elapsed = done - start
        print("Time elapsed by classifier "+str(elapsed))
        print("Classifier response", ClassifierResponse)

        start = time.time()

        #sectionfilecsv=pd.read_csv(sectionFile)
        # sectioncsvText = os.path.join("OutputSection", "sectioning_text.txt")
        # sectioncsv = pd.DataFrame(sectionfilecsv.iloc[:, 1])
        # sectioncsv.to_csv(sectioncsvText, header=None, index=None, sep=' ', mode='a')


        NERintegration = AIEngineIntegrator(NERPipelineID, sectionFile)
        done = time.time()
        elapsed = done - start
        print("Time elapsed by NER " + str(elapsed))
        print("NERintegration response", NERintegration)

        if (str(word) == 'Liability'):
            DurationData = formulateResponseforDuration(ClassifierResponse, NERintegration)
            AmountData = formulateResponseforAmount(ClassifierResponse, NERintegration)
            outcome, reason,amountresponse,durationresponse = formulateReason(DurationData, AmountData)
            clause = []
            print("Duration reason "+str(DurationData['Reason']))
            print("amountresponse,durationresponse: "+amountresponse+" "+durationresponse)
            if(len(DurationData['Start_End'])<5 or DurationData['Start_End']=="We could not find the duration of the liability from the upload document"):
                page_nos='--'
                sector_no='--'
                section_address='--'
                pagenumber='--'
                sectionnumber='--'
                DurationData['Start_End']='We could not find the duration of the liability from the upload document'
                #reason='We did not find any details in the uploaded document'
            else:

                print("*******************************************************************")
                print("Finding indexes of duration period")
                pagenumber, sectionnumber = getIndexes(DurationData['Start_End'], indexfileAbspath)
                print("*******************************************************************")
            clause_section={'Entity':'Duration of liability','page_no': pagenumber, 'section_no': sectionnumber,'passage':str(DurationData['Start_End']),'Entity_Substring':DurationData['Entity_Substring']}
            clause.append(clause_section)


            if (len(AmountData['Start_End']) < 5 or AmountData['Start_End'] == "We could not find liability amount in the uploaded SOW" or amountresponse=='We could not find the amount of liability from the uploaded SOW'):
                page_nos = '--'
                sector_no = '--'
                section_address = '--'
                pagenumber = '--'
                sectionnumber = '--'
                AmountData['Start_End'] = 'We could not find the amount of the liability from the upload document'
            else:

                print("*******************************************************************")
                print("Finding indexes of amount period")
                pagenumber, sectionnumber = getIndexes(AmountData['Start_End'], indexfileAbspath)
                print("*******************************************************************")
            clause_section={'Entity':'Amount of liability','page_no': pagenumber, 'section_no': sectionnumber,'passage':str(AmountData['Start_End']),'Entity_Substring':AmountData['Entity_Substring']}
            clause.append(clause_section)

            print("Amount of liability: "+ str(AmountData['Start_End']))

            print("%%%%%%%%%%%% Duration of liability: " + str(DurationData['Start_End']))

            if(AmountData['Start_End']==DurationData['Start_End']):
                print("+====== Amount and Duration Strat_End are same =======+")
                clause=[]
                clause_section = {'Entity': 'duration & amount of liability', 'page_no': pagenumber, 'section_no': sectionnumber,
                                  'passage': str(AmountData['Start_End']),'Entity_Substring':str(AmountData['Entity_Substring'])+"ooo"+str(DurationData['Entity_Substring'])}
                clause.append(clause_section)

            print("Clause for liability: " + str(clause))
            reason=amountresponse+"."+durationresponse+"."+reason
            Data = {
                "Checkvalue": "Liability",
                'Confidence': DurationData['Confidence'],
                'Start_End': DurationData['Start_End'],
                'Gap_outcome': outcome,
                'Response': 'The cap of liability as per Accenture standards is equal to 12 months of fees paid/payable & liability amount should not exceed the contract value(100%) ',
                'Reason': reason,
                'page_nos':section_address,
                'Clause':(clause)

            }
            #Data['Clause'].append(clause)

            print(Data)
            json_response['Data'].append(Data)
        if (str(word) == 'Benchmarking'):
            # import Utility.NERanalyzer as nr
            #
            #
            # DurationData = formulateResponseforDuration(ClassifierResponse, NERintegration)
            # AmountData = formulateResponseforAmount(ClassifierResponse, NERintegration)
            # outcome, reason = formulateReason(DurationData, AmountData)
            # Data = {
            #     'Confidence': DurationData['Confidence'],
            #     'Start_End': DurationData['Start_End'],
            #     'Gap_outcome': outcome,
            #     'Response': DurationData['Response'],
            #     'Reason': reason
            # }
            # print(Data)
            # json_response['Data'].append(Data)
            #notice_period_duration,notice_period_start_end=get_notice_period(sectionFile)
            clause = []
            initial_period_duration,initial_period_start_end,initialperiod_Entity_Substring = get_initial_period(sectionFile)
            notice_period_duration, notice_period_start_end,noticeperiod_Entity_Substring = get_notice_period_revised(sectionFile,NERintegration)

            print("Notice_period "+str(notice_period_duration))
            print("Initial_period " +str(initial_period_duration))
            print("Notice period "+str(notice_period_start_end))
            print("Initial period "+str(initial_period_start_end))
            print("*******************************************************************")

            print("Finding indexes of notice period")
            if(str(notice_period_duration) == '0'):
                pagenumber='--'
                sectionnumber='--'
                notice_period_start_end='We could not find the notice period in the upload document'
            else:
                print("Finding indexes of notice period")
                pagenumber, sectionnumber=getIndexes(notice_period_start_end,indexfileAbspath)
            print("noticeperiod_Entity_Substring: "+ noticeperiod_Entity_Substring)
            clause_section = {'Entity':'Notice period','page_no': pagenumber, 'section_no': sectionnumber, 'passage': str(notice_period_start_end),'Entity_Substring':str(noticeperiod_Entity_Substring)}
            clause.append(clause_section)

            if (str(initial_period_duration) == '0'):
                pagenumber='--'
                sectionnumber = '--'
                initial_period_start_end = 'We could not find the initial period in the upload document'
                initialperiod_Entity_Substring=''
            else:
                print("Finding indexes of initial period")
                pagenumber, sectionnumber=getIndexes(initial_period_start_end, indexfileAbspath)
            print("initialperiod_Entity_Substring: "+initialperiod_Entity_Substring)
            clause_section = {'Entity':'Initial period','page_no': pagenumber, 'section_no': sectionnumber, 'passage': str(initial_period_start_end),'Entity_Substring':str(initialperiod_Entity_Substring)}
            clause.append(clause_section)
            print("*******************************************************************")

            if(notice_period_start_end!=initial_period_start_end):
                start_end="1."+str(notice_period_start_end)+" 2."+str(initial_period_start_end)
            else:
                start_end=str(notice_period_start_end)

            NoticePeriodData=formulateResponseforNoticePeriodBechmarking(notice_period_duration)
            InitialPeriodData = formulateResponseforInitialPeriodBechmarking(initial_period_duration)
            outcome, reason,noticeperiodresponse,initialperiodresponse = formulateReasonforBenchmarking(NoticePeriodData,InitialPeriodData)
            Confidence="0.875"
            #Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']
            #print("Benchmarking confidence: "+str(Confidence))
            #reason=noticeperiodresponse+"."+initialperiodresponse+"."+reason

            if (str(initial_period_duration) == '0'):
                outcome=NoticePeriodData['Gap_outcome']
                #initialperiodresponse=''
                #noticeperiodresponse=NoticePeriodData['response']
                reason=NoticePeriodData['Reason']
            if(str(notice_period_duration) == '0'):
                outcome = InitialPeriodData['Gap_outcome']
                #initialperiodresponse= InitialPeriodData['response']
                reason = InitialPeriodData['Reason']
            if(str(notice_period_duration) == '0' and str(initial_period_duration)=='0'):
                outcome='Gap Found'
                reason = "We could not find the initial period and notice period in the upload document.Hence we have considered it as a gap"

            reason = noticeperiodresponse + "." + initialperiodresponse + "." + reason
            print("Clause for benchmarking: "+str(clause))

            Data = {
                "Checkvalue": "Benchmarking",
                'Confidence': str(Confidence),
                'Start_End': start_end,
                'Gap_outcome': outcome,
                'Response': 'The Initial period where no benchmarking is permitted should be greater than an year and minimum 30-60 days notice period before invoking benchmarking should be provided.',
                'Reason': reason,
                'page_nos': section_address,
                'Clause':(clause)
            }
            # Data = {
            #     "Checkvalue": "Benchmarking",
            #     'Confidence': 'Confidence_output',
            #     'Start_End': "start_end",
            #     'Gap_outcome': "outcome",
            #     'Response': 'Response',
            #     'Reason': 'reason'
            # }
            json_response['Data'].append(Data)
        #print("Deleting file"+filename)
        clearDirectory()
        print("Directory cleaned")
    # Data = {
    #     "Checkvalue": "Liability",
    #     'Confidence': 'Confidence_output',
    #     'Start_End': 'Start_End_Output',
    #     'Gap_outcome': 'Outcome_output',
    #     'Response': 'Response_output',
    #     'Reason': 'Reason_output'
    # }
    #
    # Data1 = {
    #     "Checkvalue":"Benchmarking",
    #     'Confidence': 'Confidence_output1',
    #     'Start_End': 'Start_End_Output1',
    #     'Gap_outcome': 'Outcome_output1',
    #     'Response': 'Response_output1',
    #     'Reason': 'Reason_output1'
    # }

    #json_response['Data'].append(Data)

    #json_response['Data'].append(Data1)

    outputFilename = "outputExcel//"+str(f.filename) + "_output.xlsx"
    outputFilename=os.path.join("outputExcel",str(f.filename) + "_output.xlsx")
    #outputFilename=outputFilename.replace("//","/")
    i=0
    OutputFile=pd.DataFrame()
    while(i < json_response['Data'].__len__()):
        tempOutputFile = pd.DataFrame(json_response['Data'][i].items(), columns=['Field', 'Response'])
        OutputFile=OutputFile.append(tempOutputFile)
        i+=1

    OutputFile.to_excel(outputFilename)

    print("OutputFilename: " + outputFilename)
    Downloadpath ="https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT_Flask/outputExcel/"+str(f.filename)+ "_output.xlsx"
    json_response['Path']=Downloadpath
    print(json_response)
    jsonOutput = json.dumps(json_response)
    return jsonOutput


def AIEngineIntegrator(pipelineId,sectionfile):

    storage = StringIO()

    url = "https://aaie.accenture.com/aceapi/ace-pipeline-execution-service/execute/PipelineExecution/"
    filepath = sectionfile#'OutputSection\\liability_section.csv'
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    # c.setopt(c.HTTPHEADER, ['enctype : multipart/form-data', 'Content-Type: multipart/form-data'])

    c.setopt(c.USERPWD, '%s:%s' % ('ace', 'ace'))

    c.setopt(c.CAINFO, certifi.where())

    c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, filepath,
                                    c.FORM_CONTENTTYPE, 'multipart/form-data',
                                    )), ('ownerUserName', 's.b.karuppasamy'), ('ownerUserId', '130'),
                          ('executorUserName', 's.b.karuppasamy'), ('executorUserId', '130'), ('pipelineId',pipelineId ),
                          ('getStatusWithResponse', 'true'), ('input', ''), ('bulletHandler', 'false'),
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

def ValidateNERforBenchmarking(pipelineId,sectionfile):
    ValidateNERforBenchmarkingResponse= AIEngineIntegrator(pipelineId, sectionfile)
    print("ValidateNERforBenchmarkingResponse : "+ str(ValidateNERforBenchmarkingResponse))
    ValidateNERforBenchmarkingResponse=json.loads(ValidateNERforBenchmarkingResponse['finalOutPut']['finalString'])
    if(str(ValidateNERforBenchmarkingResponse['Status'])=="Success" and str(ValidateNERforBenchmarkingResponse['Target'])=="noticeperiod" and float(ValidateNERforBenchmarkingResponse['Confidence'])>0.50):
        return True
    else:
        return False


def resolveDuration1(duration):
    x=list()

    duration=re.sub('[(){}<>]', '', duration)
    for word in re.split(' |-',duration):
        try:
            if word.isdigit():
                x.append(word)
            else:
                x.append(wp.words_to_num(word))
        except Exception as error:
            continue
    #x=parserduration(x,duration)

    return x

def parserduration(x,duration):
    print("Parsing duration: "+duration)
    print("Parsing x "+str(x))
    period=str(x)
    if(int(period)<=12):
        duration=duration
    print("Duration**** "+ str(duration))
    print("Boolean value: "+ str((not (duration.lower().__contains__('days') or duration.lower().__contains__('day'))) & (duration.lower().__contains__('months') or duration.lower().__contains__('month'))))
    if( (not (duration.lower().__contains__('days') or duration.lower().__contains__('day'))) & (duration.lower().__contains__('months') or duration.lower().__contains__('month'))):
        print("months found")
        period=int(x)*30
        print("Parsed Duration: "+str((period)))
    elif ((not (duration.lower().__contains__('days') or duration.lower().__contains__('day'))) & (duration.lower().__contains__('years') or duration.lower().__contains__('year'))):
        print("years found")
        period = int(x) * 365
        print("Parsed Duration: " + str((period)))

    if(str(period)==str(x) and int(period)<=12 and not (duration.lower().__contains__('days') or duration.lower().__contains__('day'))):
        period = int(period)
        print("In days")

    print("Reparsed Duration: " + str((period)))
    return period

def compareDuration(duration):
    ConfigPath = "CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = "No gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Values"].values[0])
    if (duration != StandardDuration):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["ResponseForGap"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Reason"].values[0])
        response=response.replace("qqq",str(int(duration)/30)+" months")
        return "Gap Found", response,reason  #return True, response
    else:
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["PassingRemark"].values[0])
        response = reason
        return "No gap", response,reason #return False, response


def NoDuration():
    ConfigPath = "CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["ResponseForNoValue"].values[0])
    response=str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
    response=reason
    return "Gap Found", response,reason

def NoAmount():
    ConfigPath = "CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
    reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["ResponseForNoValue"].values[0])
    response = reason
    return "Gap Found", response,reason

def compareAmount(amount):
        print("Inside compareAmount")
        ConfigPath = "CDAT Config.xlsx"
        ConfigTbl = pd.read_excel(ConfigPath)
        response = "No gap"
        ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']
        StandardAmount = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["Values"].values[0])
        if(int(amount)==0):
            outcome, response, reason = NoAmount()
            return outcome, response, reason

        if (int(amount) > StandardAmount):
            response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["ResponseForGap"].values[0])
            reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["Reason"].values[0])
            response=response.replace("qqq",str(amount)+"%")
            return "Gap Found", response, reason  # return True, response
        else:
            response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["Response"].values[0])
            reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["PassingRemark"].values[0])
            response=reason
            return "No gap", response, reason  # return False, response


def compareNoticePeriodBechmarking(duration):
    print("Inside compareNoticePeriodBechmarking")
    ConfigPath = "CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = "No gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["Values"].values[0])

    if(int(duration)==0):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["ResponseForNoValue"].values[0])
        reason="We did not find the notice period in the uploaded document"
        return "Gap Found", response,reason

    if (int(duration) <= StandardDuration):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["ResponseForGap"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["Reason"].values[0])
        return "Gap Found", response, reason  # return True, response
    else:
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking notice period']["PassingRemark"].values[0])
        response = "The notice period is present in the benchmarking section"
        return "No gap", response, reason

def compareInitialPeriodBechmarking(duration):
    print("Inside compareInitialPeriodBechmarking")
    ConfigPath = "CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = "No gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["Values"].values[0])

    if (int(duration) == 0):
        response = str(
            ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["ResponseForNoValue"].values[0])
        reason = "We did not find the intial period in the uploaded document"
        return "Gap Found", response, reason

    if (int(duration) <= StandardDuration):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["ResponseForGap"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["Reason"].values[0])
        return "Gap Found", response, reason  # return True, response
    else:
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'benchmarking initial period']["PassingRemark"].values[0])
        response = "The initial period is present in the benchmarking section"

        return "No gap", response, reason

def formulateResponseforNoticePeriodBechmarking(duration):
    print("Inside formulateResponseforNoticePeriodBechmarking")
    outcome, response, reason= compareNoticePeriodBechmarking(duration)
    Data = {


        'Gap_outcome': str(outcome),
        'Response': response,
        'Reason': reason
    }
    return Data


def formulateResponseforInitialPeriodBechmarking(duration):
    print("Inside formulateResponseforInitialPeriodBechmarking")
    outcome, response, reason = compareInitialPeriodBechmarking(duration)
    Data = {

        'Gap_outcome': str(outcome),
        'Response': response,
        'Reason': reason
    }
    return Data


def formulateResponseforDuration(ClassifierResponse,NERintegration):
    Confidence='0.83'
    #Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']
    print("Formulate Response for duration")
    #Target = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Target']
    duration="No duration"
    duration = "0"
    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'] and not str((NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])).__contains__("Section") ):
            duration = (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])
            sentence = (NERintegration['finalOutPut']['finalList'][i]['sentence'])
            start = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['start'])
            end = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['end'])
            Start_End = sentence  # [start-3:end+4]
            #Entity_Substring = sentence.split()[(sentence.split()).index(duration) - 1] + " " + sentence.split()[(sentence.split()).index(duration)] + " " + sentence.split()[(sentence.split()).index(duration) + 1]
            Entity_Substring=duration


    print('Confidence ' + str(Confidence))
    if str(duration) is "0":
        outcome, response,reason = NoDuration()
        print("Duration not found")
        Start_End="We could not find the duration of the liability from the upload document"
        Entity_Substring=''
    else:
        x = resolveDuration(duration)

        # print('Duration found:' + str(x[0]))
        # outcome, response,reason = compareDuration(int(x[0]))
        print('Duration found:' + str(x))
        outcome, response,reason = compareDuration(int(x))
        if(int(x)!=0):
            print("Before curtailing",Start_End)
            Start_End = ' '.join(str(Start_End).split(',')[0:])
            print("After curtailing", Start_End)
        else:
            print("No duration found")
            Start_End='We could not find the duration of the liability from the upload document'
    # Start_End=Start_End.split(',')[1:]

    print("Outcome Response", outcome, response,reason)


    print("For Duration passage is :" + str(Start_End))
    print("Entity_Substring: " + Entity_Substring)
    Data = {
            'Confidence': Confidence,
            'Start_End': str(Start_End),
            'Entity_Substring':str(Entity_Substring),
            'Gap_outcome': str(outcome),
            'Response': response,
            'Reason': reason

            }

    return Data


def formulateResponseforAmount(ClassifierResponse,NERintegration):
    Confidence='0.78'
    #Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']
    print("Formulate Response for Amount")
    #Target = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Target']

    percent = "0"
    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput']):
            percent = (NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput'][0]['nervalue'])
            sentence = (NERintegration['finalOutPut']['finalList'][i]['sentence'])
            start = int(NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput'][0]['start'])
            end = int(NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput'][0]['end'])
            Start_End = sentence  # [start-3:end+4]
            Entity_Substring=str(percent)
            #Entity_Substring=sentence.split()[(sentence.split()).index(percent)-1]+" "+sentence.split()[(sentence.split()).index(percent)]+" "+sentence.split()[(sentence.split()).index(percent)+1]
    print('Confidence ' + str(Confidence))

    if str(percent) is "0":
        for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
            if any(ext in NERintegration['finalOutPut']['finalList'][i]['sentence'] for ext in ['exceeds', 'exceed','exceeded']):
                percent="100"
                print("Found exceeding clause in ")
                Start_End=str(NERintegration['finalOutPut']['finalList'][i]['sentence'])
                print("-"+str((Start_End)))
                for wrd in ['exceeds', 'exceed','exceeded']:
                    if wrd in NERintegration['finalOutPut']['finalList'][i]['sentence']:
                        sentence=NERintegration['finalOutPut']['finalList'][i]['sentence']
                        Entity_Substring = sentence.split()[(sentence.split()).index(wrd) - 2]+" "+sentence.split()[(sentence.split()).index(wrd) - 1] + " " + sentence.split()[(sentence.split()).index(wrd)] + " " + sentence.split()[(sentence.split()).index(wrd) + 1]+" "+sentence.split()[(sentence.split()).index(wrd) +2]+" "+sentence.split()[(sentence.split()).index(wrd) +3]

            if any(ext in NERintegration['finalOutPut']['finalList'][i]['sentence'] for ext in ['twice', 'thrice','3 times','times']):
                percent="200"
                for wrd in ['twice', 'thrice','times']:
                    if wrd in NERintegration['finalOutPut']['finalList'][i]['sentence']:
                        sentence=NERintegration['finalOutPut']['finalList'][i]['sentence']
                        Entity_Substring = sentence.split()[(sentence.split()).index(wrd) - 1] + " " + sentence.split()[(sentence.split()).index(wrd)] + " " + sentence.split()[(sentence.split()).index(wrd) + 1]

                print("Found exceeding clause in ")
                Start_End=str(NERintegration['finalOutPut']['finalList'][i]['sentence'])
                print("-"+str((Start_End)))

    if str(percent) is "0":
        outcome, response,reason = NoAmount()
        print("Amount not found")
        Start_End="We could not find liability amount in the uploaded SOW"
        (Entity_Substring)=''
    else:
        percent = ''.join(e for e in percent if e.isdigit())
        print("Read percent "+str(percent))
        if(not percent):
            percent='0'
            outcome, response, reason = NoAmount()
            Entity_Substring=''
        # else:
        #     Entity_Substring = sentence.split()[(sentence.split()).index(percent) - 1] + " " + sentence.split()[
        #         (sentence.split()).index(percent)] + " " + sentence.split()[(sentence.split()).index(percent) + 1]

        print('Amount found:' + percent)
        outcome, response,reason = compareAmount(percent)
        Start_End = ' '.join(str(Start_End).split(',')[0:])
    # Start_End=Start_End.split(',')[1:]

    print("Outcome Response", outcome, response,reason)

    #reason = 'Because of the mismatch in the duration of the liability we have categorized it as a gap'
                #'Duration': str(x[0]),
    print("For Amount passage is :"+str(Start_End))
    print("Entity_Substring: "+Entity_Substring)
    Data = {
            'Confidence': Confidence,
            'Start_End': str(Start_End),
            'Entity_Substring': str(Entity_Substring),
            'Gap_outcome': str(outcome),
            'Response': response,
            'Reason': reason
            }



    return Data

def formulateReason(DurationData,AmountData):
    if (DurationData['Gap_outcome'] == "Gap Found" and  AmountData['Gap_outcome'] == "No gap"):
        outcome="Gap Found"
        reason=DurationData['Reason']
    if (DurationData['Gap_outcome'] == "No gap" and  AmountData['Gap_outcome'] == "Gap Found"):
        outcome="Gap Found"
        reason = AmountData['Reason']
    if (DurationData['Gap_outcome'] == "Gap Found" and  AmountData['Gap_outcome'] == "Gap Found"):
        outcome="Gap Found"
        reason='Because of the mismatch in the amount & duration of the liability we have categorized it as a gap'
    if (DurationData['Gap_outcome'] == "No gap" and  AmountData['Gap_outcome'] == "No gap"):
        outcome = "No Gap Found"
        reason="Liability section is present with amount and liability duration as per Accenture guidelines"

    durationnotfound='We could not find the duration of the liability from the upload document'
    amountnotfound='We could not find liability amount in the uploaded SOW'

    if(DurationData['Start_End']==durationnotfound and AmountData['Start_End']==amountnotfound):
        reason="We did not find duration and amount in the uploaded document.Hence, we have considered it as a gap"
    if (DurationData['Start_End'] == durationnotfound and AmountData['Start_End'] != amountnotfound):
        reason = "We did not find duration of liability in the uploaded document.Hence, we have considered it as a gap"
    if (DurationData['Start_End'] != durationnotfound and AmountData['Start_End'] == amountnotfound):
        reason = "We did not find liability amount in the uploaded document.Hence, we have considered it as a gap"

    amountresponse=AmountData['Response']
    durationresponse=DurationData['Response']

    if(str(durationresponse).__contains__('could not find')):
        outcome=AmountData['Gap_outcome']
        reason=AmountData['Reason']
    if (str(amountresponse).__contains__('could not find')):
        outcome = DurationData['Gap_outcome']
        reason = DurationData['Reason']
    if (str(durationresponse).__contains__('could not find') and str(amountresponse).__contains__('could not find')):
        outcome = 'Gap Found'
        reason = 'We did not find duration and amount in the uploaded document.Hence, we have considered it as a gap'

    return outcome,reason,amountresponse,durationresponse

def formulateReasonforBenchmarking(NoticePeriodData,InitialPeriodData):
    if (NoticePeriodData['Gap_outcome'] == "Gap Found" and  InitialPeriodData['Gap_outcome'] == "No gap"):
        outcome="Gap Found"
        reason=NoticePeriodData['Reason']
    if (NoticePeriodData['Gap_outcome'] == "No gap" and  InitialPeriodData['Gap_outcome'] == "Gap Found"):
        outcome="Gap Found"
        reason = InitialPeriodData['Reason']
    if (NoticePeriodData['Gap_outcome'] == "Gap Found" and  InitialPeriodData['Gap_outcome'] == "Gap Found"):
        outcome="Gap Found"
        reason='Because of the mismatch in the notice period & initial period of the benchmarking we have categorized it as a gap'
    if (NoticePeriodData['Gap_outcome'] == "No gap" and  InitialPeriodData['Gap_outcome'] == "No gap"):
        outcome = "No Gap Found"
        reason="Benchmarking section is present with notice period and initial period as per Accenture guidelines"
    if (NoticePeriodData['Gap_outcome'] == "Gap Found" and InitialPeriodData['Gap_outcome'] == "Gap Found" and NoticePeriodData['Reason']=='We did not find the notice period in the uploaded document'):
        outcome = "Gap Found"
        reason = 'Because we did not find the notice period,so we considered it as a gap'
        print("Reason "+ reason)

    noticeperiodresponse=NoticePeriodData['Response']
    initialperiodresponse=InitialPeriodData['Response']

    return outcome,reason,noticeperiodresponse,initialperiodresponse


def createSectionFile(f,words):
    print("File")

    # f.save((f.filename))
    doc = Document(f)
    print("Document")
    l = list()
    section = list()
    print("File" + str(f.filename))
    file = "Output Documents\\" + str(f.filename) + ".csv"
    file=os.path.join("Output Documents",str(f.filename) + ".csv")
    sectionfile = "OutputSection\\" + str(f.filename) + "_section.csv"
    sectionfile=os.path.join("OutputSection",str(f.filename) + "_section.csv")
    for i, paragraphs in enumerate(doc.paragraphs):
        text = (paragraphs.text)
        text = ''.join(x for x in (text.encode('utf-8').decode('latin-1')) if x in string.printable)

        if str(text):
            l.append(str(text))
        for x in words:
            if (str(text.lower()).__contains__(
                    x)):  # if [s for s in (text.lower()).split() if any(xs in s for xs in words)]:
                text = preprocess(text)
                section.append(str(text))
                break;
    d = pd.DataFrame(l)
    sectiondf = pd.DataFrame(section)
    sectiondf.to_csv(sectionfile)
    d.to_csv(file)

    return sectionfile

def preprocess(text):
    dictword = {"twice": "200%", "thrice": "300%","exceeds":"200%"}  #,"exceed":"200%","exceeds":"200%","exceeded":"200%"
    for word in text.split():
        if (word in dictword.keys()):
            text=text.replace(word, dictword[word])

    return text

def get_answer_json(path, question):
        print("Get answer from "+ str(path))
        csvdata = pd.read_csv(
            path, header=None,
            names=['text'])   # names=['No', 'text'])
        text = str()
        for x in csvdata['text'][1:]:
            text = text + " " + str(x) + " "

        #print(text)
        text=text.strip()
        text=text.replace("\n","")
        text = text.replace("\r", "")
        request_input = {
            "passage": "",
            "question": "",
            "text_type": "freetext",
            "file_path": "samples/contract.docx",
            "sessionParam": {"contextId": "24e81a62e5d045a22b0ff175d3c10e3cd273f4649f61d165a8bdb7929367a3c6",
                             "SenderId": "textanalysis", "SenderName": "textanalysis"}
        }
        print("Constructed passage "+text)
        if(text==""):
            text="abc def"

        request_input["passage"] = text
        request_input["question"] = question
        request_input_json = json.dumps(request_input)

        url = 'http://13.126.124.103/text-analysis-accelerator-agent/aaip/machinecomprehension/service/' #13.126.124.103 #13.126.249.116
        print("Request "+request_input_json)
        response = requests.post(url, data=request_input_json, headers={"Content-Type": "application/json"})

        print("Machine comprehension integration status "+str(response.status_code))
        #print(str(response.json()))
        #jSonOutput = response.json()

        NERvalue=str(response.json()["message"]['msg'])
        print("NER value from machine comprehension "+(NERvalue))
        # start_end=""
        # for sent in text.split('.'):
        #     tempstr=sent.replace("\r","")
        #     tempstr=tempstr.replace("\n","")
        #     if (NERvalue in tempstr):
        #         print(tempstr)
        #         start_end=tempstr
        #         break
        passage=text
        start_end = ""
        for msg in NERvalue.split('.'):
            #print(msg)
            for sent in passage.split('.'):
                tempstr = sent.replace("\r", "")
                tempstr = tempstr.replace("\n", "")
                if (msg in tempstr and (tempstr!=start_end)):
                    print(tempstr)
                    start_end = start_end + tempstr + "."
                    break;
        # for x in csvdata['text'][1:]:
        #     if(str(x).__contains__(NERvalue)):
        #         print("Index:")
        #         print(str(int(csvdata.loc[csvdata['text'] == str(x)]['No'].values[0])))
        #         break;

        print("Start_end",start_end)

        return NERvalue,start_end

def resolveDuration(duration):
        print ("Resolving benchmarking NER")
        x = list()
        print("Unprocessed duration "+duration)
        tempduration=duration
        duration=duration.replace("0", '')

        duration = re.sub('[(){}<>]', '', duration)
        for word in re.split(' |-', duration):
            try:
                if word.isdigit():
                    x.append(word)
            except Exception as error:
                continue

        if(x.__len__()==0):
            num_word = [y for y in re.split(' |-', duration) if (y in wp.numwords.keys())]
            x=[wp.words_to_num("-".join(num_word))]

        period = parserduration(x[0], duration)

        print("Period value "+str(period))

        return period

def get_notice_period(path):
        question = "notice"
        print(question)
        #notice_period,start_end = get_answer_json(path, question)

        print("First call for notice period")
        notice_period, start_end = get_answer_json(path, question)
        first_response = [start_end]
        print("First response :" + start_end)
        first_response_DF = pd.DataFrame(first_response)
        first_response_DF.to_csv("first_response_DF.csv")
        print("Second call for notice period")
        question = "what is duration of  notice?"
        notice_period, start_end = get_answer_json("first_response_DF.csv", question)



        notice_period = resolveDuration((notice_period))
        ##### workaround code for noticeperiod
        #Create CSV

        start_end_list=[start_end]

        start_end_DF = pd.DataFrame(start_end_list)
        start_end_DF.to_csv("start_end_csv.csv")

        #Call the classifier for validating the notice period
        print("Following file is created: start_end_csv.csv ")
        if(True):  #ValidateNERforBenchmarking('1118', 'start_end_csv.csv')
            notice_period=resolveDuration(start_end)
            print("Final notice "+str(notice_period))
        else:
            notice_period=0
            print("Final notice "+str(notice_period))
        #####
        return notice_period,start_end

def get_notice_period_revised(sectionFile,NERintegration):
    notice_period=0
    Start_End=''
    counter=0
    noticeperiod_Entity_Substring=''
    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'] and str(NERintegration['finalOutPut']['finalList'][i]['sentence']).lower().__contains__('notice') and not str(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue']).__contains__("0")):
            print("Notice period found")
            duration = (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])
            print("Duration: "+duration)
            sentence = str((NERintegration['finalOutPut']['finalList'][i]['sentence'])).replace("\r","")
            print("Notice period found in "+str(sentence))
            notice_period = resolveDuration(sentence)
            Start_End = ' '.join(str(sentence).split(',')[:])
            noticeperiod_Entity_Substring=str(duration)
            break;
        counter+=1
    print("NERintegration index: "+str(NERintegration['finalOutPut']['finalList'].__len__()))

    print("NER for notice found at: "+str(counter))

    print("Final notice " + str(notice_period))
    print("Sentence where notice period is found: "+str(Start_End))
    #NERintegration=AIEngineIntegrator(path)


    return notice_period, str(Start_End),noticeperiod_Entity_Substring


def get_initial_period(path):
        question ="what is the duration of project 's final acceptance ?" #"what is the duration of service commencement date?" # "what is the duration of project 's final acceptance ?"
        print(question)
        initial_period,start_end = get_answer_json(path, question)
        initialperiod_Entity_Substring=initial_period
		text=initialperiod_Entity_Substring
        if (text.__len__() > 150):
            initialperiod_Entity_Substring = ''.join((text.split('.'))[0]) + '.'
            initial_period=initialperiod_Entity_Substring
			
        initial_period = resolveDuration((initial_period))

        return initial_period,start_end,initialperiod_Entity_Substring

def clearDirectory():
    path=os.getcwd()+"\\OutputFile"
    path=os.path.join(os.getcwd(),"OutputFile")
    #path=path.replace("\\","/")
    from os import walk
    print("Cleaning "+path)
    for (filename) in os.listdir(path):
        #os.remove(path + "\\" + filename)
        #print("Removed " + filename)
        if (filename.__contains__('~$')):

            os.remove(os.path.join(path,filename))
            print("--Removed-- "+filename)
    # for (filename) in os.listdir(path):
    #         os.remove(path + "\\" + filename)
    return


def get_pagenumbers(indexfilepath):
    import math
    try:
        indexfile=pd.read_csv(indexfilepath)
        indices=indexfile['1'].values
        page_nos=str(list(set(indices.flat))).strip('[]')
        sector_indices = indexfile['2'].values
        sector_no = str((list(set(sector_indices.flat)))[::-1]).strip('[]')
        if(math.isnan(float(sector_no))):
            page_nos = '--'
            sector_no='--'
    except Exception as error:
        page_nos = '--'
        sector_no='--'
        print("No page found")




    return page_nos,sector_no

def getIndexes(start_end,indexfilepath):
    print("Finding indexes for :" +start_end)
    columns = ["Text", "page_nos", "section_nos"]
    indexfile = pd.read_csv(indexfilepath, names=columns, header=None)
    match=[]
    for i in range(indexfile.__len__()):
        passage=str(indexfile['Text'].iloc[i])
        if((passage)):
            match.append(float(pg_num.String_Subsequence(start_end,passage))) #int(longest_common_subsequence(start_end,passage)))
        else:
            match.append(0)

    myMax=max(match)
    index=match.index(max(match))

    print("Max value: "+str(myMax)+" index :"+str(index))
    pageno=indexfile['page_nos'].iloc[index]
    sectionnumber=indexfile['section_nos'].iloc[index]
    import math
    try:
        if(math.isnan(float(sectionnumber))):
            sectionnumber='--'
    except:
        sectionnumber = '--'
    print("Found in page "+str(pageno)+" & section "+str(sectionnumber))
    return str(pageno),str(sectionnumber)


def longest_common_subsequence(X, Y):
    # find the length of the strings
    try:
        m = len(X)
        n = len(Y)

        # declaring the array for storing the dp values
        L = [[None] * (n + 1) for i in xrange(m + 1)]

        """Following steps build L[m+1][n+1] in bottom up fashion 
        Note: L[i][j] contains length of LCS of X[0..i-1] 
        and Y[0..j-1]"""
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i - 1] == Y[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])

                    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
        score=L[m][n]
    except Exception as error:
        score="0"
    return score


def highestNumber(l):
    print("getting highet number match :")
    myMax = l[0]
    for num in l:
        if myMax < num:
            myMax = num

    index=l.index(myMax)
    return myMax,index


if __name__ == "__main__":

    if(os.name=='nt'):
        hostIP='127.0.0.1'
        portno=4998
    else:
        hostIP = '0.0.0.0'
        portno = 80
    app.run(debug=True, threaded=True, host=hostIP, port=portno)

#<img src="img/load.gif"  id="loader">
# alert(obj['Start_End']);
#       $("#outputBox").show();
#       $(".outputText").text(obj['Start_End']);
#       $(".feedbackHead").text(obj['Response']);
#       $(".gap").text(obj['Gap_outcome']);
#c=' '.join(str(txt).split(',')[1:])


#for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
#     if (NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput']):
#         percent = (NERintegration['finalOutPut']['finalList'][i]['nerPercentageOutput'][0]['nervalue'])
#percent=''.join(e for e in percent if e.isdigit())

#@2018 Accenture.All Rights Reserved
#http://127.0.0.1:5000/router
#http://13.232.229.71/router

#https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT%20Flask/OutputSection/AI%20Sample%20%20duration%20conflict.docx_section.csv?download=1
#https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT%20Flask/"+result1.Path+"?download=1
#"https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT_Flask/"+result1.Path+"?download=1"