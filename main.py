#######################################################################
#
# SimultaneousSwitcher
# Python3.11.2 メイン処理プログラム by easilyshorter
#
# OBSの切り替え
#
#######################################################################

#######################################################################
#
# ライブラリのインポート
#
#######################################################################
# Python標準ライブラリ
import tkinter as tk  # GUIツールキット
from tkinter import ttk, messagebox  # GUIツールキットの拡張ウィジェットとメッセージボックス
from PIL import Image, ImageTk  # 画像処理ライブラリとtkinter用の画像モジュール
import pandas as pd  # データ分析ライブラリ
import os  # ファイルを扱うモジュール
import sys  # システム固有のパラメータと関数
import json  # JSONファイルを扱うモジュール
import codecs  # iniファイルを扱うモジュール
import psutil  # システムとプロセス情報のライブラリ
import configparser  # 設定ファイルパーサ
import subprocess  # プロセス制御のサブモジュール

# 自作モジュール
import util  # ユーティリティ
import init  # 初期設定画面
import setting  # データ設定画面
import core  # 文字列情報の格納


#######################################################################
# 処理内容：コマンドライン引数に無効な文字がないかをチェックする
# 関数名　：check_startup_parameters
# 引数　　：None / なし
# 戻り値　：None / なし
#######################################################################
def check_startup_parameters():
    for param in sys.argv:
        for i in ["--collection", "--profile", "--scene"]:
            if i in param:
                messagebox.showerror(core.title_err, core.err_param)
                sys.exit()


#######################################################################
# 処理内容：本ソフトまたはOBSが起動中かをチェックする
# 関数名　：check_existing_processes
# 引数　　：current_pid / このプログラムのpid
# 戻り値　：None / なし
#######################################################################
def check_existing_processes(current_pid):
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if "obs" in process.info["name"].lower():
            messagebox.showerror(core.title_err, core.err_obs)
            sys.exit()
        elif (
            os.path.basename(__file__).lower() in process.info["name"].lower()
            and process.info["pid"] != current_pid
        ):
            messagebox.showerror(core.title_err, core.err_soft)
            sys.exit()


#######################################################################
# 処理内容：10秒毎にOBSが起動されていないかをチェックする
# 関数名　：check_obs_while_running
# 引数　　：None / なし
# 戻り値　：None / なし
#######################################################################
def check_obs_while_running():
    for process in psutil.process_iter(attrs=["name"]):
        if "obs" in process.info["name"].lower():
            messagebox.showerror(core.title_err, core.err_launch)
            sys.exit()
    root.after(10000, check_obs_while_running)


#######################################################################
# 処理内容：設定ファイルなどを生成する
# 関数名　：create_initial_files
# 引数　　：root / Tkオブジェクト
# 戻り値　：None / なし
#######################################################################
def create_initial_files(root):
    if not os.path.exists(core.path_dir):
        os.mkdir(core.path_dir)
        subprocess.run(["attrib", "+H", core.path_dir])
    if not os.path.exists(core.path_csv):
        with open(core.path_csv, "w") as file:
            file.write(core.init_csv)
    if not os.path.exists(core.path_ini):
        init.input_obs_settings(root)


#######################################################################
# 処理内容：テキストが長ければフォントサイズを小さくする
# 関数名　：adjust_font_size
# 引数　　：label / Tkのラベルウィジェット
# 　　　　：max_width / ラベルの最大幅
# 　　　　：font_size / 現時点でのフォントサイズ
# 戻り値　：None / なし
#######################################################################
def adjust_font_size(label, max_width, font_size=12):
    label.config(font=("TkDefaultFont", font_size))
    while label.winfo_reqwidth() > max_width and font_size > 1:
        font_size -= 1
        label.config(font=("TkDefaultFont", font_size))


#######################################################################
# 処理内容：パラメータを付与してOBSを起動する
# 関数名　：start_obs_with_parameters
# 引数　　：profile / 指定したプロファイル
# 　　　　：collection / 指定したシーンコレクション
# 　　　　：scene / 指定した初期表示のシーン
# 戻り値　：None / なし
#######################################################################
def start_obs_with_parameters(profile, collection, scene):
    args = [os.path.abspath(util.get_setting("obs_exe_path"))]
    args.extend(sys.argv[1:])
    if not pd.isnull(profile):
        args.extend(["--profile", profile])
    if not pd.isnull(collection):
        args.extend(["--collection", collection])
    if not pd.isnull(scene):
        args.extend(["--scene", scene])
    try:
        subprocess.Popen(args, cwd=util.get_setting("obs_dir_path"))
    except OSError as e:
        if e.winerror == 740:
            messagebox.showerror(core.title_err, core.err_adm)
        else:
            messagebox.showerror(core.title_err, core.err_ose + str(e.winerror))
    root.quit()
    sys.exit()


#######################################################################
# 処理内容：すべてのオブジェクトの名に(None)が入っていないかをチェックする
# 関数名　：none_settings
# 引数　　：None / なし
# 戻り値　：None / なし
#######################################################################
def none_settings():
    all_names = []
    # プロファイル
    profile_path = util.get_setting("profile_path")
    for subdir in os.listdir(profile_path):
        full_subdir = os.path.join(profile_path, subdir)
        if os.path.isdir(full_subdir):
            configa = configparser.ConfigParser()
            with codecs.open(
                os.path.join(full_subdir, "basic.ini"), "r", encoding="utf-8-sig"
            ) as f:
                configa.read_file(f)
            profile_name = configa.get("General", "Name")
            all_names.append(profile_name)
    # シーンコレクションとすべてのシーン
    collect_path = util.get_setting("collect_path")
    for file in os.listdir(collect_path):
        if file.endswith(".json"):
            with open(os.path.join(collect_path, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_names.append(data["name"])
                for scene in data["scene_order"]:
                    all_names.append(scene["name"])
    # (None)と同名のものがないかをチェック
    if not util.get_setting("none_setting") in all_names:
        return
    for name in core.none:
        if name not in all_names:
            util.update_config("none_setting", name)
            return
    messagebox.showerror(core.title_err, core.err_none + core.none[0])
    sys.exit()


#######################################################################
# 処理内容：メイン画面をリフレッシュする
# 関数名　：update_layout
# 引数　　：event /
# 戻り値　：None / なし
#######################################################################
def update_layout(event=None):
    # すべてのウィジェットを破棄する
    for widget in frame.winfo_children():
        widget.destroy()
    # キャンバスの縦スクロールを上部に固定し、データを読み込む
    canvas.yview_moveto(0)
    data_records = util.load_data()
    # データ数を計算し、キャンバスとフレームのサイズを設定する
    num_of_columns = int(dropdown.get().split()[0])
    total_data = len(data_records)
    rows_needed = (total_data + num_of_columns - 1) // num_of_columns
    total_buttons = rows_needed * num_of_columns
    adjusted_size = (380 - 20 * (num_of_columns + 1)) // num_of_columns
    frame.config(width=380, height=35 + (adjusted_size + 30) * rows_needed)
    for i in range(num_of_columns):
        for j in range(rows_needed):
            idx = i + j * num_of_columns
            x_position = 20 + i * (adjusted_size + 20)
            y_position_image = 35 + j * (adjusted_size + 30)
            y_position_text = y_position_image + adjusted_size + 5
            if idx >= total_data or (
                idx < total_data and not data_records[idx]["title"]
            ):
                label_img = tk.Label(
                    frame,
                    bg=("black" if theme == "dark" else "white"),
                    borderwidth=2,
                    relief="solid",
                )
                label_img.place(
                    x=x_position,
                    y=y_position_image,
                    width=adjusted_size,
                    height=adjusted_size,
                )
                label_text = tk.Label(
                    frame,
                    bg=("black" if theme == "dark" else "white"),
                    fg=("white" if theme == "dark" else "black"),
                    anchor="center",
                )
                label_text.place(x=x_position, y=y_position_text, width=adjusted_size)
                continue
            data = data_records[idx]
            try:
                if data["icon"] and isinstance(data["icon"], str):
                    img = Image.open(data["icon"])
                    max_size = max(img.width, img.height)
                    ratio = adjusted_size / max_size
                    resized_img = img.resize(
                        (int(img.width * ratio), int(img.height * ratio))
                    )
                else:
                    resized_img = Image.new(
                        "RGB", (adjusted_size, adjusted_size), "#0000FF"
                    )
            except IOError:
                resized_img = Image.new(
                    "RGB", (adjusted_size, adjusted_size), "#FF0000"
                )
            tk_image = ImageTk.PhotoImage(resized_img)
            image_photos.append(tk_image)
            label_img = tk.Label(
                frame,
                image=tk_image,
                bg=("black" if theme == "dark" else "white"),
                borderwidth=2,
                relief="solid",
                cursor="hand2",
            )
            label_img.place(
                x=x_position,
                y=y_position_image,
                width=adjusted_size,
                height=adjusted_size,
            )
            label_img.bind(
                "<Button-1>",
                lambda event, data=data: start_obs_with_parameters(
                    data["profile"], data["collection"], data["scene"]
                ),
            )
            label_text = tk.Label(
                frame,
                text=data["title"],
                bg=("black" if theme == "dark" else "white"),
                fg=("white" if theme == "dark" else "black"),
                anchor="center",
                cursor="hand2",
            )
            label_text.place(x=x_position, y=y_position_text, width=adjusted_size)
            label_text.bind(
                "<Button-1>",
                lambda event, data=data: start_obs_with_parameters(
                    data["profile"], data["collection"], data["scene"]
                ),
            )
            adjust_font_size(label_text, adjusted_size)
    # マウスホイールをバインドする
    if frame.winfo_height() <= canvas.winfo_height():
        canvas.unbind_all("<MouseWheel>")
    else:
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"),
        )
    util.update_config("rows", str(num_of_columns))


#######################################################################
#
# ここからプログラム本体
#
#######################################################################
if __name__ == "__main__":
    # ルートウィンドウを作成し非表示にする
    root = tk.Tk()
    root.withdraw()
    root.iconphoto(True, util.icon("logo"))
    root.title(core.title_main)
    root.geometry("410x600")
    root.resizable(0, 0)
    # 起動時の初期動作を行う
    check_startup_parameters()
    check_existing_processes(os.getpid())
    create_initial_files(root)
    if not os.path.exists(core.path_ini):
        sys.exit()
    none_settings()
    check_obs_while_running()
    theme = util.get_setting("theme")
    root.configure(bg="black" if theme == "dark" else "white")
    root.update_idletasks()
    root.geometry(
        "+%d+%d"
        % (
            root.winfo_screenwidth() - root.winfo_width() - 10,
            root.winfo_screenheight() - root.winfo_height() - 100,
        )
    )
    canvas = tk.Canvas(
        root, bg="black" if theme == "dark" else "white", highlightthickness=0
    )
    canvas.place(x=10, y=70, width=380, height=520)
    frame = tk.Frame(canvas, bg="black" if theme == "dark" else "white")
    canvas.create_window(0, 0, anchor="nw", window=frame)
    frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    scrollbar = tk.Scrollbar(
        root,
        orient="vertical",
        command=canvas.yview,
        bg=("grey" if theme == "dark" else "lightgrey"),
        activebackground=("white" if theme == "dark" else "grey"),
        troughcolor=("black" if theme == "dark" else "white"),
    )
    scrollbar.place(x=390, y=70, height=520)
    canvas.config(yscrollcommand=scrollbar.set)
    settings_button_img = util.imgload("setting").resize((30, 30))
    settings_photo = ImageTk.PhotoImage(settings_button_img)
    settings_button = tk.Button(
        root,
        image=settings_photo,
        bg="black" if theme == "dark" else "white",
        borderwidth=0,
        command=lambda: setting.show_settings(root, update_layout),
    )
    settings_button.place(x=10, y=10)
    """refresh_button_img = util.imgload("refresh").resize((30, 30))
    refresh_photo = ImageTk.PhotoImage(refresh_button_img)
    refresh_button = tk.Button(root, image=refresh_photo, bg='black' if theme == 'dark' else 'white', borderwidth=0, command=update_layout)
    refresh_button.place(x=50, y=10)"""
    dropdown = ttk.Combobox(
        root,
        values=["1 row", "2 rows", "3 rows", "4 rows", "5 rows"],
        state="readonly",
        width=8,
    )
    dropdown.bind("<<ComboboxSelected>>", update_layout)
    dropdown.place(x=320, y=10)
    dropdown.set(util.get_setting("rows") + " rows")
    root.option_add(
        "*TCombobox*Listbox.selectBackground", "black" if theme == "dark" else "white"
    )
    root.option_add(
        "*TCombobox*Listbox.selectForeground", "white" if theme == "dark" else "black"
    )
    version_label = tk.Label(
        root,
        text=core.version,
        bg="black" if theme == "dark" else "white",
        fg="white" if theme == "dark" else "black",
    )
    version_label.place(x=320, y=30)

    author_label = tk.Label(
        root,
        text=("by " + core.author),
        cursor="hand2",
        fg="white" if theme == "dark" else "black",
        bg="black" if theme == "dark" else "white",
    )
    author_label.place(x=310, y=45)
    author_label.bind("<Button-1>", util.open_website)
    image_photos = []
    root.deiconify()
    update_layout()
    root.mainloop()
