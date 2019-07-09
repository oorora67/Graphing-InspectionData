#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse     #コマンドラインオプション、引数、サブコマンドを利用できるようにするライブラリ(オプション機能に使用)
import sys      #システムパラメータと関数を利用できるようにするライブラリ(ターミナルの表示、入力に使用)
import os       #雑多なオペレーティングシステムインタフェース(ファイルの操作に利用)
import glob     #Unix 形式のパス名のパターン展開を行うライブラリ(計測データファイルの列挙に使用)
import math     #数学関数を利用できるようにするライブラリ(グラフの分割数を計算するのに使用)
import time     #時刻データへのアクセスと変換をできるようにするライブラリ(処理にかかった時間を計測するために使用)
import gc       #ガベージコレクタインターフェース(メモリの開放に利用)
import matplotlib.pyplot as plt     #様々なグラフを描画するライブラリ(グラフを作成するのに利用)

'''
引数の定義
-i 検査データのパス(指定なしで直下のDataフォルダ内のデータを使用)
-c データ何個でグラフを区切るか(指定なしでデータすべてを一つのグラフとして出力)
-o グラフの保存場所のパス(パスに指定されたディレクトリがなければ作成する　指定なしで直下にGraphというディレクトリを作成してそこにグラフを出力する)
-s グラフ化する検査データ範囲の先頭(指定なしで全検査データをグラフ化する)(-eの指定なしで指定した検査データだけをグラフ化)
-e グラフ化する検査データ範囲の末尾(-sの指定なしで指定した検査データだけをグラフ化)
'''
def get_args():     #オプションの設定
    psr = argparse.ArgumentParser()
    psr.add_argument('-i', '--input', help='Specify the path of data to be processed (if not specified, use the data in the Data folder directly below)')
    psr.add_argument('-o', '--output', help='Save path of graph (If not specified, create a folder named Graph immediately below and output it there)')
    psr.add_argument('-c', '--cut', help='Number of data included in one graph (If not specified, all data will be output in one graph)')
    psr.add_argument('-s', '--start', help='Specify the beginning of the range of inspection items to graph (If the `-e` option is not specified, output only the specified inspection items to the graph)')
    psr.add_argument('-e', '--end', help='Specify the end of the range of inspection items to graph')

    return psr.parse_args()

if __name__ == '__main__':
    start = time.time()
    #オプションの処理
    args = get_args()
    Option_Data = {}
    Option_Data.update({'input':'./Data','output':'./Graph','cut':int('0'),'start':int('1'),'end':int('2')})
    #ファイル読み込み
    if(args.input is not None):
        Option_Data['input'] = args.input
    file_list = sorted(glob.glob(Option_Data['input']+'/*.dlk'))        #検査データを列挙しリスト化
    #print(file_list)
    data_all=[]
    data_set=[]
    InspectionItem_Data = []
    IID_F = 0
    fileload_s = time.time()
    for filename in file_list:      #列挙した検査データの読み込み
        #print(filename)
        data_temp=[]
        with open(filename, "r") as f:  #検査データの読み込み
            data = f.readlines()
            counttest = 0
            label_No = 0
            for data_all in data:       #データの整形　リスト化
                #print(data)
                data_del = data_all.split("\n")     #改行コードの削除
                data_del = data_del[0].split(",")       #カンマで検査データの分割
                #print(data_del)
                if len(data_del) == 8 :     #８分割されたか確認
                    if IID_F == 0:
                        InspectionItem_Data.append([str(data_del[2]),str(data_del[4]),float(data_del[5]),float(data_del[6])])   #各検査項目の名前などをリスト化して保存
                    data_temp.append(float(data_del[3]))        #計測データだけをリストに追加
                elif data_del[0] == 'D':        #計測データの区切りをリストに追加
                    label_No = label_No + 1
                    data_temp.append(str(data_del))
                    if IID_F == 0 and label_No >= 2:
                        IID_F = 1
                #data_del.clear
                counttest = counttest + 1
                sys.stdout.write('\rLOAD_File:'+os.path.basename(filename)+'  Read:'+str(counttest)+'/'+str(len(data)))     #読み出し中の行を表示
                sys.stdout.flush()
        data_set.extend(data_temp)      #整形したデータをデータセットに追加
        print(' *Complete...')
    del data_del        #変数の削除
    del data_all
    del data
    del f
    del data_temp
    gc.collect()        #メモリの開放
    FileLoadTime = time.time() - fileload_s
    print('*'+str(len(file_list))+'Files Load Complete  TIME:{0}'.format(FileLoadTime)+'[sec]')     #ファイルの読み込みにかかった時間を計算

    #グラフの出力先の設定
    if(args.output is not None):
        Option_Data['output'] = args.output
    Save_Path=Option_Data['output']
    os.makedirs(Save_Path, exist_ok=True)
    #一つのグラフに検査データを何個表示するか
    if(args.cut is not None):
        Option_Data['cut'] = int(args.cut)
    #どの検査項目をグラフ化するか(検査データの書いてある順番で処理を行う)
    if(args.start is not None):
        Option_Data['start'] = min(int(args.start),int(args.end))
        if args.end is None:
            Option_Data['end'] = int(args.start)
    if(args.end is not None):
        Option_Data['end'] = max(int(args.start),int(args.end))
        if args.start is None:
            Option_Data['start'] = int(args.end)
    if args.start is None and args.end is None:
        Option_Data['start'] = 1
        Option_Data['end'] = len(InspectionItem_Data)

    #グラフ処理
    for plot_label in range(Option_Data['start'],Option_Data['end'] + 1):
        output_time = time.time()
        label_No = 0
        DataNo = 0
        DataListY = []
        DataListX = []
        DataListEX = []
        DataListEY = []
        DataSE = []
        for data in data_set:
            data_in = data
            if  isinstance(data_in,float):
                label_No = label_No + 1
                if label_No == plot_label :
                    DataListY.append(data)
                    DataListX.append(DataNo)

            elif isinstance(data_in, str):
                DataNo = DataNo + 1
                #print('個体　製造ロット: No:'+str(DataNo))
                label_No = 0
        # Figureを設定
        if(args.cut is None):
            Option_Data['cut'] = len(DataListY)
        Data_count = Option_Data['cut']
        Loop_count = math.ceil(len(DataListY)/Data_count)
        DataMaxValue = InspectionItem_Data[plot_label-1][3]
        DataMinValue = InspectionItem_Data[plot_label-1][2]
        TestName = InspectionItem_Data[plot_label-1][0]
        TestUnit = InspectionItem_Data[plot_label-1][1]
        DataMax = [DataMaxValue,DataMaxValue]
        DataMin = [DataMinValue,DataMinValue]
        os.makedirs(Save_Path+'/'+str(plot_label)+'_'+TestName+'_'+TestUnit+'/', exist_ok=True)
        for i in range(0, Loop_count):
            point = i * Data_count
            PlotListY = DataListY[point:point + Data_count]
            PlotListX = DataListX[point:point + Data_count]
            #print(TestListY)
            fig = plt.figure(figsize=(15, 8), dpi=100)
            ax = fig.add_subplot(1,1,1)
            ax.set_title(TestName, fontsize = 16)
            ax.set_xlabel("Count", size = 14, weight = "light")
            ax.set_ylabel(TestUnit, size = 14, weight = "light")
            StandardWidth = (DataMaxValue - DataMinValue)*0.05
            ax.set_ylim(DataMinValue - StandardWidth,DataMaxValue + StandardWidth)
            ax.set_xlim(point,point + Data_count)
            DataSE = [point,point + Data_count]
            ax.plot(PlotListX,PlotListY,label="Data")
            ax.plot(DataSE,DataMax,color='red',label="Max")
            ax.plot(DataSE,DataMin,color='blue',label="Min")
            ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=10)
            outputfilename = Save_Path+'/'+str(plot_label)+'_'+TestName+'_'+TestUnit+'/'+str(point)+'-'+str(point+Data_count)+'.png'
            print("Output_File:",outputfilename)
            plt.savefig(outputfilename)
            plt.close()

        del DataListY
        del DataListX
        del PlotListY
        del PlotListX
        del DataListEX
        del DataListEY
        del DataMax
        del DataMin
        del DataSE
        gc.collect()
        output_time = time.time() - output_time
        print ("time:{0}".format(output_time) + "[sec]")
    elapsed_time = time.time() - start
    print ("Total Processing Time:{0}".format(elapsed_time) + "[sec]")