import hashlib, time, json, os, random
from flask import Flask, request, jsonify
from flask_cors import CORS
DIFFICULTY=3
chain=[];mempool=[];wallets={};open_drops=[]
def calc_hash(i,ph,txs,n,ts):
    import json as js
    return hashlib.sha256(f"{i}{ph}{js.dumps(txs,sort_keys=True)}{n}{ts}".encode()).hexdigest()
def ensure(u):
    if u not in wallets:
        wallets[u]={"coin":1.0,"koin":50000.0}
        if u in ["FANENTER","Nayla","Lukey"]: wallets[u]={"coin":5.0,"koin":50000.0}
    return wallets[u]
gen_hash=calc_hash(0,"0"*64,[{"type":"GENESIS","msg":"DeSoM V16 TRACKING PoW for 8.5B"}],"0",time.time())
chain.append({"index":0,"prev_hash":"0"*64,"txs":[{"type":"GENESIS"}],"hash":gen_hash,"nonce":0})
app=Flask(__name__); CORS(app)
@app.route("/")
def home():
    return jsonify({"DeSoM":"V16.0 DHN PoW TRACKING EDITION","Coin":"FANEN tradable 1= $10k = 50k Koin","Koin":"gifters gift creators","chain_len":len(chain),"top6_self_evolving":["BTC","XMR","LTC","BCH","DOGE","ETH"]})
@app.route("/wallet/<u>")
def w(u): ensure(u); return jsonify(wallets[u])
@app.route("/transfer/koin/targeted",methods=["POST"])
def koin_target():
    d=request.get_json(); f,t,a=d["from"],d["to"],int(d["amount"]); ensure(f); ensure(t)
    if wallets[f]["koin"]<a: return jsonify({"error":"insufficient Koin"}),400
    wallets[f]["koin"]-=a; wallets[t]["koin"]+=a
    code=f"TGT{random.randint(100000,999999)}"
    return jsonify({"status":"TARGETED exclusive - only @"+t+" gets it, new balance popup","code":code,"to_balance":wallets[t],"link":f"desom://transfer?to={t}&amount={a}&code={code}"})
@app.route("/gift",methods=["POST"])
def gift():
    d=request.get_json(); f,t,k=d["from"],d["to"],int(d["koin"]); ensure(f); ensure(t)
    if wallets[f]["koin"]<k: return jsonify({"error":"low"}),400
    wallets[f]["koin"]-=k; wallets[t]["koin"]+=k
    league="A" if k>=8001 else "B" if k>=5001 else "C"
    badge="A1" if k>=10000 else "001" if league=="A" else "01"
    return jsonify({"gift":k,"league":league,"badge":badge,"banner":k>=10000,"x5_views":k>=10000,"msg":f"Gift {k} Koin League {league} - gifters gift creators"})
if __name__=="__main__":
    print("DeSoM V16 TRACKING PoW for 8.5B starting on port 8000 with CORS")
    app.run(host="0.0.0.0",port=8000)
