import ftplib
from pynput.keyboard import Listener, Key
import pyperclip

import important
"""
==============important.py===============
url = 'Your FTP address'
id = 'Your FTP ID'
pw = 'Your FTP password'
port = 'Your FTP port number'
==========================================
"""

url = important.url
id = important.id
pw = important.pw
port = important.port

session = ftplib.FTP()
session.connect(url, port=port, timeout=3600)
session.login(id, pw)
Folder = '/HDD1/services/copyPaste'

try:
    session.cwd(Folder)
except FileNotFoundError:
    session.mkd(Folder)
    session.cwd(Folder)


def reconnect():
    session.connect(url, port=port, timeout=3600)
    session.login(id, pw)
    session.cwd(Folder)


def download(fileName):
    try:
        with open('local' + fileName, 'wb') as f:
            session.retrbinary('RETR ' + fileName, f.write)
    except:
        pass


def read(fileName):
    with open('local' + fileName, 'r', encoding='utf-8') as f:
        readMessage = f.read()
        return readMessage


def write(fileName, sentence):
    with open('local' + fileName, 'w', encoding='utf-8') as f:
        print(sentence)
        sentence = sentence.replace("\n", "")
        f.write(sentence)


def upload(fileName):
    with open('local' + fileName, 'rb') as f:
        session.storbinary('STOR ' + fileName, f)


def copy():
    reconnect()
    write('copied.txt', str(pyperclip.paste()))
    upload('copied.txt')

    print('uploaded')


def paste():
    reconnect()
    download('copied.txt')
    copied = read('copied.txt')
    pyperclip.copy(copied)

    print(copied)
    print('downloaded')


"""
Upload when you release shift key, download when you release alt_l key

To use, 
1: Press 'ctrl + c' to copy
2: Press 'shift' to upload
3: Press 'alt_l' to download in another device
4: Press 'ctrl + v' to paste
"""


def on_release(key):
    if key == Key.shift:
        copy()
        pass
    elif key == Key.alt_l:
        paste()


with Listener(on_release=on_release) as listener:
    listener.join()



