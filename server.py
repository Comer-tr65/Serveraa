import asyncio
import websockets
import json

connections = {}   # {websocket: {"x": int, "y": int, "id": str}}

async def handler(websocket, path):
    pid = str(id(websocket))   # генерируем ID игрока
    connections[websocket] = {"x": 100, "y": 100, "id": pid}

    # отправляем новому игроку его ID
    await websocket.send(json.dumps({"your_id": pid}))

    try:
        async for msg in websocket:
            data = json.loads(msg)

            # обновляем позицию
            connections[websocket]["x"] = data["x"]
            connections[websocket]["y"] = data["y"]

            # формируем список игроков
            players = {c["id"]: {"x": c["x"], "y": c["y"]} for c in connections.values()}

            # рассылаем всем
            for conn in list(connections.keys()):
                try:
                    await conn.send(json.dumps(players))
                except:
                    pass
    except:
        pass
    finally:
        # удаляем игрока при отключении
        if websocket in connections:
            del connections[websocket]
        players = {c["id"]: {"x": c["x"], "y": c["y"]} for c in connections.values()}
        for conn in list(connections.keys()):
            try:
                await conn.send(json.dumps(players))
            except:
                pass

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):  # Render ждёт порт 10000
        print("Сервер запущен на порту 10000")
        await asyncio.Future()  # бесконечный цикл

if __name__ == "__main__":
    asyncio.run(main())