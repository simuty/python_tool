
import { getPrice } from './common/net';
import { sleep } from './common/fun';
import { sendIfttt } from './common/ifttt';
import { RATIO_UP, RATIO_DOWN, INTERVAL_MINTUS, BASE_ARRAY_LENGTH } from './common/config';
import * as _ from "lodash";
import * as moment from 'moment';


const tokenList = [
    // Cake
    "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    // Mbox
    "0x3203c9e46ca618c8c1ce5dc67e7e9d75f5da2377"

]

interface TYPE_TOKENINFO { [key: string]: string }
interface TYPE_ITEM { price: number, timestamp: number  }

async function start() {

    while (true) {
        const argsList: any[] = [];
        tokenList.map(item => argsList.push(getPrice(item)));
        const resultList = await Promise.all(argsList)
        // console.log(resultList);
        // key: token名字 大写
        // value: 价格
        let tokenInfo: TYPE_TOKENINFO = {}
        for (const iterator of resultList) {
            const { symbol, price } = iterator
            const name = _.toUpper(symbol);
            tokenInfo[name] = price
        }

        console.log(tokenInfo);


        mbox(tokenInfo)
        // await sleep(10)
        // MBOX > 2 ||  >3
        // tokenInfo["MBOX"] > 2

    }
}



// mbox
let mboxList: any[] = [{ price: 1.1, timestamp: 1627483538 }];


const PRICE_MBOX = [2, 3];
function mbox(tokenInfo: TYPE_TOKENINFO) {
    const price: number = _.floor(Number(tokenInfo["MBOX"]), 8);
    const item = {
        price, 
        timestamp: moment().unix()
    }
    mboxList.push(item);
    // 基数
    const judgePrice = price > 0;
    console.log(mboxList);

    // 1. 达到基准
    if (judgePrice) {
        // 2. 先推送三次
        if (mboxList.length < BASE_ARRAY_LENGTH) {
            handleNotfication(price, 11);
        } else {
            // 3。 数组最后一个与第一个计算 涨跌 百分比
            const [first, last] = [_.first(mboxList), _.last(mboxList)];
            //  与第一个对比，增长百分比
            const ratio = _.floor(_.divide((last.price - first.price), first.price), 3) * 100;
            const diffMintus = (last.timestamp - first.timestamp) / 60;
            if (ratio > RATIO_UP || ratio < RATIO_DOWN || diffMintus > INTERVAL_MINTUS) {
                // 涨跌幅度过大，则提醒⏰ & 保留最新x个 & 计算间隔时间
                mboxList = _.takeRight(mboxList, BASE_ARRAY_LENGTH)
                handleNotfication(last.price, diffMintus, ratio);
            }
        }
    }

}


async function handleNotfication(price: number, time: number, ratio = 0) {
    const one = ratio === 0 ? "" : ratio > 0 ? `📈 ${ratio}% 间隔：${time}` : `📉 ${ratio}% 间隔：${time}`;
    const two = `💵 ${price} USDT`;
    // const three = ``
    const msg = one ? `${one}\n${two}` : `${two}`;
    sendIfttt("起飞", msg);
}


(async () => {

    try {
        const msg = `
⛔️ Decreased 3.73% in 6.1 hour(s)\n💵 Price - 16.92800000 USDT\n⏱️ [28 Jul] - 08:41:48 UTC
                `
        // sendIfttt("起飞", msg);
        await start();
    } catch (error) {
        await start();
    }

})()


