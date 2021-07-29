## 项目说明

### 一、基本使用

**版本说明**

```ts
% node -v
v12.22.3
% tsc -v
Version 4.3.5
```

**安装依赖**

```ts
// 下载包
% npm i 
// 执行
% ts-node index.ts
```

**目录说明**

```ts
% tree -L 3
.
├── README.md
├── common
│   ├── config.ts      // 需要监控的，在该文件下，添加配置即可
│   ├── const.ts    // 常量
│   ├── fun.ts  // 函数
│   ├── ifttt.ts // ifttt通知
│   ├── log4.ts // 日志
│   └── net.ts // 网络请求
├── index.ts // 入口文件
├── logs // 日志文件
│   ├── BTCST.-2021-07-29.log
│   └── MBOX.-2021-07-29.log
├── package-lock.json
├── package.json
└── test.ts 

```

**启动配置**

[pancake-info-api](https://github.com/pancakeswap/pancake-info-api)需要用到梯子；需要以下配置

1. common/const.ts： 配置本地代理
2. 终端启动
   1. 在小飞机的配置项目找到 ： **复制终端代理命令** 
   2. 终端执行上一步的**复制终端代理命令**
   3. ts-node index.ts

### 二、交易相关

#### 2.1 安全配置
