/*
 * @Author: simuty
 * @Date: 2021-06-10 11:30:44
 * @LastEditTime: 2021-06-24 10:09:39
 * @LastEditors: Please set LastEditors
 * @Description:
 */
// 59100 - 5600 / 900 = 59

// $25: 59100 / 1124 = 52.5
// 1560 / 25

// let n = 1
// while (n<5) {
//     const sum = 53500 + 5600 + 1570 * n;
//     const num = 900 + (5600 + 1570 * n) / 24
//     const res = parseFloat (sum / num, 1)
//     console.log(`59 - ${n}: 单价 ${res}--个数：${num}--总金额--${sum}`, )
//     n++
// }

// let n = 1
// while (n<5) {
//     const sum = 59100 + 1570 * n;
//     const num = 900 + (1570 * n) / 22
//     const res = sum / num
//     console.log(`59 - ${n}: `, res)
//     n++
// }

// 单价24，每增1w， 单价降低 1.4



function cal(total, stake) {
    let start = 1;
    let count = 0;
    while (start < 4) {
        const oneST = total / stake;
        const st1000 = oneST * 1000;
        const dayOf1000 = st1000 / 7;
        console.log(
            `1000个： 第${start}周 1st: `,
            total,
            total / 7,
            oneST,
            "==>>>> 1000st total/day",
            st1000,
            dayOf1000,
        );
        total = total /= 2;
        start++;
        count += oneST;
    }
    return count
}




// st 质押
const stTotal = 75000000;
const stStake = 6500000;
const result_st = cal(stTotal, stStake)
console.log("1st八周共挖：", result_st, result_st * 1000);

const result_dog = cal(4500000, 65000)
console.log("1st八周共挖：", result_dog, result_dog * 1000);
