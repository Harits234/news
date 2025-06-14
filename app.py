import websocket
import threading
import json
import time
from queue import Queue

class DerivWebSocket:
    def __init__(self, symbol="frxXAUUSD"):
        self.url = "wss://ws.deriv.com/websockets/v3?app_id=1089"
        self.symbol = symbol
        self.ws = None
        self.queue = Queue()
        self.running = False

    def on_message(self, ws, message):
        data = json.loads(message)
        if "tick" in data:
            self.queue.put(data["tick"]["quote"])

    def on_open(self, ws):
        ws.send(json.dumps({
            "ticks": self.symbol,
            "subscribe": 1
        }))

    def on_error(self, ws, error):
        print("WS Error:", error)

    def on_close(self, ws, *args):
        print("WS Closed")

    def start(self):
        self.running = True
        def run():
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()
        threading.Thread(target=run).start()

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()

    def get_price(self):
        if not self.queue.empty():
            return self.queue.get()
        return None
