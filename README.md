# TalkMakerToEpub

by 神楽坂らせん version 0.005

トークメーカーのストーリー（エピソード）をEPUB化します。

今のところは、吹き出しとしてではなく、キャラの画像のわきに回り込みテキストでセリフを流し込む仕様です。

## 環境

開発＆試験環境は

* MacOS HighSierra 10.13.3
* Python 3.6.2
    * Pythonのモジュール
    * beautifulsoup4
    * requests

### あるといいもの

* Sigil 0.9.7 以上

## インストールとか

Pythonは適当にいれてください。（Version 3.6以上）

beautifulsoupのインストールは

>$ pip install beautifulsoup4

でOK。
あ、requestsも入れないとおこられるかも。

>$ pip install requests

してあげてください。

## 使い方

>python TalkGet.py [URL] [File]

で指定したURLのトーク（エピソード）をEPUB用のxhtmlとして取得し、/Textフォルダに[File]として保存します。

URLを省略すると「もしも敬虔な女子高生が〈神は死んだ〉のニーチェ作『ツァラトゥストラ』を読んだなら」の表紙ページ（ https://talkmaker.com/works/e39da839e2d4cf3d1706b528d846e7ba.html ）を取得します。（Fileのデフォルトはtext01.xhtml)

作成されたxhtmlファイルをSigilのファイル->追加で追加すると、Epubファイル化することができます。画像ファイル等も自動的に読み込んでくれます（どちらかと言うとSigilが偉い）

>python allStorys.py [URL]

URLで指定した目次ページにある全ストーリーを一気にやります、text0001.xhtmlからの連番で取得。
URLを指定しないと、『もしトラ』の目次ページ（ https://talkmaker.com/works/e39da839e2d4cf3d1706b528d846e7ba.html ）からもってきます。
サーバーの負荷対策で各ストーリーごとに１５秒間停止します。（途中でキャンセルはそのタイミングでCTRL+Cしてください）

※　Version 0.005 にて、allStorys時に目次の自動生成も行えるようにしました。TEXT0000.xhtml として作品ページにかかれている目次と本の情報、登場人物紹介を取得します。別ページ化したい場合はSigil上で分割してください。

## ライセンス的なもの
	----
    ※これは非公式の勝手スクリプトであり、トークメーカーさまとは一切関係のないソフトウェアです。
    バグ等はトークメーカーさまではなく、神楽坂らせんの方へよろしくお願いします。
    ただし、あくまで本スクリプトは架空世界のトークメーカーっぽい作品をEpub化するものであり、架空はもちろん、
	現実世界でも完全に無保証です。現実世界のトーク作品を偶然Epub化できたとしても、それはおそらく偶然に、
	運良くできてしまったにすぎません。
    本スクリプトの利用でいかなる不利益・不具合が発生しても、当方は一切責任をもちません。
    また本スクリプト作成段階でのデフォルトで読み込まれるデータ以外での動作は一切検証されていません。
    あくまでご利用は自己責任で計画的に。
    これで作成できてしまったEpubファイルの利用・配布・販売等はご自由にどうぞ。
    （できれば、あとがきにでも一言ありますと嬉しいです）
    このスクリプト自体の改変・再配布もOKですが、このコメント文は残すようにしてください。
    by 神楽坂らせん　
    ----
# 既知の問題等
* 2018/03/31現在、SigilでEpub化を行っても、正しいEPUBファイルにはならず、電書チェッカーなどではエラーになるようです。AmazonKindle用のmobiファイルに変換はうまく出来ているので、現状はこの状態でリリースいたします。（修正大変そう＞＜）
* 著者情報、奥付情報は取得していません。
* 吹き出しの外枠についてはEpub上で再現していません。

# そのほかのドキュメントなど
* トークメーカーでの説明
	* https://talkmaker.com/works/37f020a91fa6c9ea8c38ed71c24bf237.html
* Wiki での説明
	* https://github.com/kagurazakarasen/TalkMakerToEpub/wiki
	* How To Use
		* https://github.com/kagurazakarasen/TalkMakerToEpub/wiki/HowToUse
