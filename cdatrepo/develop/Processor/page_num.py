from tika import parser
from pandas import DataFrame
from bs4 import BeautifulSoup
import Doc2PDF as doc2pdf
## Filepath to the pdf
import pandas as pd
import string

# 8 /29/2018
# pdf_file=doc2pdf.Doc2PDFConverter(inputFile)
#
# #pdf_file = r'C:\Users\binit.kumar.bhagat\Documents\CDAT\Page_no_prob\dumps\Liability -  AI sample 1 .pdf'
#
# pdf_parsed = parser.from_file(pdf_file, xmlContent=True)
#
# soup = BeautifulSoup(pdf_parsed['content'], "lxml")
#
# text_list = []
# counter = 1
# for page in soup.find_all("div"):
#     print('\n\n'+'Page '+str(counter))
#     for sect in page.find_all("p"):
#         print(sect.text)
#         text_dict = {"sect": sect.text, "page": counter}
#         text_list.append(text_dict)
#     counter += 1
f='C:\\Enclave\\Git projects\\Text Analytics\\CDAT_Flask\\Input Documents\\Benchmarking -  AI sample 1.docx'
word=['benchmarking', 'benchmark']



def createSectionFile(f,words):
    print("File")
    text_list=textlist(f)
    # f.save((f.filename))
    #doc = Document(f)
    print("Document")
    l = list()
    section = list()
    file = "Output Documents\\" + "sectioning" + ".csv"
    sectionfile = "OutputSection\\" + "sectioning" + "_section.csv"
    indexfile=list()
    for i, paragraphs in enumerate(text_list):
        text = (paragraphs['sect'])
        text = ''.join(x for x in (text.encode('utf-8').decode('latin-1')) if x in string.printable)

        if str(text):
            l.append(str(text))
        for x in words:
            if (str(text.lower()).__contains__(
                    x)):  # if [s for s in (text.lower()).split() if any(xs in s for xs in words)]:
                text = preprocess(text)
                section.append(str(text))
                index=[paragraphs['sect'],paragraphs['page']]
                indexfile.append(index)
                break;
    d = pd.DataFrame(l)
    sectiondf = pd.DataFrame(section)
    sectiondf.to_csv(sectionfile)
    d.to_csv(file)
    indexfiledf = pd.DataFrame(section)
    indexfilename="Output Documents\\" + "sectioning_dict" + ".csv"
    indexfiledf.to_csv(indexfilename)

    return sectionfile,indexfilename

def preprocess(text):
    dictword = {"twice": "200%", "thrice": "300%","exceeds":"200%"}  #,"exceed":"200%","exceeds":"200%","exceeded":"200%"
    for word in text.split():
        if (word in dictword.keys()):
            text=text.replace(word, dictword[word])

    return text

def textlist(f):
    inputFile = "C:\Enclave\Git projects\Text Analytics\CDAT Flask\FileConversion\AI Sample amount conflict.docx"
    inputFile=f
    pdf_file = doc2pdf.Doc2PDFConverter(inputFile)

    # pdf_file = r'C:\Users\binit.kumar.bhagat\Documents\CDAT\Page_no_prob\dumps\Liability -  AI sample 1 .pdf'

    pdf_parsed = parser.from_file(pdf_file, xmlContent=True)

    soup = BeautifulSoup(pdf_parsed['content'], "lxml")

    text_list = []
    counter = 1
    for page in soup.find_all("div"):
        print('\n\n' + 'Page ' + str(counter))
        for sect in page.find_all("p"):
            print(sect.text)
            text_dict = {"sect": sect.text, "page": counter}
            text_list.append(text_dict)
        counter += 1

    #print(text_list)
    return text_list

sectionfile,indexfilename=createSectionFile(f,word)

print("Section file "+sectionfile)
print("Index file "+indexfilename)