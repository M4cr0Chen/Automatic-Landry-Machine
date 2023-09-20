import pyaudio  # 导入pyAudio的源代码文件，我们下面要用到，不用到就不用导入啦
import wave
from aip import AipSpeech
import serial
# from playsound import playsound
ser = serial.Serial("com11", 9600)
APP_ID = '24939317'  # 新建AiPSpeech
API_KEY = 'GEw76MzM5FYAYtwFw050PB8z'
SECRET_KEY = '6POaqrGtjAS3ePGuMEAWmgsoQZgtPzFx'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def record():  # 定义函数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 量化位数
    CHANNELS = 1  # 采样管道数
    RATE = 16000  # 采样率
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"  # 文件保存的名称
    p = pyaudio.PyAudio()  # 创建PyAudio的实例对象
    stream = p.open(format=FORMAT,  # 调用PyAudio实例对象的open方法创建流Stream
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []  # 存储所有读取到的数据
    print('* 开始录音 >>>')  # 打印开始录音
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)  # 根据需求，调用Stream的write或者read方法
        frames.append(data)
    print('* 结束录音 >>>')  # 打印结束录音
    stream.close()  # 调用Stream的close方法，关闭流
    p.terminate()  # 调用pyaudio.PyAudio.terminate() 关闭会话
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 写入wav文件里面
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
def cognitive():  # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    result = client.asr(get_file_content('output.wav'), 'wav', 16000, {
        'dev_pid': 1537,  # 识别本地文件
    })
    result_text = result["result"][0]
    print("you said: " + result_text)
    return result_text
def speak(text=""):
    result = client.synthesis(text, 'zh', 1, {
        'spd': 4,
        'vol': 5,
        'per': 4,
    })
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
#
# def speak1()
#     playsound("audio.mp3")
while True:
    record()  # 录音模块
    result = cognitive()  # 百度识别结果
    for i in result:
        if i == "风": #风干模式
            ser.write(b'111')
        if i == "阳": #阳光模式
            ser.write(b'222')
        if i == "智": #人工智能
            ser.write(b'333')
    speak(result)  # 将百度识别结果转化成语音
    # speak1()6、