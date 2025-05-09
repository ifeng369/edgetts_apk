EdgeTTS
=======


基于 Briefcase，edge-tts，flask开发的语音合成软件。

食用方式：安装apk文件，在安卓设备上运行。添加后台白名单，电池策略调整为：允许后台高耗电。
阅读APP添加朗读引擎：
    名称: 随意

    URL: http://127.0.0.1:3000,{"method": "POST","body":{"voice":3,"speed":"{{speakSpeed*2}}","text":{{java.encodeURI(speakText)}}}}

voice: 0-5，对应以下语音列表
    ["zh-CN-XiaoxiaoNeural","zh-CN-XiaoyiNeural","zh-CN-YunjianNeural", "zh-CN-YunxiNeural","zh-CN-YunxiaNeural","zh-CN-YunyangNeural"]


