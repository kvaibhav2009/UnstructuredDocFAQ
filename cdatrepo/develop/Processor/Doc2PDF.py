from docx import Document
import sys
import os
import comtypes.client
import win32com.client
import pythoncom

pythoncom.CoInitialize()
wdFormatPDF = 17

def Doc2PDFConverter(inputFile):
    pythoncom.CoInitialize()
    abspath = os.getcwd()
    # abspath=abspath.replace("\\","/")
    filename = "\\SOW 230 Draft - AI sample 1"

    # in_file="C:\Enclave\Git projects\Text Analytics\CDAT Project doc\Text Extraction\SOW 230 Draft - AI sample 1.docx"
    # out_file="C:\Enclave\Git projects\Text Analytics\CDAT Project doc\Text Extraction\SOW 230 Draft"
    # out_file=out_file+".pdf"
    in_dir = "\\..\\Sample Files"
    out_dir = "\\..\\dumps"

    in_file = abspath + in_dir + filename + ".docx"
    in_file=inputFile
    head, tail = os.path.split(inputFile)
    filename=str(tail.split('.')[:-1][0])+".pdf"
    out_file = os.path.join(head,filename)
    print(in_file)
    print(out_file)

    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(in_file)

    doc.SaveAs(out_file, FileFormat=wdFormatPDF)

    return out_file


