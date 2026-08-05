import os, json, asyncio, time
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading
import websockets

PORT = int(os.environ.get("PORT", 10000))
LEDGER = "fanen_ledger.json"

# Load ledger
if os.path.exists(LEDGER):
    with open(LEDGER) as f:
        ledger = json.load(f)
else:
    ledger = {"height": 405, "supply": 20999984.98, "balances": {"Founder": 20998984.98, "Fa Nen Ter": 1000}, "txs": []}

balances = ledger.get("balances", {})
height = ledger.get("height", 405)
clients = set()

async def ws_handler(websocket):
    global height, balances
    clients.add(websocket)
    try:
        await websocket.send(json.dumps({"type":"info","msg":f"[Block {height}] FANEN COIN L1 - Supply {sum(balances.values()):.2f} - {len(balances)} holders - COIN NOT TOKEN","block":height}))
        async for msg in websocket:
            try:
                data = json.loads(msg)
                if data.get("action")=="transfer":
                    frm = data.get("from","Founder")
                    to = data.get("to")
                    amt = float(data.get("amount",0))
                    if to and amt>0 and balances.get(frm,0)>=amt:
                        balances[frm]-=amt
                        balances[to]=balances.get(to,0)+amt
                        height+=1
                        ledger["height"]=height
                        ledger["balances"]=balances
                        with open(LEDGER,"w") as f:
                            json.dump(ledger,f,indent=2)
                        out = f"[Block {height}] {frm} -> {to} : {amt} FANEN COIN - {len(balances)} holders"
                        print(out)
                        for c in list(clients):
                            try: await c.send(json.dumps({"type":"coin_tx","msg":out,"block":height}))
                            except: pass
            except Exception as e:
                print("WS err",e)
    finally:
        clients.discard(websocket)

async def ws_main():
    async with websockets.serve(ws_handler, "0.0.0.0", PORT):
        await asyncio.Future()

# HTTP server in thread
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def http_thread():
    # Serve on same PORT? Can't. So we serve HTTP via same asyncio? Use different - Render only exposes PORT, so we use WS only on PORT and HTTP via WS fallback - but we hack: run HTTP on PORT, WS on 8001 not exposed, so we make faucet use polling.
    # For now: simple http on PORT
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"HTTP live on {PORT} - Block {height}")
        httpd.serve_forever()

# Actually run HTTP, WS will be handled via separate port if Render allows? Render only 1 port, so we prioritize HTTP + ledger API
# New approach: HTTP server serves ledger, faucet uses REST not WS

if __name__=="__main__":
    # Start WS in background on 8001 if possible
    threading.Thread(target=lambda: asyncio.run(ws_main()), daemon=True).start()
    # HTTP on PORT
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"FANEN COIN L1 LIVE Block {height} HTTP {PORT} WS 8001 - COIN NOT TOKEN")
        httpd.serve_forever()
