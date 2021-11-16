import subprocess
import os
from extractTextFrom2colHTML import getTextFrom2HTML
from text_process import segmentation

pdfFolder = 'C:/Users/Jalen/Desktop/work/papers'

if pdfFolder[-1] == '/':
    pdfFolder = pdfFolder[:-1]
os.chdir(pdfFolder)
if not os.path.exists('../htmls'):
    os.mkdir('../htmls')
htmlFolder = os.path.dirname(pdfFolder) + '/htmls'
if not os.path.exists('../txts'):
    os.mkdir('../txts')
txtFolder = os.path.dirname(pdfFolder) + '/txts'
if not os.path.exists('../results'):
    os.mkdir('../results')
resultFolder = os.path.dirname(pdfFolder) + '/results'

subprocess.run('docker pull pdf2htmlex/pdf2htmlex:0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64', shell=True)
pdfs = os.listdir(pdfFolder)
for pdf in pdfs:
    if os.path.isfile(pdf):
        newName = pdf.replace(' ', '_').replace('-', '_')
        os.rename(pdf, newName)

        if not os.path.exists(htmlFolder + '/' + newName[:-4] + '.html'):
            subprocess.run('docker run -ti --rm ' + 
                    '--mount type=bind,source=' + pdfFolder + ',target=/pdf ' +
                    '--mount type=bind,source=' + htmlFolder + ',target=/htmloutput ' +
                    'pdf2htmlex/pdf2htmlex:0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64 --zoom 1.3 ' + newName + ' ../htmloutput/' + newName[:-4] + '.html', shell=True)
        
        # if not os.path.exists(txtFolder + '/' + newName[:-4] + '.txt'):
        #     try:
        #         print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        #         getTextFrom2HTML(htmlFolder + '/' + newName[:-4] + '.html', txtFolder + '/' + newName[:-4] + '.txt', auto='single')
        #     except FileNotFoundError:
        #         print('cccccccccccccccccccccccccccccccccccccccccccccccccccc')
        #         continue
        #     except:
        #         os.remove(htmlFolder + '/' + newName[:-4] + '.html')
        #         continue
        
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        if not os.path.exists(resultFolder + '/' + newName[:-4] + '.txt'):
            segmentation(txtFolder + '/' + newName[:-4] + '.txt', resultFolder + '/' + newName[:-4] + '.txt')