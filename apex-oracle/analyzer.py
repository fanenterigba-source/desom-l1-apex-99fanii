import json
class ApexAnalyzer:
    def __init__(self, p="apex-oracle/desom_current_stats.json"):
        try: self.desom=json.load(open(p))
        except: self.desom={"tps":100,"finality":500,"avg_fee_usd":0.01}
    def analyze(self, snap):
        best_tps=max(s["tps_estimate"] for s in snap)
        best_finality=min(s["finality"] for s in snap)
        best_fee=min(s["avg_fee_estimate"] for s in snap)
        return {"targets":{"tps":round(best_tps*1.1,2),"finality":round(best_finality*0.9,2),"fee":round(best_fee*0.9,4)},"best":f"TPS {best_tps} -> DESOM must do {best_tps*1.1}"}
