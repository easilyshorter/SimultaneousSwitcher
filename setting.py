#######################################################################
#
# ファイル名：setting.py
# 処理機能　：csvデータ編集画面に関するプログラム
#
#######################################################################

#######################################################################
#
# ライブラリのインポート
#
#######################################################################
# Python標準ライブラリ
import tkinter as tk  # GUIツールキット
from tkinter import ttk, filedialog, messagebox  # GUIツールキットの拡張ウィジェットとメッセージボックス
from PIL import ImageTk  # tkinter用の画像モジュール
import os  # ファイルを扱うモジュール
import json  # JSONファイルを扱うモジュール
import codecs  # iniファイルを扱うモジュール
import csv  # csvファイルを扱うモジュール
import configparser  # 設定ファイルパーサ

# 自作モジュール
import util  # ユーティリティ
import init  # 初期設定画面
import core  # 文字列情報の格納


#######################################################################
# 処理内容：csv設定画面を表示する
# 関数名　：show_settings
# 引数　　：root / Tkオブジェクト
# 　　　　：update_func / メイン画面の更新関数
# 戻り値　：None / なし
#######################################################################
def show_settings(root, update_func):
    changes_made = False

    ###################################################################
    # 処理内容：保存ボタンを押されたらcsvを保存する
    # 関数名　：save_settings
    # 引数　　：None / なし
    # 戻り値　：None / なし
    ###################################################################
    def save_settings():
        nonlocal changes_made
        if util.get_setting("theme") != (
            "dark" if theme_var.get() == "ダーク" else "light"
        ):
            util.update_config(
                "theme", ("dark" if theme_var.get() == "ダーク" else "light")
            )
        with open(core.path_csv, "w", newline="", encoding="shift-jis") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "icon", "profile", "collection", "scene"])
            for item in tree.get_children():
                values = tree.item(item)["values"]
                values = [
                    "" if v == util.get_setting("none_setting") else v for v in values
                ]
                writer.writerow(values)
        changes_made = False
        settings_window.bell()
        update_func()

    ###################################################################
    # 処理内容：閉じるボタンを押されたら閉じる
    # 関数名　：close_settings
    # 引数　　：None / なし
    # 戻り値　：None / なし
    ###################################################################
    def close_settings():
        if changes_made or util.get_setting("theme") != (
            "dark" if theme_var.get() == "ダーク" else "light"
        ):
            settings_window.withdraw()
            settings_window.bell()
            if not messagebox.askyesno(core.title_chk, core.chk_save):
                settings_window.deiconify()
                return
        settings_window.destroy()
        root.deiconify()
        root.iconphoto(True, util.icon("logo"))

    ###################################################################
    # 処理内容：行を前後する
    # 関数名　：move_row
    # 引数　　：tree / csv画面
    # 　　　　：direction / 入れ替える方向
    # 戻り値　：None / なし
    ###################################################################
    def move_row(tree, direction):
        nonlocal changes_made
        selected = tree.selection()
        if not selected:
            return
        for s in selected:
            idx = tree.index(s)
            tree.move(s, "", idx + direction)
        changes_made = True

    ###################################################################
    # 処理内容：末尾に行を追加する
    # 関数名　：add_new_switch
    # 引数　　：tree / csv画面
    # 戻り値　：None / なし
    ###################################################################
    def add_new_switch(tree):
        nonlocal changes_made
        none = util.get_setting("none_setting")
        tree.insert("", "end", values=(core.new_switch, none, none, none, none))
        changes_made = True
        tree.yview_moveto(1)

    ###################################################################
    # 処理内容：選択した行を削除する
    # 関数名　：delete_row
    # 引数　　：tree / csv画面
    # 戻り値　：None / なし
    ###################################################################
    def delete_row(tree):
        nonlocal changes_made
        selected = tree.selection()
        if not selected:
            return
        else:
            for s in selected:
                tree.delete(s)
            changes_made = True

    ###################################################################
    # 処理内容：選択した行を編集する
    # 関数名　：edit_selected_row
    # 引数　　：tree / csv画面
    # 　　　　：columns / 列のタイプ
    # 戻り値　：None / なし
    ###################################################################
    def edit_selected_row(tree, columns):
        ###############################################################
        # 処理内容：値の変更を画面に表示する
        # 関数名　：save_edits
        # 引数　　：None / なし
        # 戻り値　：None / なし
        ###############################################################
        def save_edits():
            nonlocal changes_made
            current_values = list(tree.item(selected_items[0])["values"])
            for idx, column_name in enumerate(
                ["title", "icon", "profile", "collection", "scene"]
            ):
                if column_name in entries:
                    current_values[idx] = entries[column_name].get()
            if current_values[3] == util.get_setting("none_setting"):
                current_values[4] = util.get_setting("none_setting")
            tree.item(selected_items[0], values=tuple(current_values))
            changes_made = True
            edit_window.destroy()

        ###############################################################
        # 処理内容：閉じるボタンや取消を押された時の動作
        # 関数名　：cancel_edits
        # 引数　　：None / なし
        # 戻り値　：None / なし
        ###############################################################
        def cancel_edits():
            edit_window.destroy()

        ###############################################################
        # 処理内容：文字列に2バイト文字が含まれているかをチェックする
        # 関数名　：contains_double_byte_characters
        # 引数　　：str / チェック対象の文字列
        # 戻り値　：bool / 2バイト文字が含まれていればTrue、それ以外はFalse
        ###############################################################
        def contains_double_byte_characters(str):
            return any(ord(ch) > 127 for ch in str)

        ###############################################################
        # 処理内容：
        # 関数名　：
        # 引数　　：
        # 戻り値　：
        ###############################################################
        def get_profiles_from_directory(directory_path):
            profiles = [util.get_setting("none_setting")]
            for subdir in os.listdir(directory_path):
                full_subdir = os.path.join(directory_path, subdir)
                if os.path.isdir(full_subdir):
                    config = configparser.ConfigParser()
                    with codecs.open(
                        os.path.join(full_subdir, "basic.ini"),
                        "r",
                        encoding="utf-8-sig",
                    ) as f:
                        config.read_file(f)
                    profile_name = config.get("General", "Name")
                    if not contains_double_byte_characters(profile_name):
                        profiles.append(profile_name)
            return profiles

        ###############################################################
        # 処理内容：
        # 関数名　：
        # 引数　　：
        # 戻り値　：
        ###############################################################
        def get_scene_collections_from_directory(scene_collection_path):
            collections = [util.get_setting("none_setting")]
            for file in os.listdir(scene_collection_path):
                if file.endswith(".json"):
                    with open(
                        os.path.join(scene_collection_path, file), "r", encoding="utf-8"
                    ) as f:
                        data = json.load(f)
                        if not contains_double_byte_characters(data["name"]):
                            collections.append(data["name"])
            return collections

        ###############################################################
        # 処理内容：
        # 関数名　：
        # 引数　　：
        # 戻り値　：
        ###############################################################
        def get_scenes_from_collection(collection_name, scene_collection_path):
            scenes = [util.get_setting("none_setting")]
            for file in os.listdir(scene_collection_path):
                if file.endswith(".json"):
                    with open(
                        os.path.join(scene_collection_path, file), "r", encoding="utf-8"
                    ) as f:
                        data = json.load(f)
                        if data["name"] == collection_name:
                            for scene in data["scene_order"]:
                                if not contains_double_byte_characters(scene["name"]):
                                    scenes.append(scene["name"])
                            break
            return scenes

        ###############################################################
        #
        # ここから関数本体
        #
        ###############################################################
        selected_items = tree.selection()
        if not selected_items:
            return
        else:
            item = tree.item(selected_items[0])["values"]
            if columns == "c" and item[3] == util.get_setting("none_setting"):
                settings_window.bell()
                return
        if util.get_setting("theme") == "dark":
            edit_window = tk.Toplevel(settings_window, bg="black")
        else:
            edit_window = tk.Toplevel(settings_window)
        edit_window.title(core.title_edit)
        edit_window.transient(settings_window)
        edit_window.grab_set()
        edit_window.geometry("360x140")
        entries = {}
        if columns == "a":
            if util.get_setting("theme") == "dark":
                tk.Label(edit_window, text="名前", bg="black", fg="white").place(
                    x=10, y=10
                )
            else:
                tk.Label(edit_window, text="名前").place(x=10, y=10)
            entries["title"] = tk.Entry(edit_window, width=35)
            entries["title"].place(x=120, y=10)
            entries["title"].insert(0, item[0])
            if util.get_setting("theme") == "dark":
                tk.Label(edit_window, text="アイコン", bg="black", fg="white").place(
                    x=10, y=50
                )
            else:
                tk.Label(edit_window, text="アイコン").place(x=10, y=50)
            entries["icon"] = tk.Entry(edit_window, width=35)
            entries["icon"].place(x=120, y=50)
            entries["icon"].insert(0, item[1])
            tk.Button(
                edit_window,
                text="...",
                command=lambda: entries["icon"].delete(0, tk.END)
                or entries["icon"].insert(tk.END, filedialog.askopenfilename()),
            ).place(x=320, y=50)
        elif columns == "b":
            if util.get_setting("theme") == "dark":
                tk.Label(edit_window, text="プロファイル", bg="black", fg="white").place(
                    x=10, y=10
                )
            else:
                tk.Label(edit_window, text="プロファイル").place(x=10, y=10)
            entries["profile"] = ttk.Combobox(
                edit_window,
                values=get_profiles_from_directory(util.get_setting("profile_path")),
                width=34,
                state="readonly",
            )
            entries["profile"].place(x=120, y=10)
            entries["profile"].set(
                item[2] if item[2] else util.get_setting("none_setting")
            )
            if util.get_setting("theme") == "dark":
                tk.Label(edit_window, text="シーンコレクション", bg="black", fg="white").place(
                    x=10, y=50
                )
            else:
                tk.Label(edit_window, text="シーンコレクション").place(x=10, y=50)
            entries["collection"] = ttk.Combobox(
                edit_window,
                values=get_scene_collections_from_directory(
                    util.get_setting("collect_path")
                ),
                width=34,
                state="readonly",
            )
            entries["collection"].place(x=120, y=50)
            entries["collection"].set(
                item[3] if item[3] else util.get_setting("none_setting")
            )
        elif columns == "c":
            if util.get_setting("theme") == "dark":
                tk.Label(edit_window, text="初期シーン", bg="black", fg="white").place(
                    x=10, y=10
                )
            else:
                tk.Label(edit_window, text="初期シーン").place(x=10, y=10)
            entries["scene"] = ttk.Combobox(edit_window, width=34, state="readonly")
            entries["scene"].place(x=120, y=10)
            scene_options = get_scenes_from_collection(
                item[3], util.get_setting("collect_path")
            )
            entries["scene"]["values"] = scene_options
            entries["scene"].set(item[4])
        tk.Button(edit_window, text="保存", width=10, command=save_edits).place(
            x=80, y=90
        )
        tk.Button(edit_window, text="取消", width=10, command=cancel_edits).place(
            x=200, y=90
        )
        edit_window.mainloop()

    def show_init():
        settings_window.withdraw()
        init.input_obs_settings(settings_window)
        settings_window.deiconify()

    ###################################################################
    #
    # ここからプログラム本体
    #
    ###################################################################
    # メインウィンドウを非表示にし、設定画面のウィンドウを作成する
    root.withdraw()
    settings_window = tk.Toplevel()
    settings_window.iconphoto(True, util.icon("setting"))
    settings_window.title("設定画面")
    settings_window.geometry("410x600")
    settings_window.resizable(0, 0)
    settings_window.geometry(
        "+%d+%d"
        % (
            root.winfo_screenwidth() - root.winfo_width() - 10,
            root.winfo_screenheight() - root.winfo_height() - 100,
        )
    )
    theme = util.get_setting("theme")
    # テーマのドロップダウン
    if theme == "dark":
        settings_window.configure(bg="black")
        theme_label = tk.Label(
            settings_window, text="テーマ：", bg="black", fg="white", font=("Arial", 20)
        )
    else:
        theme_label = tk.Label(
            settings_window, text="テーマ：", fg="black", font=("Arial", 20)
        )
    theme_label.place(x=10, y=4)  # yの値を5に設定
    theme_var = tk.StringVar()
    theme_var.set("ダーク" if theme == "dark" else "ライト")
    theme_dropdown = ttk.Combobox(
        settings_window,
        textvariable=theme_var,
        values=["ライト", "ダーク"],
        state="readonly",
        width=10,
    )  # 幅を10に設定
    theme_dropdown.place(x=125, y=16)  # xの値を90に設定, yの値を7に設定
    # 各種ボタンの定義
    initial_img = util.imgload("setting").resize((30, 30))  # initial
    initial_photo = ImageTk.PhotoImage(initial_img)
    save_img = util.imgload("save").resize((30, 30))  # save
    save_photo = ImageTk.PhotoImage(save_img)
    back_img = util.imgload("return").resize((30, 30))  # data
    back_photo = ImageTk.PhotoImage(back_img)
    if theme == "dark":
        initial_button = tk.Button(
            settings_window,
            image=initial_photo,
            command=show_init,
            bg="black",
            fg="white",
            borderwidth=0,
        )
        save_button = tk.Button(
            settings_window,
            image=save_photo,
            command=save_settings,
            bg="black",
            fg="white",
            borderwidth=0,
        )
        back_button = tk.Button(
            settings_window,
            image=back_photo,
            command=close_settings,
            bg="black",
            fg="white",
            borderwidth=0,
        )
    else:
        initial_button = tk.Button(
            settings_window, image=initial_photo, command=show_init, borderwidth=0
        )
        save_button = tk.Button(
            settings_window, image=save_photo, command=save_settings, borderwidth=0
        )
        back_button = tk.Button(
            settings_window, image=back_photo, command=close_settings, borderwidth=0
        )
    initial_button.place(x=290, y=10)
    save_button.place(x=330, y=10)
    back_button.place(x=370, y=10)
    # csv編集エリア
    tree = ttk.Treeview(
        settings_window,
        columns=("title", "icon", "profile", "collection", "scene"),
        show="headings",
        height=6,
    )
    tree.heading("title", text="名前")
    tree.heading("icon", text="アイコン")
    tree.heading("profile", text="プロファイル")
    tree.heading("collection", text="シーンコレクション")
    tree.heading("scene", text="初期シーン")
    tree.column("title", width=60)
    tree.column("icon", width=60)
    tree.column("profile", width=60)
    tree.column("collection", width=60)
    tree.column("scene", width=60)
    tree.place(x=5, y=50, width=385, height=450)
    scrollbar = tk.Scrollbar(settings_window, orient="vertical", command=tree.yview)
    scrollbar.place(x=390, y=50, height=450)
    tree.configure(yscrollcommand=scrollbar.set)
    up_btn = tk.Button(settings_window, text="↑", command=lambda: move_row(tree, -1))
    up_btn.place(x=12, y=510)
    down_btn = tk.Button(settings_window, text="↓", command=lambda: move_row(tree, 1))
    down_btn.place(x=42, y=510)
    display_settings_btn = tk.Button(
        settings_window, text="表示設定", command=lambda: edit_selected_row(tree, "a")
    )
    display_settings_btn.place(x=72, y=510)
    switch_settings_btn = tk.Button(
        settings_window, text="切替設定", command=lambda: edit_selected_row(tree, "b")
    )
    switch_settings_btn.place(x=137, y=510)
    scene_btn = tk.Button(
        settings_window, text="初期シーン", command=lambda: edit_selected_row(tree, "c")
    )
    scene_btn.place(x=202, y=510)
    add_new_btn = tk.Button(
        settings_window, text="新規追加", command=lambda: add_new_switch(tree)
    )
    add_new_btn.place(x=272, y=510)
    delete_btn = tk.Button(
        settings_window, text="一行削除", command=lambda: delete_row(tree)
    )
    delete_btn.place(x=337, y=510)
    util.load_data(tree)
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)
    settings_window.mainloop()
