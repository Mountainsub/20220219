from ctypes import wintypes
import subprocess

import pandas as pd
import numpy as np
import time 
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from request5.rakuten_rss import rss , rss2 
from lib.ddeclient import DDEClient
import datetime

class Function:
    #並列処理
    def get_lines(cmd):
        '''
        :param cmd: str 実行するコマンド.
        :rtype: generator
        :return: 標準出力 (行毎).
        リアルタイムにファイルの出力を取得error
        '''
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            line = proc.stdout.readline()
            if line:
                yield line
            if not line and proc.poll() is not None:
                break
        return


    def calculation(dde_ware, indexes_weight):

        calc = rss2("現在値", dde_ware, indexes_weight)
                
        return calc

if __name__ == '__main__':  
    # コマンドライン引数を取得
    args = sys.argv
    # count番目からcount+125番目までデータの総計を出す
    count = int(args[2])*126 
    
    # コマンドライン引数の１番目で書き込みか読み取りかを選択
    num = args[1]
    temp = 0
    
    if int(num) == 0: #　書き込み
        for line in Function.get_lines(cmd='python main2.py ' + str(count)+ ' T'): # ファイル読み込み　第一引数はスタートナンバー                
            # python main2.pyは計算して書き込みを行うコマンドです。
            string = "file_"+ str(int(args[2])) + ".txt"
            try:
                f = open(string, 'a') #　上書きモード ,改行なし
                temp = line.decode('sjis')
                temp.replace('\n', "")
                temp.replace('\r', "")
                f.write(temp)
                f.close() 
            except Exception:
                print("error")

            #print("OK") 
    else: #　読み込み
        a = 0
        while a <= 10**3: #１０の３乗数字に意味はない,それだけ長く。
            proc = subprocess.Popen('python main3.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = proc.communicate()[0].decode('sjis') # 出力結果を取得
            dt = datetime.datetime.today() # 今日の日時
            with open("fileX.txt", "a") as f: # 上書き
                try:
                    f.write(str(float(result)))    
                except:
                    print(result)
                    pass
                try:
                    print("present time:"+ str(dt),float(result))
                except:
                    pass
            time.sleep(2)
            a += 1
    



