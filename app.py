FAUCET_AMOUNT=7
FAUCET_CAP=18000
FAUCET_TOTAL_FILE="faucet_total.txt"

def get_total():
    try:
        return float(open(FAUCET_TOTAL_FILE).read() or 0)
    except:
        return 0
def add_total(a):
    t=get_total()+a
    open(FAUCET_TOTAL_FILE,'w').write(str(t))
    return t


import os, json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading

PORT = int(os.environ.get("PORT", 10000))
LEDGER = "fanen_ledger.json"

def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            return json.load(f)
    return {"height": 407, "balances": {"Founder": 20998984.98, "Fa Nen Ter": 500, "Chidi": 50}, "supply": 20999984.98}

def save_ledger(l):
    with open(LEDGER, "w") as f:
        json.dump(l, f, indent=2)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/claim":
            qs = parse_qs(parsed.query)
            to = qs.get("to", [None])[0]
            if not to:
                self.send_response(400); self.end_headers(); self.wfile.write(b'need?to=NAME'); return
            ledger = load_ledger()
            bal = ledger["balances"]
            if to in bal:
                self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
                self.wfile.write(json.dumps({"error":"already claimed","balance":bal[to]}).encode()); return
            if bal.get("Founder",0) < 50:
                self.send_response(400); self.end_headers(); return
            bal["Founder"] -= 50
            # CAP CHECK 18,000
    total = get_total()
    if total + 7 > FAUCET_CAP:
        self.wfile.write(json.dumps({"ok": False, "error": f"Faucet ended! {total}/18000 given. Now MINE to earn!"}).encode())
        return
    bal[to] = bal.get(to,0)+7
    add_total(7)
            ledger["height"] = ledger.get("height",407)+1
            ledger["balances"] = bal
            save_ledger(ledger)
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "to": to, "amount": 7, "block": ledger["height"], "holders": len(bal)}).encode())
            print(f"[Block {ledger['height']}] Founder -> {to} 50 FANEN - {len(bal)} holders")
            return
        if parsed.path == "/api/ledger":
            self.send_response(200); self.send_header("Content-type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.end_headers()
            self.wfile.write(json.dumps(load_ledger()).encode()); return
        return super().do_GET()

    def log_message(self, *a):
        pass

print(f"FANEN COIN L1 WORLD LIVE - Block {load_ledger()['height']} - PORT {PORT} - COIN NOT TOKEN")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
