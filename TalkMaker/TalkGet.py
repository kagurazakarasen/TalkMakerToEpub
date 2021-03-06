# -*- coding:utf-8 -*-

"""
    トークメーカーのストーリーをEpubファイルにしちゃうやつ Ver0.21
    使い方：　python TalkGet.py [URL] [File]
    URLにあるトークメーカーのストーリーを取得してTextディレクトリにxhtmlページ(file)を作成します。
    自動的に画像も取得します。
    できたxhtmlファイルはSigilにつっこみ、表紙と目次等を追加すればEpub化できます。
    詳しくは：https://talkmaker.com/works/37f020a91fa6c9ea8c38ed71c24bf237.html 参照

    ※ 2018/03/31現在、SigilでEpub化を行っても、正しいEPUBファイルにはならず、電書チェッカーなどではエラーになるようです。
    　AmazonKindle用のmobiファイルに変換はうまく出来ているので、現状はこの状態でリリースいたします。（修正大変そう＞＜）

    ※ 2018/07/15修正：谷川求鹿さん作、鹿にっき https://talkmaker.com/works/a4e3ad39e1a98a43c31d873a207b8801.html
    　を元に、大幅な修正を行い、吹き出し＆背景色をいれられるモードを新設しました。
    　ソース内で ShikaMode = True にすることで実行できます

    ----
    ※これは非公式の勝手スクリプトであり、トークメーカーさまとは一切関係のないソフトウェアです。
    バグ等はトークメーカーさまではなく、神楽坂らせんの方へよろしくお願いします。
    ただし、あくまで本スクリプトは架空世界のトークメーカーっぽい作品をEpub化するものであり、架空はもちろん、現実世界でも完全に無保証です。
    現実世界のトーク作品を偶然Epub化できたとしても、それはおそらく偶然に、運良くできてしまったにすぎません。
    本スクリプトの利用でいかなる不利益・不具合が発生しても、当方は一切責任をもちません。
    また本スクリプト作成段階でのデフォルトで読み込まれるデータ以外での動作は一切検証されていません。
    あくまでご利用は自己責任で計画的に。
    これで作成できてしまったEpubファイルの利用・配布・販売等はご自由にどうぞ。
    （できれば、あとがきにでも一言ありますと嬉しいです）
    このスクリプト自体の改変・再配布もOKですが、このコメント文は残すようにしてください。
    by 神楽坂らせん　
    ----
"""

import random
import time
import requests, bs4
import urllib.request
import sys
import os
import codecs


#定数的ないろいろ
ShikaMode = False    #鹿にっきモード、Trueにすると吹き出しがONになります

CR = chr(13)    #改行コード

FUKIDASI_BR = False #キャラ画像脇のテキスト冒頭に改行を入れるかどうか
CHARA_SIZE = '30%'  #キャラクタ画像サイズ。％かpxで指定します。


xhtml_head = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
<meta charset="UTF-8"/>
<link href="../Styles/styles_epub.css" rel="stylesheet" type="text/css" media="all"/>
"""


def TalkGet(url,saveTextFile):
    """ トークメーカーのストーリー部分(url)を、Text/ (saveTextFile) にHTML形式で保存する """

    rubyCng(url) # urlからDLした内容のルビを置換、結果はworkout.datに入る

    #res = requests.get(url)
    #res.raise_for_status()
    #soup = bs4.BeautifulSoup(res.text, "html.parser")

    dummyFile = codecs.open('workout.dat' ,'r','utf-8')
    soup = bs4.BeautifulSoup(dummyFile, "html.parser")
    dummyFile.close()
    print(soup.title)

    tt = soup.h3
    print(tt.text)

    file = codecs.open('Text/' + saveTextFile ,'w','utf-8')

    #file.write('<?xml version="1.0" encoding="utf-8"?>'+CR)
    #file.write("<!DOCTYPE html>"+CR+CR)
    #file.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" xmlns:epub="http://www.idpf.org/2007/ops">'+CR)
    #file.write("<head>"+CR)
    #file.write('<meta charset="UTF-8"/>'+CR)
    #file.write('<link href="../Styles/styles_epub.css" rel="stylesheet" type="text/css" media="all"/>'+CR)

    file.writelines(xhtml_head)

    file.write("<title>")
    #file.writelines(soup.title)
    file.writelines(tt.text)
    file.write("</title>"+CR)
    file.write("<body>"+CR)

    strg=str(tt)
    file.write(strg+CR)

    file.write('<HR/>'+CR)

    #m30div = soup.find_all("div", class_="m30")
    #print(m30div[1])    # すべての発言

    #mt30 = soup.find_all("div", class_="mt30")
    FukiPos=""
    i=0
    for div in soup.select(".mt30"):
        i=i+1
        f = div.find("div",class_="fLeft")        # ここがnoneならば吹き出しではない
        #print(range(len(s)),s)
        if f:   #fLeftがある＝吹き出しである
            if str(f).find('class="fLeft">')>0:
                print("LEFT balloon:",str(f).find('class="fLeft">'))
                imgSrc=f.find("img")['src']
                print("IMGソース：",imgSrc)
                imgFileGet(imgSrc)
                if ShikaMode:
                    print('鹿モード')
                    FukiPos="fukiR"
                    strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconL" />'+CR
                else:
                    strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconL" width="'+ CHARA_SIZE +'"/>'+CR
                print(strg)
                file.write(strg)
                ff = div.find("div",class_="fRight")
                #print('ff=',ff)
                if ShikaMode:
                    ffs= str(ff).find('balloonColor')+len('balloonColor')
                    #print('ffs=',ffs)
                    ffss= str(ff)[ffs:ffs+2]
                    if ffss[-1]=='"':
                        ffss = ffss[0]
                    #print('fC=',ffss)

            else:
                print("RIGHT balloon:")
                r= div.find("div",class_="fRight")
                #print("IMGソース：",end='')
                imgSrc=r.find("img")['src']
                print("IMGソース：",imgSrc)
                imgFileGet(imgSrc)
                if ShikaMode == True:
                    print('鹿モード')
                    FukiPos="fukiL"
                    strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconR" />'+CR
                else:
                    strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconR" width="'+ CHARA_SIZE +'"/>'+CR
                print(strg)
                file.write(strg)
                ff = div.find("div",class_="fLeft")
                if ShikaMode:
                    ffs= str(ff).find('balloonColor')+len('balloonColor')
                    #print('ffs=',ffs)
                    ffss= str(ff)[ffs:ffs+2]
                    if ffss[-1]=='"':
                        ffss = ffss[0]
                    #print('fC=',ffss)

            fff = ff.find("div")
            if ShikaMode:
                #print('鹿モード')
                fff=str(fff).replace("div",'div class="'+FukiPos+' fC'+ffss+'"',1)
            print('fff=',fff)
            if FUKIDASI_BR:
                strg='<BR>'
            else:
                strg=''
            strg= strg +str(fff)+CR # 吹き出しの冒頭改行いれ
            file.write(strg)
            file.write('<p class="iconClear"><BR> </p>'+CR)
            #print("吹き出し＞＞＞",f)
        else:
            #吹き出しではない
            print("＃吹き出しではない")
            imglazy = div.find("img",class_="lazy")
            imgon = div.find("img",class_="op_no")
            if imglazy and not imgon:
                print('大型イメージタグ:',end='')
                print(imglazy)
                #print(imglazy['src'])
                imgFileGet(imglazy['src'])
                #固定画像の横幅は３段階から指定
                print(imglazy['width'])
                if imglazy['width'] == '640':
                    Wid = '100%'
                elif imglazy['width'] == '480':
                    Wid = '70%'
                else:
                    Wid = '50%'
                strg='<div class="img_Center"><img src="../Images/' + os.path.basename(imglazy['src']) +'" width="'+ Wid + '"></div>'+CR
                print(strg)
                file.write(strg)

            s = div.find("div")
            #print(range(len(s)),s)
            strg = str(s)+CR
            if strg.find('id="main_img"')>0:
                break
            ss = strg.find('class="balloon type2 ')
            if(ss > 0):
                print("＃アイコンなし：特殊処理")
                if ShikaMode:
                    ffs= strg.find('balloonColor')+len('balloonColor')
                    #print('ffs=',ffs)
                    ffss= strg[ffs:ffs+2]
                    if ffss[-1]=='"':
                        ffss = ffss[0]
                    #print('fC=',ffss)
                sss = strg.find('<div class="r mt10 f72">')
                strg = strg[:sss] + CR
                if ShikaMode:
                    #print('鹿モード')
                    strg=strg.replace("div",'div class="'+FukiPos+' fC'+ffss+'"',1)

            print("ベタ書き：",s)
            file.write(strg)
            if ShikaMode:
                file.write('</div> <p class="iconClear"><BR> </p>'+CR)
            else:
                file.write('<p><br></p>')
        #print('>>>',i)
        #if i>10: break

    file.write("</BODY></HTML>"+CR)

    file.close()

    #後始末
    if os.path.isfile('workout.dat'):
        os.remove('workout.dat')
    if os.path.isfile('work.dat'):
        os.remove('work.dat')


# ルビのバグ対策
def rubyCng(url):
    #download(url,'work.html')
    urllib.request.urlretrieve(url,"{0}".format('work.dat'))
    file = codecs.open('workout.dat' ,'w','utf-8')

    lineCount = 0
    for Line in codecs.open("work.dat", "r",'utf-8'):
        lineCount += 1
        Line = Line.replace('<rp>(</rt>','<rp>(</rp>')
        Line = Line.replace('<rp>)</rt>','<rp>)</rp>')
        file.write(Line)

    file.close()


#必要なディレクトリを作成
def setDir():
    # print(os.getcwd()) #現在のディレクトリ
    if not os.path.isdir('Images'):
        os.mkdir('Images')
    if not os.path.isdir('Text'):
        os.mkdir('Text')
    if not os.path.isdir('Styles'):
        os.mkdir('Styles')

#イメージファイル取得
def imgFileGet(url):
    fn = os.path.basename(url)
    #Imagesディレクトリにすでに保存されているか確認し、なければダウンロードする
    #ディレクトリの/はMac以外では¥¥じゃなきゃダメかも？
    if not os.path.exists('Images/'+fn):
        urllib.request.urlretrieve(url,'Images/'+fn)

#メインルーチン
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    setDir()
    print(argc)
    if(argc < 2):
        #指定なければもしトラ表紙ページを取得URL
        #print('argc<2')
        TalkGet('https://talkmaker.com/works/episode/9880b1ccec9b22606e7b31e29027fafa.html','text01.xhtml')
    elif(argc < 3):
        #指定が一つのみ（URLだけ）の場合
        if(argvs[1].find("episode")>0):
            TalkGet(argvs[1],'text01.xhtml')
        else:
            print("読み込みエラー：",argvs[1],"はエピソードURLでは無いようです")
    else:
        #argcが２以上なら、指定URLを指定fileに保存
        if(argvs[1].find("episode")>0):
            TalkGet(argvs[1],argvs[2])
        else:
            print("読み込みエラー：",argvs[1],"はエピソードURLでは無いようです")
