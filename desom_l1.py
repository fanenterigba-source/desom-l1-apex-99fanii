import time
h=0; s=21000000.0
print("CLOUD9 MATE 8001 - Box 1/2/4/9 LIVE - DHN 21/21")
while True:
 h+=1; s-=0.2
 msg=f"[Block {h}] DHN breathing 21/21 - Supply {s:.1f} - Box Game LIVE"
 print(msg, flush=True)
 time.sleep(3)
