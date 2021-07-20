const { ethers } = require("ethers");
const fs = require("fs");

async function main() {
    const provider = new ethers.providers.JsonRpcProvider(
        "https://bsc-dataseed1.binance.org",
    );
    const filter = {
        topics: [ethers.utils.id("Transfer(address,address,uint256)")],
    };
    const counter = {};
    // console.log("----->", provider)

    provider.on(filter, async (log) => {
        if (!counter[log.address]) {
            counter[log.address] = 1;
        } else {
            counter[log.address] += 1;
        }
    });

    const t1 = Date.now();
    async function getTokenName(address) {
        const abi = [
            {
                constant: true,
                inputs: [],
                name: "name",
                outputs: [{ internalType: "string", name: "", type: "string" }],
                payable: false,
                stateMutability: "view",
                type: "function",
            },
        ];
        const token = new ethers.Contract(address, abi, provider);
        console.log(token);
        return token.name();
    }

    const token = await getTokenName("0x17b7163cf1dbd286e262ddc68b553d899b93f526");
    console.log("----->>>", token);
    // setInterval(async () => {
    //     const lines = [];
    //     console.log("======>>", counter);
    //     for (let addr in counter) {
    //         const name = await getTokenName(addr);
    //         lines.push([addr, name, counter[addr]]);
    //     }
    //     lines.sort((a, b) => b[1] - a[1]);
    //     fs.writeFile("./counter.csv", lines.join("\n"));
    //     const elapsed = (Date.now() - t1) / (60 * 1000);
    //     console.log(`saved after ${elapsed} minutes, tokens: ${lines.length}`);
    // }, 1000);
}

main()
.then(() => console.log('done'))
.catch(e => console.error(e))
