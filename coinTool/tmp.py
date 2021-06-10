dic = {"total": 1,
       "data": [
           {
               "id": "0xe7cb24f449973d5b3520e5b93d88b405903c75fb-bsc",
               "address": "0xe7cb24f449973d5b3520e5b93d88b405903c75fb",
               "symbol": "BNBTC", "name": "BNbitcoin Token - minable bitcoin on BSC",
               "description": "BNbitcoin Token - minable bitcoin on BSC/BNBTC",
               "txns24h": 495,
               "txns24hChange": -0.013392857142857142,
               "verified": "false",
               "decimals": 8,
               "volume24h": 110699.82852786034,
               "volume24hUSD": 25540.09183004585,
               "volume24hETH": 487.75722781235174,
               "volumeChange24h": -0.018718666273723258,
               "liquidityUSD": 7079.715193050582,
               "liquidityETH": 135.20633673685347,
               "liquidityChange24h": 0.32875759817057704,
               "logoURI": "null",
               "priceUSD": 0.23071482738221277,
               "priceETH": 0.004406124510749315,
               "priceChange24h": 0.035482505616534,
               "priceUSDChange24h": 0.035482505616534,
               "priceETHChange24h": -0.014550620767458358,
               "timestamp": 0, "blockNumber": 10008555,
               "AMM": "pancakeswap",
               "network": "bsc"
           },
           {
               "id": "0xe7cb24f449973d5b3520e5b93d88b405903c75fb-bsc",
               "address": "1234",
               "symbol": "BNBTC", "name": "BNbitcoin Token - minable bitcoin on BSC",
               "description": "BNbitcoin Token - minable bitcoin on BSC/BNBTC",
               "txns24h": 495,
               "txns24hChange": -0.013392857142857142,
               "verified": "false",
               "decimals": 8,
               "volume24h": 110699.82852786034,
               "volume24hUSD": 25540.09183004585,
               "volume24hETH": 487.75722781235174,
               "volumeChange24h": -0.018718666273723258,
               "liquidityUSD": 7079.715193050582,
               "liquidityETH": 135.20633673685347,
               "liquidityChange24h": 0.32875759817057704,
               "logoURI": "null",
               "priceUSD": 0.23071482738221277,
               "priceETH": 0.004406124510749315,
               "priceChange24h": 0.035482505616534,
               "priceUSDChange24h": 0.035482505616534,
               "priceETHChange24h": -0.014550620767458358,
               "timestamp": 0, "blockNumber": 10008555,
               "AMM": "pancakeswap",
               "network": "bsc"
           },

       ]}


addressList = dic["data"]

# for item in addressList:
#     if item["address"] == "1234":
#         print(item["priceUSD"])


tu = ()

import sys

gpus =  "h" if len(sys.argv) > 1 else ""
print("传入参数----->>", gpus)