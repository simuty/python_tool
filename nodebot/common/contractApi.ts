// const pancakeswapPairAbi = require("./abis/PancakePair.json");
// const pancakeswapFactoryAbi = require("./abis/PancakeFactoryV2.json");
const Web3 = require("web3")
const Tx = require('ethereumjs-tx').Transaction;
const Common = require('ethereumjs-common').default;

const pancakeSwapAbi = require("./abis/pancakeabi.json");
const pancakeSwapRouterAddress = '0x10ed43c718714eb63d5aa57b78b54704e256024e';
require("dotenv").config()

// bacscan 交易详情
const BSCSCANHASH = 'https://bscscan.com/tx/'

// !明确输入token数量
// ?精度可以通过token abi 获取，但是有些居然没有！！ 比如btcst
interface TYPE_SWAPEXACTTOKENSFORTOKENS {
    // 付出的token
    inputToken: string;
    // token 精度
    inputTokenDecimal: number;
    // 将要 花费多少个 inputToken
    inputNum: number;
    // 要购买的token
    outToken: string;
    // 可以省略，默认会很小
    outTokenDecimal: number;
    // 交换路径，[token]
    route: string[];
}

// !明确输出的token数量
interface TYPE_SWAPTOKENSFOREXACTTOKENS {
    // 付出的token
    inputToken: string;
    // token 精度
    inputTokenDecimal: number;
    // 要购买的token
    outToken: string;
    // 要购买的token 的数量
    outTokenNum: number;
     // token精度
     outTokenDecimal: number;
    // 交换路径，[token]
    route: string[];
}

export default class ContractApi {
    private contract: any;
    private url = "https://bsc-dataseed.binance.org/"
    private walletAddress = process.env.WALLET_ADDRESS
    private walletPK = Buffer.from(process.env.PRIVATEKEY.slice(2), 'hex');
    private gasLimitMax = 290000;
    private web3: any;
    // 滑点: 默认通过pancake计算出来的价格
    // 可以加大滑点，保证一次买入
    public slippage: number;

    constructor(slippage?: number) {
        this.slippage = slippage ? slippage : 0;
        this.web3 = new Web3(new Web3.providers.HttpProvider(this.url));
        this.contract = new this.web3.eth.Contract(pancakeSwapAbi, pancakeSwapRouterAddress, { from: this.walletAddress });
    }

    /**
     * 
     * @param inputToken @确定  如：用 100U 买 outToken; 
     * @param inputNum 付出的inputToken个数
     * @param outToken 需要购买的token
     * 
     */
    public async swapExactTokensForTokens(args: TYPE_SWAPEXACTTOKENSFORTOKENS) {
        const { inputToken, inputNum, inputTokenDecimal, outToken,
            outTokenDecimal, route } = args;
        // 付款数量
        // const inputTokenDec = 17;// await this.getDecimal(inputToken);
        const amountIn = this.tokenAmountToHex(inputTokenDecimal, inputNum);
        // 最小接受个数
        const minNum = 0.00000001;
        const amountOut = this.tokenAmountToHex(outTokenDecimal, minNum);
        const data = this.contract.methods.swapExactTokensForTokens(
            // 付出的 U或bnb 币的总数
            amountIn,
            // 将要购买的数量
            amountOut,
            // 购买路径
            route,
            // 钱包地址
            this.walletAddress,
            // 等待时间
            this.web3.utils.toHex(Math.round(Date.now() / 1000) + 60 * 20)
        );
        const gasPrice = await this.web3.eth.getGasPrice();
        const count = await this.web3.eth.getTransactionCount(this.walletAddress);
        const rawTransaction = {
            from: this.walletAddress,
            gasPrice: this.web3.utils.toHex(gasPrice),
            gasLimit: this.web3.utils.toHex(this.gasLimitMax),
            to: pancakeSwapRouterAddress,
            value: this.web3.utils.toHex('0'),
            data: data.encodeABI(),
            nonce: this.web3.utils.toHex(count)
        };
        const BSC_FORK = Common.forCustomChain(
            'mainnet',
            {
                name: 'Binance Smart Chain Mainnet',
                networkId: 56,
                chainId: 56,
                url: 'https://bsc-dataseed.binance.org/'
            },
            'istanbul',
        );
        const transaction = new Tx(rawTransaction, { 'common': BSC_FORK });
        transaction.sign(this.walletPK);
        const result = await this.web3.eth.sendSignedTransaction('0x' + transaction.serialize().toString('hex'));
        const { status, transactionHash } = result;
        return {
            status,
            transactionHash: `${BSCSCANHASH}${transactionHash}`
        }
    }

    /**
     * 购买执行数量的token
     * 
     * @param outTokenNum @确定
     */
    public async swapTokensForExactTokens(args: TYPE_SWAPTOKENSFOREXACTTOKENS) {
        const { inputToken, inputTokenDecimal, outToken, outTokenNum, outTokenDecimal, route } = args;
        // 要购买的token个数
        const amountOut = this.web3.utils.toHex((Math.round(10 ** outTokenDecimal)) * outTokenNum).toString();
        // 反推需要的inputToken数量
        // const price = await this.getTokenPeice(route, inputTokenDecimal, outTokenNum);
        // const amountIn = this.web3.utils.toHex(price).toString();

        // ! 滑点价格
        const price = await this.getTokenPeice(route, inputTokenDecimal, outTokenNum);
        const slippagePrice = this.slippage === 0 ? price : price +  price*this.slippage
        const amountIn = this.web3.utils.toHex(slippagePrice).toString();
        const data = this.contract.methods.swapTokensForExactTokens(
            // 将要购买的数量
            amountOut,
            // 付出的 U或bnb 币的总数
            amountIn,
            // 购买路径
            route,
            // 钱包地址
            this.walletAddress,
            // 等待时间
            this.web3.utils.toHex(Math.round(Date.now() / 1000) + 60 * 20)
        );
        const gasPrice = await this.web3.eth.getGasPrice();
        const count = await this.web3.eth.getTransactionCount(this.walletAddress);
        const rawTransaction = {
            from: this.walletAddress,
            gasPrice: this.web3.utils.toHex(gasPrice),
            gasLimit: this.web3.utils.toHex(this.gasLimitMax),
            to: pancakeSwapRouterAddress,
            value: this.web3.utils.toHex('0'),
            data: data.encodeABI(),
            nonce: this.web3.utils.toHex(count)
        };
        console.log(rawTransaction);
        const BSC_FORK = Common.forCustomChain(
            'mainnet',
            {
                name: 'Binance Smart Chain Mainnet',
                networkId: 56,
                chainId: 56,
                url: 'https://bsc-dataseed.binance.org/'
            },
            'istanbul',
        );
        const transaction = new Tx(rawTransaction, { 'common': BSC_FORK });
        transaction.sign(this.walletPK);
        const result = await this.web3.eth.sendSignedTransaction('0x' + transaction.serialize().toString('hex'));
        return {
            status,
            transactionHash: `${BSCSCANHASH}${transactionHash}`
        }
    }

    /**
     * token 单价
     * @param token 
     * @param routePath // todo 暂时不知道怎么自动获取两个token之间的route
     * @param decimal 精度 一般为18
     * @param num 默认为一个token的价格
     * ! 返回值为 如：1742701375703401883 ； 单价为 1742701375703401883 / 10**decimal
     */
    public async getTokenPeice(routePath: string[], decimal: number, num = 1, token: string = "") {
        const buyNum = (Math.round(10 ** decimal)) * num;
        const amountOut = this.web3.utils.toHex(buyNum).toString();
        const getIn = await this.contract.methods.getAmountsIn(amountOut, routePath).call()
        console.log("=====>>>", getIn);
        return getIn[0]
    }
    // 
    // 
    /**
     * 获取token精度
     * 1. 获取abi ---> getDecimal
     * 2. 
     * 
     * https://api.bscscan.com/api?module=contract&action=getabi&address=0x78650b139471520656b9e7aa7a5e9276814a38e9&apikey=key
     * @param token 
     * @returns 
     */
    private async getDecimal(token: string) {
        // ! btcst abi居然没有获取基本信息接口 并且 精度还是 17 ！！！！！！
        // const contract = await new this.web3.eth.Contract(tokenAbi, token );
        // const tokenDecimals = await contract.methods.decimals().call();
        return 18;
    }

    private tokenAmountToHex(decimal: number, num: number) {
        return this.web3.utils.toHex((Math.round(10 ** decimal)) * num).toString();
    }
}