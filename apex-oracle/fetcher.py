import requests, time, json
from datetime import datetime
COINGECKO_API = "https://api.coingecko.com/api/v3"
GITHUB_API = "https://api.github.com/repos"
REPO_MAP = {"bitcoin": "bitcoin/bitcoin","ethereum": "ethereum/go-ethereum","monero": "monero-project/monero","cardano": "IntersectMBO/cardano-node","litecoin": "litecoin-project/litecoin"}
class ApexFetcher:
    def __init__(self, p="apex-oracle/config.json"):
        import json; self.coins=json.load(open(p))["top_decentralized_coins"]
    def fetch_market_data(self):
        try: return requests.get(f"{COINGECKO_API}/coins/markets?vs_currency=usd&ids={','.join(self.coins)}",timeout=15).json()
        except: return []
    def get_snapshot(self):
        print("Fetching Top 5..."); snap=[]
        for m in self.fetch_market_data():
            cid=m["id"]; snap.append({"id":cid,"symbol":m["symbol"],"price":m["current_price"],"tps_estimate":{"bitcoin":7,"ethereum":30,"monero":4,"cardano":250,"litecoin":56}.get(cid,10),"avg_fee_estimate":{"bitcoin":1.2,"ethereum":0.8,"monero":0.02,"cardano":0.15,"litecoin":0.02}.get(cid,0.1),"finality":{"bitcoin":3600,"ethereum":900,"monero":1200,"cardano":600,"litecoin":1800}.get(cid,1000)})
            time.sleep(1)
        return snap
