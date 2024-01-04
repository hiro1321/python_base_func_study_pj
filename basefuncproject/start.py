# tkinterのインポート
from signal import raise_signal
import tkinter as tk
import tkinter.ttk as ttk
from importlib import import_module
from .libs.exception import FuncException

from basefuncproject.libs.utils.load_yml_service import load_yml


def show_choice_func() -> None:
    show_func_list()
    func_num = input("対象機能の数字入力してください>")
    execute_func(func_num)


def show_func_list():
    print("*****************機能一覧*****************")
    func_list: dict = load_yml("func_list")
    for num, func in func_list.items():
        func_name = func.get("func_name")
        print(f"{num} : {func_name}")
    print("****************************************")


def execute_func(num_str: str) -> bool:
    func_list: dict = load_yml("func_list")
    str_keys = list(map(lambda key: str(key), func_list.keys()))
    if num_str not in str_keys:
        raise Exception("存在しない機能番号が入力されました")
    target_func = func_list.get(int(num_str))
    target_description = target_func.get("description")
    print(f" ---\n[機能概要]\n{target_description}\n---")
    target_method = target_func.get("module_name")
    try:
        import_module(target_method).execute()
    except ModuleNotFoundError as e:
        raise Exception("対象機能のメソッドが定義されていません")
