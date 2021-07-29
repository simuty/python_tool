// proxy
export const HOST = "localhost"
export const PORT = "7890"

// 获取token价格的时间间隔
export const INTERVAL_GET_PRICE = 30

/* ---------------- judge ---------------- */
// 数组长度，避免重复推送; 达到阀值连续通知5次之后，判断：比例、时间间隔
export const BASE_ARRAY_LENGTH = 5
// 涨跌比例
export const RATIO_UP = 10
export const RATIO_DOWN = -10
// 间隔时间
export const INTERVAL_MINTUS = 0.5




