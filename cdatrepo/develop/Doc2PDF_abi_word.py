import os

def doc2Pdf(inputFile):
    try:
        print("inputFile: "+inputFile)
        inputFile=inputFile.replace("\\","/")
        command = "abiword --to=pdf " + "'" + inputFile + "'"

        #outputFile=''.join(inputFile.split('.')[:-1])+".pdf"

        head, tail = os.path.split(inputFile)
        filename = str(tail.split('.')[:-1][0]) + ".pdf"
        outputFile = os.path.join(head, filename)

        os.system(command)
    except Exception as error:
            print("subprocess exception,please continue")
    return outputFile

#\\home\\ubuntu\\cdat\\SOW- AI for. Benchmarking-Initial period_3.docx
# >>> import Doc2PDF_abi_word as doc
# >>> path='/home/ubuntu/cdat/SOW- AI for Benchmarking-Initial period_3.docx'
# >>> outpath=doc.doc2Pdf(path)