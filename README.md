# TalkMakerToEpub

by 神楽坂らせん version 0.001 

トークメーカーのストーリー（エピソード）をEPUB化します。

今のところは、吹き出しとしてではなく、キャラの画像のわきに回り込みテキストでセリフを流し込む仕様です。

## 環境

開発＆試験環境は

* MacOS HighSierra 10.13.3
* Python 3.6.2
* beautifulsoup4

### あるといいもの

* Sigil

## インストールとか

beautifulsoupのインストールは
>$ pip install beautifulsoup4
でOK

## 使い方

>python TalkGet.py [URL] [File]

で指定したURLのトーク（エピソード）をEPUB用のxhtmlとして取得し、/Textフォルダに[File]として保存します。

URLを省略すると「もしも敬虔な女子高生が〈神は死んだ〉のニーチェ作『ツァラトゥストラ』を読んだなら」の表紙ページ（ https://talkmaker.com/works/e39da839e2d4cf3d1706b528d846e7ba.html ）を取得します。（Fileのデフォルトはtext01.xhtml)

作成されたxhtmlファイルをSigilのファイル->追加で追加すると、Epubファイル化することができます。画像ファイル等も自動的に読み込んでくれます（どちらかと言うとSigilが偉い）

### 現状の問題点
* トークメーカーのバグ（？）でルビの取得がうまく出来ていません。rtタグが微妙におかしい様子。
* 複数のストーリーの一括取得はまだ。できれば目次も生成したいけれど手付かず。


