import re
import json
from ..exception.FuncException import FuncException
from urllib import parse, request


class Address:
    def __init__(self, post_num) -> None:
        self.post_num = post_num
        self.address: dict = None

    @property
    def post_num(self):
        return self._post_num

    @post_num.setter
    def post_num(self, value):
        if not re.match("[0-9]{7}", value):
            raise FuncException("郵便番号の入力が不正です")
        self._post_num = value

    def set_address(self):
        """
        郵便番号からURLを取得
        """
        # URLを設定
        BASE_URL = "https://zipcloud.ibsnet.co.jp/api/"
        REQ_PARM_FMT = "search?zipcode={}"
        param = REQ_PARM_FMT.format(self.post_num)
        target_url = parse.urljoin(BASE_URL, param)

        # getRequest
        req = request.Request(target_url)
        with request.urlopen(req) as res:
            body = json.load(res)

        # responseチェック
        if body["status"] != 200 or body["results"] == None:
            raise FuncException("郵便番号から住所を取得できませんでした")

        self.address = body["results"][0]

    def show_address(self):
        key_list = list(self.address.keys())
        address_key_list: list = []
        for i in range(3):
            address_key_list.append(key_list[i])
        print("-----住所-----")
        [print(self.address[k], end=" ") for k in address_key_list]
        print("\n---------------")


def execute():
    post_num = input('7桁の郵便番号を入力してください(" - "不要)')
    address: Address = Address(post_num)
    address.set_address()
    address.show_address()

    return None
