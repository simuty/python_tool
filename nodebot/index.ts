
import { getPrice } from './common/net';
import { TOKEN_CONFIG } from './common/config';
import { sleep } from './common/fun';
import { sendIfttt } from './common/ifttt';
import { RATIO_UP, RATIO_DOWN, REMIND_MINTUS, ALTER_TIME, SLEEP_TIME } from './common/const';
import * as _ from "lodash";
import moment from 'moment';

interface TYPE_TOKEN_API { name: string, symbol: string, price: string, price_BNB: string }

async function start() {
    while (true) {
        const argsList: any[] = [];
        _.keys(TOKEN_CONFIG).map(item => argsList.push(getPrice(TOKEN_CONFIG[item]["token"])))
        const resultList: TYPE_TOKEN_API[] = await Promise.all(argsList)
        // console.log(resultList);
        for (const iterator of resultList) {
            const apiTokenNmae = _.toUpper(iterator.symbol);
            const apiTokenPrice = _.floor(Number(iterator.price), 5);
            const { basePrices, list } = TOKEN_CONFIG[apiTokenNmae];
            const judgeList = TOKEN_CONFIG[apiTokenNmae].list;
            const priceList = TOKEN_CONFIG[apiTokenNmae].basePrices;
            TOKEN_CONFIG[apiTokenNmae].list = _.concat(list, apiTokenPrice);

            // todo 
            const upPrice = apiTokenPrice > basePrices[0];
            // 1. 过阀值 连续推送4次
            if (upPrice) {
                // 1.1 重置监控价格基数
                TOKEN_CONFIG[apiTokenNmae].basePrices = priceList.length > 1 ? _.takeRight(priceList, priceList.length - 1) : priceList;
                // const repeat = _.fill(Array(ALTER_TIME), handleNotfication(apiTokenNmae, apiTokenPrice));
                // let repeatList: any[] = [];
                // Array(ALTER_TIME).map(() => repeatList.push(handleNotfication(apiTokenNmae, apiTokenPrice)))
                // const result =  await Promise.all(repeatList)
                // console.log("======>>>>;;;; ", result);
                let i = ALTER_TIME;
                while (i > 0) {
                    await handleNotfication(apiTokenNmae, apiTokenPrice);
                    i--;
                }
            }
            // 2. 涨跌百分比 > x 
            const [first = 0, last = 0] = [_.first(judgeList), _.last(judgeList)];
            const ratio = _.floor(_.divide((last - first), first), 3) * 100;
            if (ratio > RATIO_UP || ratio < RATIO_DOWN) {
                // 涨跌幅度过大，则提醒⏰ & 保留最新x个
                handleNotfication(apiTokenNmae, apiTokenPrice, ratio);
                TOKEN_CONFIG[apiTokenNmae].list = [];
            }
            // 3. 数组长度过长，清空重新计算
            if (judgeList.length > 1000) {
                TOKEN_CONFIG[apiTokenNmae].list = []
            }
            // todo 4: 每30分钟推送一次
            const minutes = moment().minutes();
            if (_.includes(REMIND_MINTUS, minutes)) {
                handleNotfication(apiTokenNmae, apiTokenPrice);
            }
        }
        // console.log("111====>>>", TOKEN_CONFIG);
        await sleep(SLEEP_TIME);
    }
}

async function handleNotfication(token: string, price: number, ratio = 0) {
    const one = ratio === 0 ? "" : ratio > 0 ? `📈 ${token} ${ratio}% ` : `📉 ${token} ${ratio}%`;
    const two = `💵 ${price}`;
    await sendIfttt(one, two);
}


(async () => {

    try {
        sendIfttt("🛫️", "🛫️🛫️🛫️🛫️");
        await start();
    } catch (error) {
        await start();
    }

})()


