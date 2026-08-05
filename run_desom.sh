pkill -f desom_l1.py
pkill -f "http.server 8080"
echo "🚀 DeSoM V13.4 - Starting ALL in 1..."
cat > desom_l1.py << 'PY'
import time
h=0; s=21000000.0
print("CLOUD9 MATE 8001 - Box 1/2/4/9 LIVE - DHN 21/21")
while True:
 h+=1; s-=0.2
 msg=f"[Block {h}] DHN breathing 21/21 - Supply {s:.1f} - Box Game LIVE"
 print(msg, flush=True)
 time.sleep(3)
PY
python desom_l1.py > cloud9.log 2>&1 &
echo "☁️ CLOUD9 MATE 8001 PID $! - Box Game LIVE"
python -m http.server 8080 > fountain.log 2>&1 &
echo "💧 Fountain Wallet http://localhost:8080 PID $!"
sleep 1
echo "✅ ALL IN 1 SESSION LIVE!"
cat cloud9.log
