import json, os
from datetime import datetime
class SelfUpgrader:
    def apply(self, analysis, snapshot):
        dip={"dip_id":f"DIP-{datetime.now().strftime('%Y%m%d-%H%M')}","created_at":datetime.utcnow().isoformat(),"reason":"Auto-upgrade to beat Top 5 decentralized L1s","targets":analysis["targets"],"snapshot":snapshot}
        os.makedirs("apex-oracle/proposals",exist_ok=True)
        open(f"apex-oracle/proposals/{dip['dip_id']}.json","w").write(json.dumps(dip,indent=2))
        open("apex-oracle/latest_dip.json","w").write(json.dumps(dip,indent=2))
        print(f"[UPGRADER] Created proposal {dip['dip_id']}.json")
        return dip
