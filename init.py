#######################################################################
#
# ファイル名：init.py
# 処理機能　：初期設定画面に関するプログラム
#
#######################################################################

#######################################################################
#
# ライブラリのインポート
#
#######################################################################
# Python標準ライブラリ
import tkinter as tk  # GUIツールキット
from tkinter import filedialog  # ファイル選択
import os  # ファイルを扱うモジュール
import sys  # システム固有のパラメータと関数
import getpass  # ユーザー名を取得

# 自作モジュール
import util  # ユーティリティ
import core  # 文字列情報の格納


#######################################################################
# 処理内容：初期設定画面を表示する
# 関数名　：input_obs_settings
# 引数　　：root / Tkオブジェクト
# 戻り値　：None / なし
#######################################################################
def input_obs_settings(root):
    ###################################################################
    # 処理内容：設定値情報を保存する
    # 関数名　：save_settings
    # 引数　　：None / なし
    # 戻り値　：None / なし
    ###################################################################
    def save_settings():
        theme = util.get_setting("theme") if os.path.exists(core.path_ini) else "light"
        with open(core.path_ini, "w") as file:
            file.write("[settings]\n")
            file.write(f"obs_exe_path={obs_exe_entry.get()}\n")
            file.write(f"obs_dir_path={obs_dir_entry.get()}\n")
            file.write(f"profile_path={profile_entry.get()}\n")
            file.write(f"collect_path={collect_entry.get()}\n")
            file.write(f"none_setting={core.none[0]}\n")
            file.write(f"theme={theme}\n")
            file.write("rows=3\n")
        settings_window.destroy()

    ###################################################################
    # 処理内容：exeファイルを開いてパスを格納する
    # 関数名　：open_file_dialog
    # 引数　　：entry / ファイルパス
    # 戻り値　：None / なし
    ###################################################################
    def open_file_dialog(entry):
        file_path = filedialog.askopenfilename(
            filetypes=[("Executable files", "*.exe")]
        )
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    ###################################################################
    # 処理内容：ディレクトリを開いてパスを格納する
    # 関数名　：open_directory_dialog
    # 引数　　：entry / ディレクトリパス
    # 戻り値　：None / なし
    ###################################################################
    def open_directory_dialog(entry):
        dir_path = filedialog.askdirectory()
        if dir_path:
            entry.delete(0, tk.END)
            entry.insert(0, dir_path)

    ###################################################################
    # 処理内容：閉じるボタンを押されたら強制終了する
    # 関数名　：on_closing
    # 引数　　：None / なし
    # 戻り値　：None / なし
    ###################################################################
    def on_closing():
        settings_window.destroy()
        sys.exit()

    ###################################################################
    #
    # ここからプログラム本体
    #
    ###################################################################
    # ウィンドウを作成する
    settings_window = tk.Toplevel(root)
    settings_window.title(core.title_init)
    settings_window.geometry(
        "+%d+%d"
        % (
            int(
                (settings_window.winfo_screenwidth() / 2)
                - (settings_window.winfo_reqwidth() / 2)
            ),
            int(
                (settings_window.winfo_screenheight() / 2)
                - (settings_window.winfo_reqheight() / 2)
            ),
        )
    )

    # 各種ラベルとエントリーを作成(実行ファイル)
    obs_exe_label = tk.Label(settings_window, text=core.init_exe)
    obs_exe_label.grid(row=0, column=0, sticky="w")
    obs_exe_entry = tk.Entry(settings_window, width=50)
    obs_exe_entry.grid(row=0, column=1)
    obs_exe_entry.insert(0, "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe")
    obs_exe_button = tk.Button(
        settings_window, text="...", command=lambda: open_file_dialog(obs_exe_entry)
    )
    obs_exe_button.grid(row=0, column=2)

    # 各種ラベルとエントリーを作成(実行ディレクトリ)
    obs_dir_label = tk.Label(settings_window, text=core.init_dir)
    obs_dir_label.grid(row=1, column=0, sticky="w")
    obs_dir_entry = tk.Entry(settings_window, width=50)
    obs_dir_entry.grid(row=1, column=1)
    obs_dir_entry.insert(0, "C:\\Program Files\\obs-studio\\bin\\64bit")
    obs_dir_button = tk.Button(
        settings_window,
        text="...",
        command=lambda: open_directory_dialog(obs_dir_entry),
    )
    obs_dir_button.grid(row=1, column=2)

    # 各種ラベルとエントリーを作成(プロファイル)
    profile_label = tk.Label(settings_window, text=core.init_pro)
    profile_label.grid(row=2, column=0, sticky="w")
    profile_entry = tk.Entry(settings_window, width=50)
    profile_entry.grid(row=2, column=1)
    profile_entry.insert(
        0,
        f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\obs-studio\\basic\\profiles",
    )
    profile_button = tk.Button(
        settings_window,
        text="...",
        command=lambda: open_directory_dialog(profile_entry),
    )
    profile_button.grid(row=3, column=2)

    # 各種ラベルとエントリーを作成(シーンコレクション)
    collect_label = tk.Label(settings_window, text=core.init_col)
    collect_label.grid(row=3, column=0, sticky="w")
    collect_entry = tk.Entry(settings_window, width=50)
    collect_entry.grid(row=3, column=1)
    collect_entry.insert(
        0,
        f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\obs-studio\\basic\\scenes",
    )
    collect_button = tk.Button(
        settings_window,
        text="...",
        command=lambda: open_directory_dialog(collect_entry),
    )
    collect_button.grid(row=2, column=2)

    # 保存ボタンを作成
    save_button = tk.Button(settings_window, text=core.init_ini, command=save_settings)
    save_button.grid(row=4, column=0, columnspan=3)
    settings_window.protocol("WM_DELETE_WINDOW", on_closing)
    settings_window.grab_set()  # 他のウィンドウの操作を無効にする
    root.wait_window(settings_window)  # settings_windowが閉じるまで待つ
