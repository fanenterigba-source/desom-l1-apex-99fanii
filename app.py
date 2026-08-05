import json, os, hashlib, time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 10000))
FAUCET_AMOUNT = 7
FAUCET_CAP = 18000
MINE_REWARD = 1
MINE_COOLDOWN = 30

LEDGER_FILE = "ledger.json"
TOTAL_FILE = "faucet_total.txt"

def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return {"height": 407, "balances": {"Founder": 20998984.98, "Fa Nen Ter": 500, "Chidi": 50}, "balances_fanii": {}, "last_mine": {}}
    with open(LEDGER_FILE) as f:
        data = json.load(f)
        if "balances_fanii" not in data: data["balances_fanii"] = {}
        if "last_mine" not in data: data["last_mine"] = {}
        return data

def save_ledger(l):
    with open(LEDGER_FILE, "w") as f:
        json.dump(l, f)

def get_total():
    if not os.path.exists(TOTAL_FILE): return 0
    try:
        with open(TOTAL_FILE) as f: return int(f.read().strip() or 0)
    except: return 0

def add_total(a):
    t = get_total() + a
    with open(TOTAL_FILE, "w") as f: f.write(str(t))
    return t

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode() if length else "{}"
        try: data = json.loads(body)
        except: data = {}
        if parsed.path == "/api/faucet":
            to = data.get("to") or data.get("address")
            if not to:
                self.send_response(400); self.end_headers(); return
            ledger = load_ledger()
            bal = ledger["balances"]
            if to in bal:
                self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
                self.wfile.write(json.dumps({"error":"already claimed","balance":bal[to]}).encode()); return
            if bal.get("Founder",0) < FAUCET_AMOUNT:
                self.send_response(400); self.end_headers(); return
            total = get_total()
            if total + FAUCET_AMOUNT > FAUCET_CAP:
                self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": f"Faucet ended! {total}/18000 given. Now MINE FANII to earn!", "total": total, "cap": FAUCET_CAP}).encode())
                return
            bal["Founder"] -= FAUCET_AMOUNT
            bal[to] = bal.get(to,0)+FAUCET_AMOUNT
            add_total(FAUCET_AMOUNT)
            ledger["height"] = ledger.get("height",407)+1
            ledger["balances"] = bal
            save_ledger(ledger)
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "to": to, "amount": FAUCET_AMOUNT, "block": ledger["height"], "holders": len(bal), "total_given": get_total()}).encode())
            print(f"[Block {ledger['height']}] Founder -> {to} {FAUCET_AMOUNT} FANEN")
            return
        if parsed.path == "/api/mine":
            addr = data.get("to") or data.get("address")
            if not addr:
                self.send_response(400); self.end_headers(); return
            ledger = load_ledger()
            now = time.time()
            last = ledger.get("last_mine",{}).get(addr,0)
            if now - last < MINE_COOLDOWN:
                self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": f"Cooldown! Wait {int(MINE_COOLDOWN-(now-last))}s", "wait": int(MINE_COOLDOWN-(now-last))}).encode())
                return
            fanii_bal = ledger.get("balances_fanii",{})
            fanii_bal[addr] = fanii_bal.get(addr,0) + MINE_REWARD
            ledger["balances_fanii"] = fanii_bal
            ledger["last_mine"][addr] = now
            ledger["height"] += 1
            save_ledger(ledger)
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "to": addr, "reward": MINE_REWARD, "token": "FANII", "balance": fanii_bal[addr], "block": ledger["height"]}).encode())
            print(f"[MINE {ledger['height']}] {addr} +{MINE_REWARD} FANII")
            return
        return super().do_POST()
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/ledger":
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(json.dumps(load_ledger()).encode()); return
        if parsed.path == "/api/stats":
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            ledger = load_ledger()
            self.wfile.write(json.dumps({"height": ledger["height"], "faucet_total": get_total(), "faucet_cap": FAUCET_CAP, "faucet_remaining": FAUCET_CAP-get_total(), "holders": len(ledger["balances"]), "fanii_holders": len(ledger.get("balances_fanii",{})), "fanen_supply": 21000000}).encode()); return
        return super().do_GET()
    def log_message(self, *a):
        pass

print(f"FANEN COIN L1 WORLD LIVE - Block {load_ledger()['height']} - PORT {PORT} - V15-B FANII MINING")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
