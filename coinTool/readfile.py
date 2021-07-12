'''
Author: simuty
Date: 2021-07-01 14:19:06
LastEditTime: 2021-07-01 14:31:04
LastEditors: Please set LastEditors
Description: 
'''
import json
import ast


def read_log():
    """
    读取日志文件,进行数据重组,写入mysql
    :return:
    """
    file = "w_logs/luck.log"
    with open(file) as f:
        """使用while循环每次只读取一行,读到最后一行的时候结束"""
        while True:
            lines = f.readline()
            if not lines:
                break
            line = lines.replace("\n", "").split("INFO:")
            print("---->", line[1])
            dic = eval(line[1])
            print("---======->", dic["TIME"])
            
            data.append(dic)
            return data


if __name__ == '__main__':
    data = []
    print(read_log())