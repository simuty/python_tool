/*
 * @Author: simuty
 * @Date: 2021-07-19 21:23:18
 * @LastEditTime: 2021-07-19 21:48:47
 * @LastEditors: Please set LastEditors
 * @Description: 
 */
const ethers = require('ethers');
// const utils = require('ethers/utils');


let privateKey = "0x9a80d48172b7386cf38fca46b2537f1cf6378edf40ab6e1633f5426aa6fefc55";
let wallet = new ethers.Wallet(privateKey);

// Connect a wallet to mainnet
let provider = ethers.getDefaultProvider();
console.log(provider);
console.log("================================");

let walletWithProvider = new ethers.Wallet(privateKey, provider);
console.log(walletWithProvider);


console.log();

let transaction = {
    nonce: 0,//(node:1036) UnhandledPromiseRejectionWarning: Error: nonce has already been used (version=4.0.13)
    
    gasLimit: 210000,
    gasPrice: ethers.BigNumber.from("20000000000").toNumber(),
    // ethers.BigNumber("20000000000"),

    // ethers.utils.bigNumberify("20000000000"),

    to: "0x0Fb50728fBbe508f0414538B43a1dcEB7268DA6f",
    // ... or supports ENS names
    // to: "ricmoo.firefly.eth",
    
    //(node:1037) UnhandledPromiseRejectionWarning: Error: insufficient funds (version=4.0.13),所以将value设为0
    value: 0,
    data: "0x",

    // This ensures the transaction cannot be replayed on different networks
    // chainId: 
};

let signPromise = wallet.sign(transaction)

signPromise.then((signedTransaction) => {

    console.log(signedTransaction);
    //0xf865808504a817c80083033450947ddad6a67544efb0c51808c77009a7b98cc8163080801ca0ae2b8b042371a68d2e00b3ad5949575e24428f0eb432d3094af4d72ee0cc63fea04de5df55127c7e9d9dedaa8d754afbb14fc32686ea31cfa01d1d06409dcf24be

    customHttpProvider.sendTransaction(signedTransaction).then((tx) => {

        console.log(tx);
        // {
        //    // These will match the above values (excluded properties are zero)
        //    "nonce", "gasLimit", "gasPrice", "to", "value", "data", "chainId"
        //
        //    // These will now be present
        //    "from", "hash", "r", "s", "v"
        //  }
        // Hash:
        
        // { nonce: 0,
        //   gasPrice: BigNumber { _hex: '0x04a817c800' },
        //   gasLimit: BigNumber { _hex: '0x033450' },
        //   to: '0x7DdaD6a67544efB0c51808c77009a7B98Cc81630',
        //   value: BigNumber { _hex: '0x00' },
        //   data: '0x',
        //   chainId: 0,
        //   v: 28,
        //   r:
        //    '0xae2b8b042371a68d2e00b3ad5949575e24428f0eb432d3094af4d72ee0cc63fe',
        //   s:
        //    '0x4de5df55127c7e9d9dedaa8d754afbb14fc32686ea31cfa01d1d06409dcf24be',
        //   from: '0x3455f15cc11F2E77c055f931A6C918ccc7c18fd8',
        //   hash:
        //    '0xb48c1995addcf3268bdbe1a33878b7048de1fbfd5bc2ccb571ce63d2a4ab8953',
        //   wait: [Function] }
    }).catch((e) => {
        console.log(e);
    });
}).catch((e) => {
    console.log(e);
});