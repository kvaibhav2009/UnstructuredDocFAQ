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

    #in_file = abspath + in_dir + filename + ".docx"
    # if(str(inputFile.split('.')[-1])=='doc'):
    #     inputFile=doc2docx(inputFile)


    in_file=inputFile


    print("INPUT_file "+in_file)
    head, tail = os.path.split(inputFile)
    filename=str(tail.split('.')[:-1][0])+".pdf"
    out_file = os.path.join(head,filename)
    #out_file=filename
    print("InputFilename in converter "+in_file)
    print("OutputFilename in converter "+out_file)
    print("Converter path "+os.getcwd()+"\\"+in_file)
    word = comtypes.client.CreateObject('Word.Application')
    #word = win32com.client.Dispatch('Word.Application')
    InputAbspath=in_file    #os.getcwd()+"\\"+in_file
    #######
    doc = word.Documents.Open(InputAbspath)
    OutputAbspath=out_file#os.getcwd()+"\\"+out_file
    doc.SaveAs(OutputAbspath, FileFormat=wdFormatPDF)
    print("Type "+str(type(doc)))
    doc.Close()
    #######
    word.Quit()
    print("Conversion completed")
    return out_file

#Doc2PDFConverter("C:\Enclave\Git projects\Text Analytics\CDAT_Flask\AI Sample amount conflict.docx")


def doc2docx(inputFile):
    pythoncom.CoInitialize()
    print("Converting doc to docx "+str(inputFile))
    head, tail = os.path.split(inputFile)
    filename = str(tail.split('.')[:-1][0]) + ".docx"
    out_file = os.path.join(head, filename)

    print("Docx path " + str(out_file))
    word = comtypes.client.CreateObject('Word.Application')
    wb = word.Documents.Open(inputFile)
    wb.SaveAs2(out_file, FileFormat=16)
    wb.Close()
    word.Quit()

    return out_file