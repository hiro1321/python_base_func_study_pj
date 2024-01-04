import configparser
from ..exception.FuncException import FuncException
import sys
import hashlib
import base64
import os


def execute():
    #  処理を選択 登録 or 承認
    print("処理を選択してください。")
    func_type = input("1:パスワード登録 2:パスワード認証")
    if func_type == "1":
        register_pw()
    elif func_type == "2":
        auth_pw()
    else:
        raise FuncException("想定外の値が入力されました")


def register_pw():
    pw = input("登録するパスワードを入力してください")
    conf = configparser.ConfigParser()
    conf.read("./UserInfo.ini")
    salt = base64.b64encode(os.urandom(32))
    hashed_pw = get_hased_password(pw, salt)
    # iniファイルの書き換え
    conf["USER_INFO"]["password"] = hashed_pw
    conf["USER_INFO"]["salt"] = str(salt)
    with open("./UserInfo.ini", "w") as inifile:
        conf.write(inifile)


def auth_pw():
    input_pw = input("パスワードを入力してください")
    conf = configparser.ConfigParser()
    conf.read("./UserInfo.ini")
    salt = encode_to_bytes(conf["USER_INFO"]["salt"])
    hashed_pw = conf["USER_INFO"]["password"]
    input_hashed_pw = get_hased_password(input_pw, salt)
    print(input_hashed_pw)
    print(hashed_pw)
    if hashed_pw == input_hashed_pw:
        print("パスワードの認証に成功しました！")
    else:
        print("NG！！！パスワードが違います")


def get_hased_password(pw, salt):
    return str(hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, 100000).hex())


def encode_to_bytes(str_data: str) -> bytes:
    # 前後の"とbを削除してencodeする。
    return str_data.encode()[2:-1]
