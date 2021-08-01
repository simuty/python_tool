// 1. tg bsc交易记录  https://github.com/simuty/telegram-bot/blob/master/index.js
// 2. web3 交易 https://github.com/Nafidinara/tranfer-bot/blob/master/bot.js
// 3. ethers 交易 https://github.com/Nafidinara/bot-pancakeswap

import ContractApi from './common/contractApi';
const BNBToken = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; // BNB
const USDToken = "0x55d398326f99059fF775485246999027B3197955"; // USDT
const BTCSTToken = "0x78650b139471520656b9e7aa7a5e9276814a38e9"; // btcst
const cakeToken = "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"
const bunnyToken = "0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51"



const btcstPath = [USDToken, BNBToken, BTCSTToken];
const cakePath = [USDToken, cakeToken, bunnyToken];

// 获取token价格
async function getPrice() {
    const contractApi = new ContractApi()
    const price = await Promise.all([
        contractApi.getTokenPeice(btcstPath, 17),
        contractApi.getTokenPeice(cakePath, 18),
    ]) 
    console.log(price[0] / 10**18);
}

// getPrice()

// 买币 明确U的数量
async function swapExactTokensForTokens() {
    const contractApi = new ContractApi()
    const args = {
        inputToken: USDToken,
        inputNum: 5,
        inputTokenDecimal: 18,
        // 要购买的token
        outToken: BTCSTToken,
        outTokenDecimal: 17,
        // 交换路径，[token]
        route: btcstPath
    }
    const result = await contractApi.swapExactTokensForTokens(args);
    console.log(result);
}

// swapExactTokensForTokens()

// 买币 明确U的数量
async function swapTokensForExactTokens() {
    const contractApi = new ContractApi()
    const args = {
        inputToken: USDToken,
        inputTokenDecimal: 18,
        // 要购买的token
        outToken: BTCSTToken,
        outTokenDecimal: 17,
        outTokenNum: 0.2,
        // 交换路径，[token]
        route: btcstPath
    }
    const result = await contractApi.swapTokensForExactTokens(args);
    console.log(result);
}

swapTokensForExactTokens()