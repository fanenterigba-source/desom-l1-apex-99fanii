import asyncio, json, time, os
import websockets

# --- FANEN COIN L1 LEDGER ---
CHAIN_FILE = "fanen_ledger.json"
h=43
s=20999988.6
clients=set()

# Load or init ledger
if os.path.exists(CHAIN_FILE):
    with open(CHAIN_FILE) as f:
        ledger=json.load(f)
        balances=ledger.get("balances",{"Founder":20999988.6})
        h=ledger.get("height",43)
        s=ledger.get("supply",20999988.6)
else:
    balances={"Founder":20999988.6, "Fountain":0}
    # 21 DHN humans genesis
    for i in range(1,22):
        balances[f"DHN_{i}"]=1000.0

def save_ledger():
    with open(CHAIN_FILE,"w") as f:
        json.dump({"height":h,"supply":s,"balances":balances,"coin":"FANEN","type":"L1_NATIVE_COIN"},f,indent=2)

clients=set()

async def handler(ws):
    clients.add(ws)
    print(f"💰 Wallet connected - {len(clients)} - Balances: {len(balances)} holders")
    try:
        await ws.send(json.dumps({
            "type":"init",
            "block":h,
            "supply":s,
            "balances":balances,
            "coin":"FANEN",
            "msg":f"[Block {h}] FANEN COIN L1 - Supply {s} - {len(balances)} holders - COIN NOT TOKEN"
        }))
        async for raw in ws:
            try:
                data=json.loads(raw)
                if data.get("action")=="transfer":
                    frm=data.get("from","Founder").strip()
                    to=data.get("to","").strip()
                    amt=float(data.get("amount",0))
                    if not to or amt<=0:
                        await ws.send(json.dumps({"type":"error","msg":"Invalid to/amount"}))
                        continue
                    if balances.get(frm,0) < amt:
                        await ws.send(json.dumps({"type":"error","msg":f"Insufficient FANEN COIN - {frm} has {balances.get(frm,0)}"}))
                        continue
                    # COIN TRANSFER - L1 NATIVE
                    balances[frm]=round(balances.get(frm,0)-amt,6)
                    balances[to]=round(balances.get(to,0)+amt,6)
                    save_ledger()
                    print(f"💸 COIN TRANSFER {frm} -> {to} : {amt} FANEN COIN")
                    # Broadcast to all
                    msg=json.dumps({"type":"coin_tx","from":frm,"to":to,"amount":amt,"balances":balances,"msg":f"💸 {frm} -> {to} : {amt} FANEN COIN L1 TRANSFER"})
                    for c in list(clients):
                        try: await c.send(msg)
                        except: clients.discard(c)
            except Exception as e:
                print(f"tx err {e}")
    finally:
        clients.discard(ws)

async def broadcaster():
    global h,s
    print("☁️ CLOUD9 MATE 8001 - FANEN COIN L1 - WS LIVE")
    while True:
        h+=1
        s=round(s-0.01,6) # burn fee
        save_ledger()
        data=json.dumps({"type":"block","block":h,"supply":s,"balances":balances,"msg":f"[Block {h}] DHN 21/21 - Supply {s} FANEN COIN - {len(balances)} holders - L1 NATIVE"})
        for ws in list(clients):
            try: await ws.send(data)
            except: clients.discard(ws)
        print(f"[Block {h}] FANEN COIN {s} - {len(clients)} wallets",flush=True)
        await asyncio.sleep(3)

async def main():
    save_ledger()
    async with websockets.serve(handler,"0.0.0.0",8001):
        print(f"💰 FANEN COIN L1 WS 0.0.0.0:8001 - GENESIS {s} - COIN NOT TOKEN")
        await broadcaster()

asyncio.run(main())
