###
 # @Author: simuty
 # @Date: 2021-06-07 18:11:49
 # @LastEditTime: 2021-06-07 18:12:02
 # @LastEditors: Please set LastEditors
 # @Description: 
### 
#! /bin/bash
pidof ifttt_pitman.py # 检测程序是否运行
while [ $? -ne 0 ]    # 判断程序上次运行是否正常结束
do
    echo "Process exits with errors! Restarting!"
    python3 ifttt_pitman.py    #重启程序
done
echo "Process ends!"