from ast import main
import sys
from . import start
from .libs.exception.FuncException import FuncException
import traceback


def main():
    start.show_choice_func()


if __name__ == "__main__":
    try:
        main()
    except FuncException as e:
        print(str(e))
    except Exception as e:
        print("想定外のエラーが発生しました")
        print("エラーメッセージ ： " + str(e))
        print(traceback.format_tb(e.__traceback__))
