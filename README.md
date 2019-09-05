
これは、日経ソフトウエア2019年9月号特集「PythonでAIと対戦できるリバーシを作ろう データ構造とUI編
https://shop.nikkeibp.co.jp/front/commodity/0000/SW1244/
のコードを変更したものです。  

Python 3.7.4 on Mac で動作確認しています。  

pycodestyle reversi.py で linte チェックをしています。  

変更点の概要

その１
- global 変数をなくした。
- 0, 1 などを なるべく Enum に変更した。
- コンピュータの思考ルーチンを別ファイルに分離した。

その２
- 復数の AI をえらべるようにする準備
  
その３
- 人間の手番のときに、石を置ける場所を示すようにした。


参考情報
- https://blog.makotoishida.com/2019/03/reacttypescript-5.html
  React/TypeScriptでリバーシゲームを作る

- https://www.pytry3g.com/entry/Othello-v1.0
  tkinterを使ってオセロを作る v1.0

- https://app.lavox.net/kifubox/
  棋譜Boxは、Richard Delorme氏によるGPL v3ソフトウェアEdax4.4のソースコードを改変して使用しています。
  改変したソースコードはhttps://github.com/lavox/edax-reversi/releases/tag/libEdax4i-1.1にて入手可能です

- https://github.com/abulmo/edax-reversi
  Edax reversi version 4.4 and above

- http://el-ement.com/blog/2017/02/20/reversi-ai/
  PCやスマートフォンのブラウザ上で動くリバーシ（オセロ）AIを作りました。
  棋譜の読み込み・優劣のグラフ表示機能があるので対局の研究に使えます。

- https://mayumen.com/1419.html
  オセロの棋譜とは？棋譜を採るタイミングや棋譜を採る意味は？

- https://qiita.com/sensuikan1973/items/459b3e11d91f3cb37e43
  オセロをビットボードで実装する

