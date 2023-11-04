#######################################################################
#
# ファイル名：util.py
# 処理機能　：SimultaneousSwitcherのユーティリティ
#
#######################################################################

#######################################################################
#
# ライブラリのインポート
#
#######################################################################
# Python標準ライブラリ
import base64  # 画像ファイルをBase64で暗号化する
import pandas as pd  # csvを扱うモジュール
import tkinter as tk  # GUIツールキット
from PIL import Image  # tkinter用の画像モジュール
from io import BytesIO  # 画像を表示するモジュール
import image  # 画像を扱うモジュール
import configparser  # iniファイルを扱うモジュール
import webbrowser  # Webページに遷移させる

# 自作モジュール
import core  # 文字列情報の格納


#######################################################################
# 処理内容：画像をBase64で暗号化する
# 関数名　：i2t
# 引数　　：image / 暗号化したい画像のファイル名
# 　　　　：txt / Base64のデータを格納するファイル名
# 戻り値　：None / なし
#######################################################################
def i2t(image, txt):
    with open(image, "rb") as image_file:
        base64_data = base64.b64encode(image_file.read()).decode("utf-8")
    with open(txt, "w") as text_file:
        text_file.write(base64_data)


#######################################################################
# 処理内容：Base64で暗号化された画像を表示する
# 関数名　：imgload
# 引数　　：input / 表示したい画像
# 戻り値　：None / なし
#######################################################################
def imgload(input: str):
    match input:
        case "logo":
            return Image.open(BytesIO(base64.b64decode(image.logo)))
        case "setting":
            return Image.open(BytesIO(base64.b64decode(image.setting)))
        case "save":
            return Image.open(BytesIO(base64.b64decode(image.save)))
        case "return":
            return Image.open(BytesIO(base64.b64decode(image.back)))
        case "refresh":
            return Image.open(BytesIO(base64.b64decode(image.refresh)))
        case _:
            pass


#######################################################################
# 処理内容：Base64で暗号化された画像をアイコン化する
# 関数名　：icon
# 引数　　：input / 表示したいアイコン画像
# 戻り値　：None / なし
#######################################################################
def icon(input):
    match input:
        case "logo":
            return tk.PhotoImage(data=image.logo)
        case "setting":
            return tk.PhotoImage(data=image.setting)
        case _:
            pass


#######################################################################
# 処理内容：data.csvからデータを読み込む
# 関数名　：load_data
# 引数　　：
# 戻り値　：dict / csvの読み込みデータ
#######################################################################
def load_data(tree=None):
    data = pd.read_csv("ss_data/data.csv", encoding="shift_jis")
    if tree is None:
        data["title"] = data["title"].apply(
            lambda x: x
            if isinstance(x, str) and len(x) < 20
            else ("（ｒｙ" if isinstance(x, str) else "")
        )
        return data.to_dict("records")
    else:
        data = data.where(pd.notna(data), get_setting("none_setting"))
        for _, row in data.iterrows():
            values = (
                row["title"],
                row["icon"],
                row["profile"],
                row["collection"],
                row["scene"],
            )
            tree.insert("", "end", values=values)


#######################################################################
# 処理内容：init.iniに記述されたデータを取り出す
# 関数名　：get_setting
# 引数　　：key / 取り出したいデータ
# 戻り値　：None / なし
#######################################################################
def get_setting(key):
    config = configparser.ConfigParser()
    config.read(core.path_ini)
    return config.get("settings", key)


#######################################################################
# 処理内容：init.iniのデータを書き換える
# 関数名　：update_config
# 引数　　：key / 書き換えたい情報
# 　　　　：value / 書き換え後の値
# 戻り値　：None / なし
#######################################################################
def update_config(key, value):
    config = configparser.ConfigParser()
    config.read(core.path_ini)
    config.set("settings", key, value)
    with open(core.path_ini, "w") as configfile:
        config.write(configfile)

#######################################################################
# 処理内容：著作者のWebページを表示する
# 関数名　：open_website
# 引数　　：event / イベント
# 戻り値　：None / なし
#######################################################################
def open_website(event=None):
    webbrowser.open(core.url)
