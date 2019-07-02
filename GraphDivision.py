import sys
import os
import glob
import math
import matplotlib.pyplot as plt
args = sys.argv
plot_label = int(args[1])
os.makedirs('AllData3', exist_ok=True)
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
                            #plt.plot(DataNo,float(data[3]),marker="o",color='yellow')
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
    Data_count = int(args[2])
    Loop_count = math.ceil(len(DataListY)/Data_count)
    print(Loop_count)
    for i in range(0, Loop_count):
        point = i * Data_count
        TestListY = DataListY[point:point + Data_count]
        TestListX = DataListX[point:point + Data_count]
        #print(TestListY)
        fig = plt.figure(figsize=(15, 8), dpi=100)

        # Axesを追加
        ax = fig.add_subplot(1,1,1)
        ax.set_title(TestName, fontsize = 16)
        DataMax = [DataMaxValue,DataMaxValue]
        DataMin = [DataMinValue,DataMinValue]
        DataSE = [point,point + Data_count]
        ax.plot(DataSE,DataMax,color='red',label="Max")
        ax.plot(DataSE,DataMin,color='blue',label="Min")
        ax.plot(TestListX,TestListY,label="Data")
        ax.set_ylim(DataMinValue-(DataMinValue*0.05),DataMaxValue*1.05)
        ax.set_xlim(point,point + Data_count)
        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=10)
        #plt.plot(DataListEX,DataListEY,marker="o",color='yellow')
        os.makedirs('AllData3/'+str(plot_label)+'_'+TestName+'_'+TestUnit+'_'+str(ercunt)+'/', exist_ok=True)
        outputfilename = './AllData3/'+str(plot_label)+'_'+TestName+'_'+TestUnit+'_'+str(ercunt)+'/'+str(point)+'-'+str(point+Data_count)+'.png'
        print("合計:",DataNo)
        print("ERROR_Count:",ercunt)
        print("Output_File:",outputfilename)
        plt.savefig(outputfilename)
        plt.close()
    #sys.exit()
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
    

