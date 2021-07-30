
import got from 'got'
import * as _ from 'lodash';
const moment = require('moment');
const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config()

import { HOST, PORT } from './const'

// doc: https://ifttt.com/maker_webhooks
const EVENT_NAME = "buy_coin"
const IFTTT_WEBHOOKS_URL = `https://maker.ifttt.com/trigger/${EVENT_NAME}/with/key/${process.env.IFTTT_KEY}`;
export async function sendIfttt(title: string, value: string) {
    const top = title + " ⏰ " + moment().format("YYYY-MM-DD hh:mm:ss")
    const args = { value1: top, value2: value }
    const result = await got.post(IFTTT_WEBHOOKS_URL, { json: args })
    // console.log("00000---------");
    // console.log(result);
}


/** ******************  tg  ********************   */
interface TYPE_TG_MSG {
    key: string;
    token: string;
    price: number;
}

const TOKEN = process.env.TELEGRAM_TOKEN;
const TELEGRAM_GROUP = process.env.TELEGRAM_GROUP;
const bot = new TelegramBot(TOKEN, { polling: true });

// todo 自动回复, 之后完善
async function autoReply() {
    if (_.isEmpty(TOKEN) && _.isEmpty(TELEGRAM_GROUP)) {
        return false;
    }
    // 匹配/hentai
    bot.onText(/\/hentai/, function onLoveText(msg) {
        bot.sendMessage(msg.chat.id, 'Are you a hetai?');
    });

    // 匹配/echo
    bot.onText(/\/echo (.+)/, (msg: any, match: any) => {
        const chatId = msg.chat.id;
        const resp = match[1];
        bot.sendMessage(chatId, resp);
    });

    bot.onText(/\/token (.+)/, (msg: any, match: any) => {
        const chatId = msg.chat.id;
        const resp = match[1];
        bot.sendMessage(chatId, resp);
    });

    bot.on('message', (msg: any, match: any) => {
        const chatId = msg.chat.id;
        console.log(msg);
        const resp = match[1] || "走错了";
        bot.sendMessage(chatId, resp);
    });

}

// sendTg({ name: "BNB", token: "0x17B7163cf1Dbd286E262ddc68b553D899B93f526", price: 1 })
export async function sendTg(args: TYPE_TG_MSG) {
    console.log(args);
    const { key, token, price } = args;
    const bscScan = `[ BscScan ](https://bscscan.com/token/${token})`
    const buy = `[ Buy ](https://exchange.pancakeswap.finance/#/swap?outputCurrency=${token})`

    const dexGuru = `[ DexGuru ](https://dex.guru/token/${token})`
    const dextools = `[ Dextools ](https://www.dextools.io/app/pancakeswap/pair-explorer/${token})`
    let reply =
        `*${key}* \$${price}
💴 *Market Cap*: ${1}
💰 *Circulating Supply*: ${1}T / ${1}T
🔥 *Total burned*: ${1}T / ${1}
💰 ${bscScan} |  ${buy}
📈 ${dexGuru} | ${dextools}
`;
    bot.sendMessage(TELEGRAM_GROUP, reply, { parse_mode: 'Markdown' });
}
/** ******************  tg  ********************   */

// formatTgMsg()



// curl -X POST "https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/sendMessage" -d "chat_id=-403769892&text=my sample text"


// https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/getUpdates
// 1. botfater 新增bot 得到token
// 2. 将bot加入群组
// 3. 拼接如下URL，--> tg中：helloworld @botname --> 浏览器访问如下链接 ----> 得到chat.id
// https://api.telegram.org/bot<token>/getUpdates
// 4. 向群组发送消息 ---> 如下拼接
// https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/sendMessage?chat_id=-403769892&text=my sample text

