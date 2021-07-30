
interface TYPE_CONFIG {
    [key: string]: {
        key: string;
        token: string;
        // 监控价格; [1, 5, 10] ==> 依次以数组第一个为基准
        basePrices: number[];
        // 用于计算涨跌幅度
        list: number[];
        alter: number[];
    }
}
// todo 涨跌比例、通知时间其余的也可以单独配置

// ! 只需要在此添加token, 监控价格
export let TOKEN_CONFIG: TYPE_CONFIG = {
    MBOX: {
        key: "MBOX",
        token: "0x3203c9e46ca618c8c1ce5dc67e7e9d75f5da2377",
        basePrices: [2, 2.1],
        list: [],
        alter: []
    },
    BTCST: {
        key: "BTCST",
        token: "0x78650b139471520656b9e7aa7a5e9276814a38e9",
        basePrices: [40, 50, 60],
        list: [],
        alter: []
    },
    DNXC: {
        key: "DNXC",
        token: "0x3c1748d647e6a56b37b66fcd2b5626d0461d3aa0",
        basePrices: [0.65, 0.7, 0.8],
        list: [],
        alter: []
    }
}