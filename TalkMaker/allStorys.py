# -*- coding:utf-8 -*-

from TalkGet import *

import sys
import os
from time import sleep

"""
全ストーリーまるっとゲットしちゃうやつ
"""



def tocGet(url):
    """ 目次を取得 """
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    print(soup.title)

    tt = soup.h3
    print(tt.text)

    tocSrc = soup.find("ul",class_="episode")
    #print(tocSrc)
    storyNo=0
    for a in tocSrc.select('li > a'):
        txt=str(a.text)
        st=txt.find("更新日")
        txt2=txt[:st]
        print(txt2)
        b=a['href']
        if b:
            storyNo = storyNo + 1
            print(b)
            storyUrl = 'https://talkmaker.com'+str(b)
            TalkGet(storyUrl,'text'+'{0:04d}'.format(storyNo) +'.xhtml')
            print("ーーーーー５秒間停止中ーーーーーー")
            sleep(5) #５秒スリープ
    print("ーーーーー　終了　ーーーーーー")



if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    setDir()
    print(argc)
    if(argc != 2):
        #指定なければもしトラ全取得URL
        tocGet('https://talkmaker.com/works/e39da839e2d4cf3d1706b528d846e7ba.html')
        
    else:
        #argcが２以上なら、指定URL
        tocGet(argvs[1])
#print('モジュール名：{}'.format(__name__))  #実行したモジュール名を表示する