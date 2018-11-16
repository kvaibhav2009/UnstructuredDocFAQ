from subprocess import Popen, PIPE
import time

def convert(src, dst):
    d = {'src': src, 'dst': dst}
    commands = [
        '/usr/bin/docsplit pdf --output %(dst)s %(src)s' % d,
        'oowriter --headless -convert-to pdf:writer_pdf_Export %(dst)s %(src)s' % d,
    ]
    print("Path "+dst)
    for i in range(len(commands)):
        print("hell")
        command = commands[i]
        print("hell2")
        st = time.time()
        print(str(st))
        process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True) # I am aware of consequences of using `shell=True`
        out, err = process.communicate()
        print("communicated")
        errcode = process.returncode
        print(str(errcode))
        if errcode != 0:
            raise Exception(err)
        en = time.time() - st
        print 'Command %s: Completed in %s seconds' % (str(i+1), str(round(en, 2)))

if __name__ == '__main__':
    src = 'C:/Enclave/Git projects/Text Analytics/CDAT_Flask/Input Documents/Benchmarking -  AI sample 1.docx'
    dst = 'C:/Enclave/Git projects/Text Analytics/CDAT_Flask/OutputFile/'
    convert(src, dst)