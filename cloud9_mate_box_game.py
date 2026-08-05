import asyncio, json
import websockets

async def handle(ws):
    await ws.send(json.dumps({"type":"welcome","msg":"☁️ CLOUD9 IMPERIUM MATE LIVE - Box Game 1/2/4/9","genesis":"21M FANEN - 21 humans breathe 3s","gifts":319,"cloud9":"350k Fanii $700 UNIVERSE"}))
    print("Creator connected!")
    async for message in ws:
        try:
            data=json.loads(message)
            gift=data.get("gift","Rose")
            fanii=data.get("fanii",50)
            print(f"🎁 {gift} - {fanii} Fanii - 100% Direct to Creator - Burn 0.2 FANEN")
            await ws.send(json.dumps({"type":"gift_animation","gift":gift,"fanii":fanii,"earn":f"{fanii} Fanii 100% Direct = {fanii/99:.2f}$ PalmPay","mode":"GOAT 22s" if fanii>500000 else "UNIVERSE 12s" if fanii>100000 else "ROSE 1s"}))
        except Exception as e:
            print(e)

async def breathing():
    height=0
    supply=21000000.0
    while True:
        height+=1
        supply-=0.2
        print(f"[Block {height}] DHN breathing 21/21 - Supply {supply:.1f} - Chain alive - No breath=No block=sleep")
        await asyncio.sleep(3)

async def main():
    asyncio.create_task(breathing())
    async with websockets.serve(handle, "0.0.0.0", 8001):
        print("🚀 CLOUD9 MATE WebSocket listening on ws://0.0.0.0:8001")
        print("Box Game 1/2/4/9 LIVE - Host can go Box Game!")
        await asyncio.Future()

asyncio.run(main())
