
import got from 'got'
import _ from 'lodash';
const moment = require('moment');
require('dotenv').config();
// import TelegramBot from 'node-telegram-bot-api'
const TelegramBot = require('node-telegram-bot-api');


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



const TOKEN = process.env.TELEGRAM_TOKEN;
const TELEGRAM_GROUP = process.env.TELEGRAM_GROUP;
const bot = new TelegramBot(TOKEN, { polling: true });

export async function sendTg(args: TYPE_TG_MSG) {
    if (_.isEmpty(TOKEN) && _.isEmpty(TELEGRAM_GROUP)) {
        return false;
    }
    // 匹配/hentai
    bot.onText(/\/hentai/, function onLoveText(msg) {
        console.log("-------");
        bot.sendMessage(msg.chat.id, 'Are you a hetai?');
    });

    // 匹配/echo
    bot.onText(/\/echo (.+)/, (msg, match) => {
        const chatId = msg.chat.id;
        const resp = match[1];
        bot.sendMessage(chatId, resp);
    });

    bot.on('message', (msg) => {
        const chatId = msg.chat.id;
        console.log("------ss-");
        bot.sendMessage(chatId, "1234");
    });
}


interface TYPE_TG_MSG {
    token: string;
    price: number;

}

function formatTgMsg(args: TYPE_TG_MSG) {

}


sendTg()



// curl -X POST "https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/sendMessage" -d "chat_id=-403769892&text=my sample text"


// https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/getUpdates
// 1. botfater 新增bot 得到token
// 2. 将bot加入群组
// 3. 拼接如下URL，--> tg中：helloworld @botname --> 浏览器访问如下链接 ----> 得到chat.id
// https://api.telegram.org/bot<token>/getUpdates
// 4. 向群组发送消息 ---> 如下拼接
// https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/sendMessage?chat_id=-403769892&text=my sample text

