import json
import pandas as pd
import re
import Word2numParser as wp


def NoDuration():
    ConfigPath = "..\CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["ResponseForNoValue"].values[0])
    reason=response
    return "Gap Found", response,reason

def NoAmount():
    ConfigPath = "..\CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'liability cap amount']["ResponseForNoValue"].values[0])
    reason=response
    return "Gap Found", response,reason

def compareDuration(duration):
    ConfigPath = "..\CDAT Config.xlsx"
    ConfigTbl = pd.read_excel(ConfigPath)
    response = "No gap"
    ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']
    StandardDuration = int(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Values"].values[0])
    if (duration != StandardDuration):
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Reason"].values[0])
        return "Gap Found", response,reason  #return True, response
    else:
        response = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["Response"].values[0])
        reason = str(ConfigTbl.loc[ConfigTbl['Standards'] == 'Duration of liability']["PassingRemark"].values[0])
        return "No gap", response,reason #return False, response


def resolveDuration(duration):
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
    return x

def formulateResponseforDuration(ClassifierResponse,NERintegration):
    Confidence = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Confidence']
    print("Formulate Response for duration")
    Target = (json.loads(((ClassifierResponse['finalOutPut']['finalString']))))['Target']
    # duration="No duration"
    duration = "0"
    for i in range(NERintegration['finalOutPut']['finalList'].__len__()):
        if (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput']):
            duration = (NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['nervalue'])
            sentence = (NERintegration['finalOutPut']['finalList'][i]['sentence'])
            start = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['start'])
            end = int(NERintegration['finalOutPut']['finalList'][i]['nerDateOutput'][0]['end'])
            Start_End = sentence  # [start-3:end+4]
    print('Confidence ' + Confidence)
    if str(duration) is "0":
        outcome, response,reason = NoDuration()
        print("Duration not found")
        Start_End="Nothing found"
    else:
        x = resolveDuration(duration)

        print('Duration found:' + str(x[0]))
        outcome, response,reason = compareDuration(int(x[0]))
        print("Before curtailing",Start_End)
        Start_End = ' '.join(str(Start_End).split(',')[1:])
        print("After curtailing", Start_End)
    # Start_End=Start_End.split(',')[1:]

    print("Outcome Response", outcome, response,reason)

    #reason = 'Because of the mismatch in the duration of the liability we have categorized it as a gap'
                #'Duration': str(x[0]),
    Data = {
            'Confidence': Confidence,
            'Start_End': str(Start_End),
            'Gap_outcome': str(outcome),
            'Response': response,
            'Reason': reason
            }

    return Data