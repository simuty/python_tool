/*
 * @Author: simuty
 * @Date: 2021-06-10 11:30:44
 * @LastEditTime: 2021-06-10 11:51:01
 * @LastEditors: Please set LastEditors
 * @Description: 
 */
// 59100 - 5600 / 900 = 59

// $25: 59100 / 1124 = 52.5 
// 1560 / 25 



let n = 1
while (n<5) {
    const sum = 53500 + 5600 + 1570 * n;
    const num = 900 + (5600 + 1570 * n) / 24
    const res = parseFloat (sum / num, 1)
    console.log(`59 - ${n}: 单价 ${res}--个数：${num}--总金额--${sum}`, )
    n++
}

// let n = 1
// while (n<5) {
//     const sum = 59100 + 1570 * n;
//     const num = 900 + (1570 * n) / 22
//     const res = sum / num
//     console.log(`59 - ${n}: `, res)
//     n++
// }

// 单价24，每增1w， 单价降低 1.4 