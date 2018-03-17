#-*- coding:utf-8 -*-

import urllib.request
import sys
import codecs

#改行コード
CR = chr(13)    #Mac

def download(url,fileName):

    urllib.request.urlretrieve(url,"{0}".format(fileName))

def rubyCng(url):
    download(url,'work.html')

    file = codecs.open('workout.txt' ,'w','utf-8')

    lineCount = 0
    for Line in codecs.open("work.html", "r",'utf-8'):
        lineCount += 1
        Line = Line.replace('<rp>(</rt>','<rp>(</rp>')
        Line = Line.replace('<rp>)</rt>','<rp>)</rp>')
        file.write(Line)

    file.close()
    
if __name__ == "__main__":

    #url = sys.argv[1]
    #fileName = sys.argv[2]

    #download(url,fileName)
    #download('https://talkmaker.com/works/episode/9c0c78769031cd6414543ee462d7d43e.html','test.html')
    rubyCng('https://talkmaker.com/works/episode/9c0c78769031cd6414543ee462d7d43e.html')

