
import got from 'got'
import { HOST, PORT } from './config'
const tunnel = require('tunnel');
import { logger } from "./log4";


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

export async function getPrice(token: string): Promise<Data> {
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
        const { symbol } = result.data;
        logger(symbol).info(JSON.stringify(result));
        return result.data;
    } catch (error) {

    }
}


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
