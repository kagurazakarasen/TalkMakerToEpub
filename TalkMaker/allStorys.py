# -*- coding:utf-8 -*-

"""
    全ストーリーをまるっとゲットしちゃうやつ

    使い方：　python allStorys.py [URL] [No]

    URLに目次ページがあるトークメーカーの全ストーリーを取得します。内部で TalkGet.py スクリプトを呼び出しています。
    [No]は目次の起点No（＋１＝連番の開始No（目次デフォルトは text0000.xhtml)
    ----
    ※これは非公式の勝手スクリプトであり、トークメーカーさまとは一切関係のないソフトウェアです。
    バグ等はトークメーカーさまではなく、神楽坂らせんの方へよろしくお願いします。
    ただし、あくまで本スクリプトは架空世界のトークメーカーっぽい作品をEpub化するものであり、架空はもちろん、現実世界でも完全に無保証です。現実世界のトーク作品を偶然Epub化できたとしても、それはおそらく偶然に、運良くできてしまったにすぎません。
    本スクリプトの利用でいかなる不利益・不具合が発生しても、当方は一切責任をもちません。
    また本スクリプト作成段階でのデフォルトで読み込まれるデータ以外での動作は一切検証されていません。
    あくまでご利用は自己責任で計画的に。
    これで作成できてしまったEpubファイルの利用・配布・販売等はご自由にどうぞ。
    （できれば、あとがきにでも一言ありますと嬉しいです）
    このスクリプト自体の改変・再配布もOKですが、このコメント文は残すようにしてください。
    by 神楽坂らせん　
    ----
"""

#定数的なモノ
WAIT_SEC = 5    #強制ウェイトタイム
TOC_HTML = 'TEXT0000.xhtml'
TOC_NO = 0
HYOSHI_IMG_SIZE = '300px'
MOKUJI_CHARA_SIZE = '30%'



from TalkGet import *

import sys
import os
from time import sleep


def tocGet(url,tn):
    """ 目次を取得 ※tnはTOCの開始番号、通常のページはtn+1から連番"""
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    print(soup.title)

    
    toc_t = 'text'+'{0:04d}'.format(tn) +'.xhtml'
    t_file = codecs.open('Text/' + toc_t ,'w','utf-8')
    t_file.writelines(xhtml_head)

    tt = soup.h3
    tf_str="<title>"+ tt.text+ "</title>"+CR+"<body>"+CR 
    t_file.write(tf_str)

    tf_str="<h2>"+ tt.text+ "</h2>"+CR #タイトル
    print(tf_str)
    t_file.write(tf_str)

    cell = soup.find_all("div",class_="cell")

    tf_str="<h3>"+cell[1].a.text+"</h3>"+CR   #著者名
    print(tf_str)
    t_file.write(tf_str)

    icon_img = cell[0].img.get("src")   #表紙アイコン
    print(icon_img)
    imgFileGet(icon_img)
    strg = '<img src="../Images/' + os.path.basename(icon_img) +'" width="'+ HYOSHI_IMG_SIZE +'"/>'+CR
    print(strg)
    t_file.write(strg)

    #説明文
    p15 = soup.find("p",class_="mt15")
    print(p15)
    tf_str=str(p15)+CR
    t_file.write(tf_str)

    t_file.write("<hr>"+CR)
    t_file.write("<p> <br> </p>")
    t_file.write("<h2>もくじ</h2>"+CR)

    t_file.write("<ul>"+CR)

    #エピソード取得
    tocSrc = soup.find("ul",class_="episode")
    #print(tocSrc)
    storyNo=tn
    for a in tocSrc.select('li > a'):
        txt=str(a.text)
        st=txt.find("更新日")  #更新日以下の情報はカット
        txt2=txt[:st]
        print(txt2) #ストーリータイトル
        b=a['href']
        if b:
            storyNo = storyNo + 1
            print(b)
            xhtml_file = 'text'+'{0:04d}'.format(storyNo) +'.xhtml'
            storyUrl = 'https://talkmaker.com'+str(b)
            
            print(txt2,"-->",xhtml_file)

            tf_str='<li><a href="../Text/'+ xhtml_file + '">'+ txt2+ '</a></li>'+CR
            print(tf_str)
            t_file.write(tf_str)

            TalkGet(storyUrl,'text'+'{0:04d}'.format(storyNo) +'.xhtml')
            print("ーーーーー",WAIT_SEC,"秒間停止中ーーーーーー")
            sleep(WAIT_SEC) #スリープ


    t_file.write("</ul>"+CR)
    t_file.write("<hr>"+CR)

    t_file.write("<h3>登場人物紹介</h3>"+CR)
    
    ch = soup.find("div",class_="join list m15")

    s2 = bs4.BeautifulSoup(str(ch), "html.parser")

    chf= s2.find_all("div",class_="clear type1 mt30")

    for i in range(len(chf)):
        print(i,end='')
        s3 = bs4.BeautifulSoup(str(chf[i]), "html.parser")
        ss = s3.find("div",class_="fLeft")
        sss = ss.find("img")['src']
        print("イメージソース：",sss)
        imgFileGet(sss)

        ss = s3.find("div",class_="fRight")
        ssp = ss.find("p")
        print("P：",ssp)

        strg = '<img src="../Images/' + os.path.basename(sss) +'" class="iconL" width="'+ MOKUJI_CHARA_SIZE +'"/>'+CR

        print(strg)
        t_file.write(strg)

        t_file.writelines(str(ssp))

        t_file.write('<p class="iconClear"><BR> </p>'+CR)


    print("ーーーーー　終了　ーーーーーー")

    t_file.write("</body></html>"+CR)


    t_file.close()



#メインルーチン
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    setDir()
    print(argc)
    if(argc < 2):
        #指定なければもしトラ全取得URL
        tocGet('https://talkmaker.com/works/e39da839e2d4cf3d1706b528d846e7ba.html',0)
    elif(argc < 3):
        #指定が一つのみ（URLだけ）の場合
        print("指定URLのみ")
        tocGet(argvs[1],0)
    else:
        #argcが２以上なら、指定URL+指定No
        print("指定U+No")
        tocGet(argvs[1],int(argvs[2]))
        

