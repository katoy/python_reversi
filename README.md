
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