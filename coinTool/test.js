/*
 * @Author: simuty
 * @Date: 2021-07-01 18:44:56
 * @LastEditTime: 2021-07-02 11:21:59
 * @LastEditors: Please set LastEditors
 * @Description: 
 */



// bnbtc 波段， 赚50%跑路
let [i, start]  = [0,  230];
while (i < 10) {
    start += start /= 2;
    console.log(i, start, start * 5)
    i++
}



/** 
➜  coinTool git:(main) ✗ node test.js
0 150 750
1 225 1125
2 337.5 1687.5
3 506.25 2531.25
4 759.375 3796.875
5 1139.0625 5695.3125
6 1708.59375 8542.96875
7 2562.890625 12814.453125
8 3844.3359375 19221.6796875
9 5766.50390625 28832.51953125
*/