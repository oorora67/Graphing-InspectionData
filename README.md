# Graphing-InspectionData
検査データのグラフ化  
## 環境
### 開発言語
- Python 3.7.0
> 公式サイト(https://www.python.org/)  
### 利用ライブラリ
- matplotlib  
> 公式サイト(https://matplotlib.org/)  
> インストール方法`pip install matplotlib`または`pip3 install matplotlib`(Pythonの環境によって変わる)をターミナルで実行する  
## 検証環境
### macOS
- HW:MacBook Pro (13-inch,2017)
- OS:macOS Mojave Ver 10.14.5  
- CPU: Intel Core i5 2.3GHz  
- RAM:8GB (2133MHz LPDDR3)  
- Python 3.7.0  
### Linux
- OS:Ubuntu 16.04.4 LTS (MATE 1.12.1)  
- CPU Intel Xeon E5-2697 v2 2.7GHz  
- RAM:64GB  
- Python 3.5.2  
### Windows
- 未検証  
## 利用方法
### デフォルト設定で利用する
- Dataフォルダ内に検査データ(.dlk)ファイルを入れる(※データを入れすぎるとメモリが足りなくなる可能性がある【未検証】)  
- ターミナルを開きData2Graph.pyのあるフォルダまで移動する  
- ターミナルで`python3 Data2Graph.py`または`python Data2Graph.py`(Pythonの環境によって変わる)を実行する  
- 処理が完了するとData2Graph.pyのあるフォルダ内にGraphというフォルダが作成されその中にグラフが出力される  
### カスタム設定で利用する
- カスタム設定を利用する場合ターミナルで`python3 Data2Graph.py <オプション>`または`python Data2Graph.py <オプション>`  
- 例)`python3 Data2Graph.py -i ./SampleData -o ./SampleGraph -c 10000 -s 1 -e 10`

| オプション | 機能 |  
|:----:|----|  
| `-i` | 検査データのパス(指定なしで直下のDataフォルダ内のデータを使用) 例)./Data |  
| `-o` | グラフの保存場所のパス(指定なしで直下のGraphというディレクトリに出力する フォルダがなければ作成する) 例)./Graph |  
| `-c` | データ何個でグラフを区切るか(指定なしでデータすべてを一つのグラフとして出力) 例)1000 |  
| `-s` | グラフ化する検査データ範囲の先頭(-s,-e指定なしで全検査データをグラフ化する)(-eの指定なしで指定した検査データだけをグラフ化) 例)1 |  
| `-e` | グラフ化する検査データ範囲の末尾(-sの指定なしで指定した検査データだけをグラフ化)(-sよりも値が小さいときは-sの値と交換する) 例)10 |  

【注意】パスを指定する場合は最後のスラッシュを消さなければならない。例)`./Data/`ではなく`./Data`とする必要がある  