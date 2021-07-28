
import { getPrice } from './common/net';
import { sleep } from './common/fun';
import { sendIfttt } from './common/ifttt';
import * as _ from "lodash";


const tokenList = [
    // Cake
    "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    // Mbox
    "0x3203c9e46ca618c8c1ce5dc67e7e9d75f5da2377"

]


async function start() {

    // while (true) {
    const argsList = [];
    tokenList.map(item => argsList.push(getPrice(item)));
    const resultList = await Promise.all(argsList)
    console.log(resultList);
    // key: token名字 大写
    // value: 保留三位
    let tokenInfo: { [key: string]: string } = {}
    for (const iterator of resultList) {
        const { symbol, price } = iterator
        const name = _.toUpper(symbol);
        tokenInfo[name] = price
    }

    // MBOX > 2 ||  >3
    // tokenInfo["MBOX"] > 2

    // }
}

(async () => {

    try {
        sendIfttt("起飞", "🛫️");
        await start();
    } catch (error) {
        await sleep(10);
        await start();
    }

})()


