from tkinter import filedialog
import csv
import openpyxl
import os
import pprint
import datetime


class CsvFileInfo:
    def __init__(self, file_path):
        file_name = file_path.split("/")[-1]
        folder_path = file_path.replace(file_name, "")

        self.file_path = file_path
        self.file_name = file_name
        self.folder_path = folder_path


def execute():
    print("csv_func_service：start")

    # ダイアログでファイルを選択
    file_path = filedialog.askopenfilename(title="取込対象のcsvファイルを選択してください")

    # ファイルチェック・ファイル解析
    file_info = csv_file_parse(file_path)

    # csvをExcelに出力
    write_xl_from_csv(file_info)

    print("csv_func_service：END")


def csv_file_parse(file_path: str) -> CsvFileInfo:
    """
    (1)拡張子が ".csv" でないなら例外を投げる
    (2)ファイルが空なら例外を投げる
    (3)ファイル情報を返す
    """
    split_file_path = file_path.split(".")
    if split_file_path[-1] != "csv":
        raise Exception("対象ファイルの拡張子が.csvではありません")

    if os.stat(file_path).st_size == 0:
        raise Exception("対象ファイルが空です")

    return CsvFileInfo(file_path)


def write_xl_from_csv(fi: CsvFileInfo):
    """
    csvを読み込み,カンマ区切りでexcelに貼り付ける
    """
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]

    with open(fi.file_path, encoding="utf8", newline="") as f:
        # csvファイルを1行ずつ読み込む
        csvreader = csv.reader(f)

        # excelのworksheetに書き込み
        for i, row in enumerate(csvreader):
            for k, value in enumerate(row):
                ws.cell(i + 1, k + 1).value = value

    out_path = get_output_path(fi)
    wb.save(out_path)
    wb.close()


def get_output_path(fi: CsvFileInfo) -> str:
    """
    出力excelのパスを取得
    "/{csvと同じ階層}/YYYYMMDD_hhmmss_csv_parse.xlsx
    """
    csv_file_name: str = fi.file_name
    xl_file_name = csv_file_name.replace(".csv", ".xlsx")
    str_ymd = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    return "{0}/{1}_{2}".format(fi.folder_path, str_ymd, xl_file_name)
