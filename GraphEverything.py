import sys
import os
import glob
import matplotlib.pyplot as plt
args = sys.argv
plot_label = int(args[1])
os.makedirs('AllData', exist_ok=True)
file_list = sorted(glob.glob('*.dlk'))
while(plot_label>=1):
    label_No = 0
    DataNo = 0
    ercunt = 0
    E_Label = ''
    DataListY = []
    DataListX = []
    DataListEX = []
    DataListEY = []
    DataSE = []
    for file in file_list:
        lot, ext = os.path.splitext(file)
        if ext == '.dlk':
            test_data = open(file, "r")
            lines = test_data.readlines()
            print('file:{},ext:{}'.format(lot,ext))
            for line in lines:
                data = line.split("\n")
                data = data[0].split(",")
                if len(data) == 8:
                    label_No = label_No + 1
                    #print(data)
                    if label_No == plot_label :
                        TestName = data[2]
                        TestUnit = data[4]
                        DataMaxValue = float(data[6])
                        DataMinValue = float(data[5])
                        DataListY.append(float(data[3]))
                        DataListX.append(DataNo)
                        if data[1] != 'P':
                            print("ERROR")
                            E_Label='_E'
                            plt.plot(DataNo,float(data[3]),marker="o",color='yellow')
                            #DataListEY.append(float(data[3]))
                            #DataListEX.append(DataNo)
                            #sys.exit()
                            ercunt = ercunt + 1

                elif data[0] == 'D':
                    DataNo = DataNo + 1
                    #print('個体　製造ロット:'+lot+' No:'+str(DataNo))
                    label_No = 0
                    #sys.exit()
                #elif data[0] == 'R':
                    #print("計測項目数:",label_No)
            test_data.close()
    # Figureを設定
    fig = plt.figure(figsize=(15, 8), dpi=100)

    # Axesを追加
    ax = fig.add_subplot(111)
    ax.set_title(TestName, fontsize = 16)
    ax.set_xlabel("Count", size = 14, weight = "light")
    ax.set_ylabel(TestUnit, size = 14, weight = "light")
    DataMax = [DataMaxValue,DataMaxValue]
    DataMin = [DataMinValue,DataMinValue]
    DataSE = [0,DataNo]
    ax.plot(DataSE,DataMax,color='red',label="Max")
    ax.plot(DataSE,DataMin,color='blue',label="Min")
    ax.plot(DataListX,DataListY,label="Data")
    ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=10)
    #plt.plot(DataListEX,DataListEY,marker="o",color='yellow')
    outputfilename = './AllData/'+str(plot_label)+'_'+TestName+'_'+TestUnit+E_Label+'_'+str(ercunt)+'.png'
    print("合計:",DataNo)
    print("ERROR_Count:",ercunt)
    print("Output_File:",outputfilename)
    #plt.savefig(outputfilename) 
    #plt.show()
    plot_label = plot_label - 1
    E_Label =''
    DataListY.clear()
    DataListX.clear()
    DataListEX.clear()
    DataListEY.clear()
    DataMax.clear()
    DataMin.clear()
    DataSE.clear()
    label_No = 0
    DataNo = 0
    ercunt = 0
#sys.exit()
# ファイルをオープンする

#lot = 'Y895073H'
# 行ごとにすべて読み込んでリストデータにする


# 一行ずつ表示する

    

    # ファイルをクローズする
    

