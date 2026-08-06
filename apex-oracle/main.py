import json
from fetcher import ApexFetcher
from analyzer import ApexAnalyzer
from self_upgrader import SelfUpgrader
print("=== DESOM APEX ORACLE v2 - SELF-UPGRADING ===")
f=ApexFetcher()
snap=f.get_snapshot()
analysis=ApexAnalyzer().analyze(snap)
dip=SelfUpgrader().apply(analysis,snap)
print(json.dumps(dip,indent=2))
print("\nSUCCESS! DESOM now knows how to beat Top 5!")
