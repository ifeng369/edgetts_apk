EdgeTTS
=======


基于 Briefcase，edge-tts，flask开发的语音合成软件。

下载地址： https://github.com/ifeng369/edgetts_apk/releases/latest/download/app-debug.apk


食用方式：安装并运行apk文件。添加后台白名单，电池策略调整为：允许后台高耗电。
阅读APP添加朗读引擎：

名称: ``随意``

URL: 
``http://127.0.0.1:3000,{"method": "POST","body":{"voice":3,"speed":"{{speakSpeed*2}}","text":{{java.encodeURI(speakText)}}}}``

voice: 0-5，对应以下语音列表
    0. "zh-CN-XiaoxiaoNeural"
    1. "zh-CN-XiaoyiNeural"
    2. "zh-CN-YunjianNeural"
    3. "zh-CN-YunxiNeural"
    4. "zh-CN-YunxiaNeural"
    5. "zh-CN-YunyangNeural"


