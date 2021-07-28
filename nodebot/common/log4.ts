import { configure, getLogger } from "log4js";

export function logger(filename: string) {
    configure({
        appenders: {
            cheese: {
                type: 'dateFile',
                filename: `logs/${filename}`,
                pattern: "-yyyy-MM-dd.log",
                alwaysIncludePattern: true,
                category: 'normal'
            }
        },
        categories: { default: { appenders: ['cheese'], level: 'debug' } }
    });
    return getLogger('cheese');
}

// 使用实例
// const btcLog = logger("btc")
// btcLog.info({key: "btc", value: 1000000})
// const ethLog = logger("eth")
// ethLog.info({key: "eth", value: 1000000})

