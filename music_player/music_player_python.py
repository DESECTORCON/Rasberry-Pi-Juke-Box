import serial, sys
import os, random
import subprocess
from subprocess import call
import threading, pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3])

def say_this(this):
    engine.say(this)
    engine.runAndWait()

say_this("주크박스에 오신것을 환영합니다.")
say_this('시리얼 커낵팅... 잠심만 기다려 주십시오')
ser = serial.Serial('/dev/cu.usbserial-AC01RUCV', 9600)

if (ser):
    print("Serial port " + ser.portstr + " opened.")

say_this('시리얼 포트에 연결 완료.')
say_this('노래재생 준비중.')
audio_files = []
for root, dirs, files in os.walk("./music", topdown=False):
    for name in files:
        if name.endswith('.mp3'):
            audio_files.append(os.path.join(root, name))

def music_player():
    global play_music
    play_music = False
    while True:
        if play_music:
            random_file = str(random.sample(audio_files, 1)[0])
            print(random_file)
            subprocess.call(["afplay", random_file], shell=False)

music_player_thread = threading.Thread(target=music_player)
music_player_thread.setDaemon(True)
music_player_thread.start()

say_this('준비가 완료 되었습니다.')

while True:
    input_ = str(ser.read())
    print(input_)
    if not input_ == '' or not input_ == None:
        if input_ == "b'P'":
            # subprocess.call(["ffplay", "-nodisp", "-autoexit", "/music"])
            # random_file = str(random.sample(audio_files, 1)[0])
            # print(random_file)
            
            os.system(' osascript -e "set Volume 3"')
            say_this('노래를 재생합니다.')
            # subprocess.call(["afplay", random_file], shell=False)
            # continue
            play_music = True

        elif input_ == "b'S'":
            play_music = False
            say_this('노래를 멈춥니다.')
            os.system(' osascript -e "set Volume 0"')
        
        elif input_ == "b'Q'":
            say_this('시스탬 종료중.. 이용해주셔서 감사합니다.')
            os.system(' poweroff')
