#######################################################################
#
# ファイル名：core.py
# 処理機能　：文字列を変更したい時はこちらから
#
#######################################################################

# (None)が使われていた時、以下の文字列を試す
none = ["(None)", "---", "なし"]

# バージョン情報と著作者情報
version = "Version 1.00"
author = "easilyshorter"
url = "https://easilyshorter.com"

# 各ウィンドウのタイトル
title_main = "SimultaneousSwitcher"
title_init = "OBSの設定"
title_err = "エラー"
title_chk = "確認"
title_edit = "編集"

# 初期設定画面のラベル
init_exe = "OBS実行ファイル:"
init_dir = "OBS実行ディレクトリ:"
init_pro = "プロファイルディレクトリ:"
init_col = "シーンコレクションディレクトリ:"
init_ini = "設定を保存"

# エラーメッセージ
err_param = "起動パラメータに誤りがあります。"
err_obs = "OBSが既に起動しています。"
err_soft = "このソフトは既に起動しています。"
err_launch = "OBSが起動されました。"
err_none = "プロファイル・シーンコレクション・シーンすべてに\n以下の文字列が内容にしてください。\n"
err_adm = "OBSを実行するには、本プログラムも管理者権限で実行してください。"
err_ose = "OBSの起動に失敗しました。エラーコード："

# 動作確認メッセージ
chk_save = "変更内容を保存せずに閉じますか？"
chk_del = "選択された行を削除してもよろしいですか？"

# 設定ファイルのパス
path_dir = "./ss_data"
path_csv = "./ss_data/data.csv"
path_ini = "./ss_data/init.ini"

# csvと新規スイッチの文字列
init_csv = "title,icon,profile,collection,scene\nOBSの通常起動,,,,"
new_switch = "新規スイッチ"
# obs_exe_path, obs_dir_path, profile_path, collect_path, none_setting, theme, rows
