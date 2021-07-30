
import got from 'got'
import moment from 'moment';
import * as _ from 'lodash';
import { HOST, PORT } from './const'
const tunnel = require('tunnel');
import { logger } from "./log4";
import { sleep } from './fun';


interface RESULT {
    updated_at: number;
    data: Data;
}
interface Data {
    name: string;
    symbol: string;
    price: string;
    price_BNB: string;
}


// https://github.com/pancakeswap/pancake-info-api
const PANCAKESWAP_URL = "https://api.pancakeswap.info/api/v2/tokens/"

export async function getPrice(token: string) {
    try {
        const url = PANCAKESWAP_URL + token;
        const result: RESULT = await got(url, {
            agent: {
                https: tunnel.httpsOverHttp({
                    proxy: {
                        host: HOST,
                        port: PORT
                    }
                })
            }
        }).json()
        const { symbol, price } = result.data;
        logger(symbol).info(JSON.stringify(result));
        console.log(JSON.stringify({time: moment().format('YYYY-MM-DD HH:MM:SS'), symbol, price: _.floor(Number(price), 3)}));
        return result.data;
    } catch (error) {
        logger("error").error(JSON.stringify(error));
        await sleep(10);
        return [];
    }
}

// getPrice("0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82")

// async function getPrice(token: string) {
//     try {
//         const url = PANCAKESWAP_URL + token;

//         const instance = got.extend({
//             hooks: {
//                 afterResponse: [
//                     (response, retryWithMergedOptions) => {
//                         if (response.statusCode !== 200) {

//                         }
//                         // No changes otherwise
//                         return response;
//                     }
//                 ]
//             }
//         })

//         const result: RESULT = await got(url, {
//             agent: {
//                 https: tunnel.httpsOverHttp({
//                     proxy: {
//                         host: HOST,
//                         port: PORT
//                     }
//                 })
//             }
//         }).json()
//         return result.data;
//     } catch (error) {

//     }

// }
