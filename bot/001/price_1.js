const Web3 = require('web3');


var ETHER = Math.pow(10, 18);

var WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c';
var CAKE_ROUTER_V2 = Web3.utils.toChecksumAddress('0x10ed43c718714eb63d5aa57b78b54704e256024e');

var web3 = new Web3('https://bsc-dataseed1.binance.org:443');

var ABI = [{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}];


var get_price = async function(token, decimals, pair_contract, is_reverse, is_price_in_peg) {
    var price,
        peg_reserve = 0,
        token_reserve = 0,
        res = await pair_contract.methods.getReserves().call(),
        reserve0 = res[0],
        reserve1 = res[1];
        
    if (is_reverse) {
        peg_reserve = reserve0;
        token_reserve = reserve1;
    } else {
        peg_reserve = reserve1;
        token_reserve = reserve0;
    }
    
    if (token_reserve && peg_reserve) {
        if (is_price_in_peg) {
            // CALCULATE PRICE BY TOKEN PER PEG
            price = (Number(token_reserve) / Number(Math.pow(10, decimals))) / (Number(peg_reserve) / Number(ETHER));
        } else {
            // CALCULATE PRICE BY PEG PER TOKEN
            price = (Number(peg_reserve) / Number(ETHER)) / (Number(token_reserve) / Number(Math.pow(10, decimals)));
        }
            
        return price;
    }
    
    return Number(0);
};



(async function test(){
    var token = Web3.utils.toChecksumAddress('0x126f5f2a88451d24544f79d11f869116351d46e1');
    var pair = await (await (new web3.eth.Contract(ABI, CAKE_FACTORY_V2))).methods.getPair(token, WBNB).call();
    var pair_contract = await new web3.eth.Contract(ABI, pair);
    var is_reversed = (await pair_contract.methods.token0().call()) == WBNB;
    var decimals = await (await new web3.eth.Contract(ABI, token)).methods.decimals().call();
    var is_price_in_peg = true;
    
    console.log(await get_price(token, decimals, pair_contract, is_reversed, is_price_in_peg), 'BNB')
})()



// 2071024336924435472253392/6811785327690737321528 = 304.0354675456