import sys
import websocket
from plugin import AntiRecall


def on_message(_ws, message):
    PluginAntiRecall.on_message(_ws, message)


def on_open(_ws):
    PluginAntiRecall.on_open(_ws)


if __name__ == '__main__':
    websocket.enableTrace(False)
    data = sys.argv
    name = data[data.index('--name') + 1]
    key = data[data.index('--key') + 1]
    uri = "ws://127.0.0.1:8202/wx?name=" + name + "&key=" + key
    ws = websocket.WebSocketApp(uri, on_open=on_open, on_message=on_message)
    PluginAntiRecall = AntiRecall(uri)
    ws.run_forever()
