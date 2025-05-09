"""
edge tts
"""
import time
from toga.style.pack import COLUMN, ROW, CENTER
from io import BytesIO
from urllib.parse import unquote
import edge_tts
from flask import Flask, Response, json, jsonify, request
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading

VOICES = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoyiNeural", 
    "zh-CN-YunjianNeural", 
    "zh-CN-YunxiNeural",
    "zh-CN-YunxiaNeural",
    "zh-CN-YunyangNeural",
]
textList = [" "]*100
global label

def run_flask():
    app = Flask(__name__)

    @app.route('/tts', methods=['POST'])
    async def tts():
        global textList
        data = json.loads(request.data)
        voiceIndex = int(data.get('voice', "0"))
        text = unquote(data.get('text', "哇哈哈"))
        rate = data.get('speed', "0")
        volume = data.get('volume', "0")
        # print(text)
        text = text.strip()
        nowtime1 = time.strftime('%H:%M:%S', time.localtime(time.time()))
        textList.append(nowtime1+" "+text)
        textList = textList[-100:]

        output = '\n'.join(str(e) for e in reversed(textList))
        label.text = output

        communicate = edge_tts.Communicate(text, VOICES[voiceIndex],rate="+"+rate+"%",volume="+"+volume+"%")
        audio_buffer = BytesIO()
        metadata_buffer = BytesIO()

        async for message in communicate.stream():
            if message["type"] == "audio":
                audio_buffer.write(message["data"])
            elif message["type"] == "WordBoundary":
                metadata_buffer.write(json.dumps(message).encode("utf-8"))
                metadata_buffer.write(b"\n")

        audio_buffer.seek(0)
        metadata_buffer.seek(0)
        return Response(
            audio_buffer.getvalue(),
            mimetype="audio/wav",
        )
    @app.route('/')
    def get_data():
        return 'http://127.0.0.1:3000,{"method": "POST","body":{"voice":3,"speed":"{{speakSpeed*2}}","text":{{java.encodeURI(speakText)}}}}'

    app.run(host='0.0.0.0', port=3000)


class EdgeTTS(toga.App):

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # main_box = toga.Box()
        # textbox = toga.MultilineTextInput()
        # textbox.value ='http://127.0.0.1:3000/tts,{"method": "POST","body":{"voice":3,"speed":"{{speakSpeed*2}}","text":{{java.encodeURI(speakText)}}}}'
        # textbox.readonly = True
        global label
        global textList
        label = toga.Label("")
        # button = toga.Button('一键导入tts源', on_press=self.button_handler,style=Pack(flex=1))
        main_box = toga.Box(
            children=[label],
        )
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        nowtime1 = time.strftime('%H:%M:%S', time.localtime(time.time()))
        textList.append(nowtime1+" "+"启动 http://127.0.0.1:3000")
        textList = textList[-100:]
        output = '\n'.join(str(e) for e in reversed(textList))
        label.text = output

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 设为守护线程，避免主线程退出后阻塞
    flask_thread.start()
    return EdgeTTS()
