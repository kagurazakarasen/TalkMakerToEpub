# -*- coding:utf-8 -*-

"""
    使い方：　python TalkGet.py [URL] [File]
    URLにあるトークメーカーのストーリーを取得してTextディレクトリにxhtmlページ(file)を作成します。
    自動的に画像も取得します。
    できたxhtmlファイルはSigilにつっこみ、表紙と目次等を追加すればEpub化できます。
    今のところは吹き出し枠表示と背景色はナシです。
    ----
    by 神楽坂らせん　
    ※もちろんですが、完全に無保証です。
    本スクリプト作成段階でのトークメーカーのデータ以外での動作は一切検証されていません。
    あくまでご利用は自己責任で計画的に。
    これで作成したEpubファイルの利用・配布・販売等はご自由にどうぞ。
    （できれば、あとがきにでも一言ありますと嬉しいです）
    このスクリプト自体の改変・再配布もOKですが、このコメント文は残すようにしてください。
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
CR = chr(13)    #改行コード

FUKIDASI_BR = False #キャラ画像脇のテキスト冒頭に改行を入れるかどうか
CHARA_SIZE = '30%'  #キャラクタ画像サイズ。％かpxで指定します。


def TalkGet(url,saveTextFile):
    """ トークメーカーのストーリー部分(url)を、Text/ (saveTextFile) にHTML形式で保存する """

    rubyCng(url) # urlからDLした内容のルビを置換、結果はworkout.datに入る

    #res = requests.get(url)
    #res.raise_for_status()
    #soup = bs4.BeautifulSoup(res.text, "html.parser")

    dummyFile = codecs.open('workout.dat' ,'r','utf-8')
    soup = bs4.BeautifulSoup(dummyFile, "html.parser")
    print(soup.title)

    tt = soup.h3
    print(tt.text)

    file = codecs.open('Text/' + saveTextFile ,'w','utf-8')

    """
    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE html>

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" xmlns:epub="http://www.idpf.org/2007/ops">
    <head>
    <meta charset="UTF-8"/>
    <link href="../Styles/styles_epub_reset.css" rel="stylesheet" type="text/css"/>
    <link href="../Styles/styles_epub_ltr.css" rel="stylesheet" type="text/css" media="all"/>
    <title>てすとのほん</title>
    """
    file.write('<?xml version="1.0" encoding="utf-8"?>'+CR)
    file.write("<!DOCTYPE html>"+CR+CR)
    file.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" xmlns:epub="http://www.idpf.org/2007/ops">'+CR)
    file.write("<head>"+CR)
    file.write('<meta charset="UTF-8"/>'+CR)
    file.write('<link href="../Styles/styles_epub.css" rel="stylesheet" type="text/css" media="all"/>'+CR)

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
                strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconL" width="'+ CHARA_SIZE +'"/>'+CR
                print(strg)
                file.write(strg)
                ff = div.find("div",class_="fRight")

            else:
                print("RIGHT balloon:")
                r= div.find("div",class_="fRight")
                #print("IMGソース：",end='')
                imgSrc=r.find("img")['src']
                print("IMGソース：",imgSrc)
                imgFileGet(imgSrc)
                strg = '<img src="../Images/' + os.path.basename(imgSrc) +'" class="iconR" width="'+ CHARA_SIZE +'"/>'+CR
                print(strg)
                file.write(strg)
                ff = div.find("div",class_="fLeft")
            fff = ff.find("div")
            print(fff)
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
            imglazy = div.find("img",class_="lazy")
            imgon = div.find("img",class_="op_no")
            if imglazy and not imgon:
                print('大型イメージタグ:',end='')
                print(imglazy)
                #print(imglazy['src'])
                imgFileGet(imglazy['src'])
                #print(os.path.basename(imglazy['src']))
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
            print("ベタ書き：",s)
            file.write(strg)
            file.write('<p><br></p>')
        print('>>>',i)
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

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    setDir()
    print(argc)
    if(argc < 2):
        #指定なければもしトラ表紙ページを取得URL
        TalkGet('https://talkmaker.com/works/episode/9880b1ccec9b22606e7b31e29027fafa.html','text01.xhtml')
        
    else:
        #argcが２以上なら、指定URLを指定fileに保存(今のところ１つだけ)
        TalkGet(argvs[1],argvs[2])
        

#print('モジュール名：{}'.format(__name__))  #実行したモジュール名を表示する