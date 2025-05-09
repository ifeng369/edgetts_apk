from io import BytesIO
import edge_tts
from flask import Flask, Response, json,request
from urllib.parse import unquote
# from waitress import serve

app = Flask(__name__)
VOICES = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoyiNeural", 
    "zh-CN-YunjianNeural", 
    "zh-CN-YunxiNeural",
    "zh-CN-YunxiaNeural",
    "zh-CN-YunyangNeural",
]


@app.route('/', methods=['POST'])
async def hello_world():

    data = json.loads(request.data)

    voiceIndex = int(data.get('voice', "0"))
    text = unquote(data.get('text', "哇哈哈"))
    rate = data.get('speed', "0")
    volume = data.get('volume', "0")
    # print(text)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
    # serve(app, host="0.0.0.0", port=5000)


