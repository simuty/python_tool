const Web3 = require('web3');


(async ()=> {
    // const tokenAddres = '0xe550a593d09fbc8dcd557b5c88cea6946a8b404a'; // change this with the token addres that you want to know the 
    const tokenAddres = '0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51'; // bunny
    const BNBTokenAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c" //BNB
    const PANCAKESWAP_FACTORY_ADDR_V2 = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73";
    const pancakeswapFactoryAbi = require("./PancakeFactoryV2.json");
    const pancakeswapPairAbi = require("./PancakePair.json");
    const tokenAbi = require("./PancakePair.json");

    const web3 = new Web3("https://bsc-dataseed1.binance.org");


    let con = await new web3.eth.Contract( tokenAbi, tokenAddres );
    let tokenDecimals = await con.methods.decimals().call();
    console.log(tokenDecimals)

    const pancakeswapFactoryV2 = new web3.eth.Contract(
        pancakeswapFactoryAbi,
        PANCAKESWAP_FACTORY_ADDR_V2
      );

    const pairAddress = await pancakeswapFactoryV2.methods
      .getPair(tokenAddres, BNBTokenAddress)
      .call();

    const contract = new web3.eth.Contract(pancakeswapPairAbi, pairAddress);
    const token0 = await contract.methods.token0().call();
    console.log(pairAddress);
    console.log(token0);
    
})()

// 9650250045076011674614/18016873450800522053208

// 965548301674072/2032334068924844747863

// 0.000000475093301 * 300

// 965548301674072/2032334068924844747863

553080518611308685919957/ 29427547466932416361201 === 18.7946521616