import asyncio, json, time, websockets

h=0
s=20999997.2
clients=set()

async def handler(ws):
    clients.add(ws)
    print(f"💧 Wallet connected! {len(clients)} clients")
    try:
        await ws.send(json.dumps({"type":"init","block":h,"supply":s,"dhn":"21/21","box":"1/2/4/9 LIVE"}))
        await ws.wait_closed()
    finally:
        clients.remove(ws)

async def broadcaster():
    global h,s
    print("☁️ CLOUD9 MATE 8001 WebSocket LIVE - Box Game 1/2/4/9")
    while True:
        h+=1
        s-=0.2
        msg = {
            "type":"block",
            "block":h,
            "supply":round(s,1),
            "dhn":"21/21",
            "msg":f"[Block {h}] DHN breathing 21/21 - Supply {s:.1f} - Box Game LIVE",
            "time":time.time()
        }
        # Write to log for backup
        with open("cloud9.log","a") as f:
            f.write(msg["msg"]+"\n")
        # Broadcast to all wallets
        if clients:
            dead=set()
            for ws in clients:
                try:
                    await ws.send(json.dumps(msg))
                except:
                    dead.add(ws)
            clients.difference_update(dead)
        print(msg["msg"], flush=True)
        await asyncio.sleep(3)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8001):
        await broadcaster()

asyncio.run(main())
