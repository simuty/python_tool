
// import * as _ from "lodash";
// const res = _.fill(Array(4), 1);
// // console.log(res);


// import * as fs from "fs"
// const dotenv = require('dotenv')
// const envConfig = dotenv.parse(fs.readFileSync('.env'))
// // console.log(envConfig);
// // console.log(envConfig["projectId"]);

// // for (const k in envConfig) {
// //   process.env[k] = envConfig[k]
// // }



// import got from 'got'
// const moment = require('moment');
// // import TelegramBot from 'node-telegram-bot-api'
// const TelegramBot = require('node-telegram-bot-api');
// import Agent from 'socks5-https-client/lib/Agent'


// import { HOST, PORT } from './common/const'


// export async function sendTg() {
//     const TOKEN = process.env.TELEGRAM_TOKEN || 'YOUR_TELEGRAM_BOT_TOKEN';
//     const TELEGRAM_GROUP_ID = process.env.TELEGRAM_GROUP_ID || 'YOUR_TELEGRAM_CHAT_ID';
//     console.log(process.env.TELEGRAM_TOKEN, TELEGRAM_GROUP_ID);
//     const bot = new TelegramBot(TOKEN, {
//         polling: true,
//         request: {
//             agentClass: Agent,
//             agentOptions: {
//                 socksHost: HOST,
//                 socksPort: PORT
//                 // If authorization is needed:
//                 // socksUsername: process.env.PROXY_SOCKS5_USERNAME,
//                 // socksPassword: process.env.PROXY_SOCKS5_PASSWORD
//             }
//         }
//     });
//     // console.log(bot);
//     bot.sendMessage(TELEGRAM_GROUP_ID, "replyText");

//     // 匹配/hentai
//     bot.onText(/\/hentai/, function onLoveText(msg) {
//         console.log("-------");
//         bot.sendMessage(msg.chat.id, 'Are you a hetai?');
//     });


//     // 匹配/echo
//     bot.onText(/\/echo (.+)/, (msg, match) => {

//         const chatId = msg.chat.id;
//         const resp = match[1];
//         bot.sendMessage(chatId, resp);
//     });

//     bot.on('message', (msg) => {
//         const chatId = msg.chat.id;
//         console.log("------ss-");

//         // bot.sendMessage(chatId, replyText );
//     });
// }

require('dotenv').config();



const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const TELEGRAM_GROUP_ID = process.env.TELEGRAM_GROUP;
// console.log(process.env.TELEGRAM_TOKEN, TELEGRAM_GROUP_ID);
// const bot = new TelegramBot(TOKEN);
// const url = `https://api.telegram.org`
// bot.setWebHook(`${url}/bot${TOKEN}`);
// // console.log(bot);
// bot.sendMessage(TELEGRAM_GROUP_ID, "replyText");


console.log(TELEGRAM_TOKEN);
// https://github.com/pancakeswap/pancake-info-api
// const PANCAKESWAP_URL = "https://api.pancakeswap.info/api/v2/tokens/"
const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`

// https://api.telegram.org/bot1852861163:AAF48Mn1q-FbsTl7Q9OyYC68O5jRcmIDDC0/sendMessage?chat_id=-403769892&text=my sample text

// import got from 'got'
// const moment = require('moment');
// import * as _ from 'lodash';
// import { HOST, PORT } from './common/const'
// const tunnel = require('tunnel');



// // ?chat_id=-403769892&text=my sample text`
// export async function getPrice() {
//     try {
//         const result = await got.post(url, {
//             agent: {
//                 https: tunnel.httpsOverHttp({
//                     proxy: {
//                         host: HOST,
//                         port: PORT
//                     }
//                 })
//             },
//             json: {
//                 chat_id: TELEGRAM_GROUP_ID,
//                 text: "asdfsdfsadfsadfsd"
//             }
//         }).json()
//         console.log(result);
//     } catch (error) {
//         return [];
//     }
// }

// getPrice()


const TelegramBot = require('node-telegram-bot-api');
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

bot.on('message', async (msg) => {
    console.log(msg);

    if (!!msg && !!msg.text && msg.text.startsWith('/price')) {
        const chatId = msg.chat.id;
        // const price = await rmPrice.getLatestPrice();
        // const pricePer1M = price.multipliedBy(Math.pow(10, 6));
        // const burnedTokens = await stats.getBurnedTokens();
        // const totalSupply = await stats.getTotalSupply();
        // const totalSupplyInT = (totalSupply/Math.pow(10,12));
        // const totalCirculation = totalSupply-burnedTokens;
        // const burnedTokensInT = (burnedTokens/Math.pow(10,12)).toFixed(1);
        // const priceBurnedTokens = stats.getDollarFormatted(price * burnedTokens);
        // const totalCirculationInT = (totalCirculation / Math.pow(10,12)).toFixed(1);
        // const marketCap =  stats.getDollarFormatted(price * totalCirculation);

        let reply =
            `*TokenName*
1M tokens = \$${1.222222}
💴 *Market Cap*: ${12212}
💰 *Circulating Supply*: ${111111111111111111}T / ${1000}T
🔥 *Total burned*: ${111111122222}T / ${8}

[Buy](https://rsk.mn/buy) | [Wallet](https://rsk.mn/wallet) | [UniRocket](https://rsk.mn/unirocket) | [BSCScan](https://rsk.mn/bscscan) | [Website](https://riskmoon.com)
📈 [Charts](https://rsk.mn/chart): [DexGuru](https://rsk.mn/dex) | [Bogged](https://rsk.mn/bog) | [DexT](https://rsk.mn/dext)
📣 *Social Insights:* [LunarCrush](https://rsk.mn/insights)
`;

let reply =
`*RISKMOON*
1M tokens = \$${pricePer1M.toFixed(6)}
💴 *Market Cap*: ${marketCap}
💰 *Circulating Supply*: ${totalCirculationInT}T / ${totalSupplyInT}T
🔥 *Total burned*: ${burnedTokensInT}T / ${priceBurnedTokens}

[Buy](https://rsk.mn/buy) | [Wallet](https://rsk.mn/wallet) | [UniRocket](https://rsk.mn/unirocket) | [BSCScan](https://rsk.mn/bscscan) | [Website](https://riskmoon.com)
📈 [Charts](https://rsk.mn/chart): [DexGuru](https://rsk.mn/dex) | [Bogged](https://rsk.mn/bog) | [DexT](https://rsk.mn/dext)
📣 *Social Insights:* [LunarCrush](https://rsk.mn/insights)
`;


        bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });
    }
});
