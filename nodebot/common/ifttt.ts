
import got from 'got'
import moment from 'moment';

const EVENT_NAME = "buy_coin"
// doc: https://ifttt.com/maker_webhooks
const IFTTT_WEBHOOKS_URL = `https://maker.ifttt.com/trigger/${EVENT_NAME}/with/key/oJPBHriGv3c5Gh9iCZvop`;

export async function sendIfttt(title: string, value: string) {
    const top = title + " ⏰ " + moment().format("YYYY-MM-DD HH:MM:SS")
    const args = { value1: top, value2: value }
    const result = await got.post(IFTTT_WEBHOOKS_URL, { json: args })
    // console.log("00000---------");
    // console.log(result);
}
