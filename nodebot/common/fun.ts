// 休眠 单位 秒
export function sleep(s: number) {
    return new Promise(resolve => setTimeout(resolve, s * 1000));
}