"""
ユーザー追加 / 削除ガイドページ（ホーム画面と統一ダークブルー背景）
"""
import tkinter as tk
from tkinter import ttk
import home, create, delete


def CreateAndDelete(account):
    # ==========================
    # メインウィンドウ設定
    # ==========================
    App = tk.Tk()
    App.title('倉庫権限管理')
    App.geometry('900x600')
    App.config(bg='#1E3D59')  # ダークブルー背景
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    title_jp = tk.Label(App, text='システムユーザー管理',
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 42, 'bold'))
    title_jp.place(relx=0.5, y=80, anchor='center')

    title_en = tk.Label(App, text="System Users' Management",
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 18))
    title_en.place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白カード
    # ==========================
    card = tk.Frame(App, bg='white', width=700, height=300, relief='ridge', bd=2)
    card.place(relx=0.5, rely=0.55, anchor='center')

    # ==========================
    # スタイル設定（ブルー/ホワイト統一）
    # ==========================
    style = ttk.Style()
    style.configure("Blue.TButton",
                    font=('メイリオ', 15, 'bold'),
                    background='#1E3D59',
                    foreground='white',
                    borderwidth=0)
    style.map("Blue.TButton",
              background=[('active', '#244E73')])

    style.configure("White.TButton",
                    font=('メイリオ', 15, 'bold'),
                    background='white',
                    foreground='#1E3D59',
                    borderwidth=2)
    style.map("White.TButton",
              background=[('active', '#E5E5E5')])

    # ==========================
    # 機能ボタン
    # ==========================
    def jump_to_create():
        App.destroy()
        create.Create(account)

    def jump_to_delete():
        App.destroy()
        delete.Delete(account)

    btn_create = ttk.Button(card, text='ユーザー追加 / 更新',
                            style='White.TButton', command=jump_to_create)
    btn_create.place(x=100, y=60, width=230, height=80)

    btn_delete = ttk.Button(card, text='ユーザー削除',
                            style='White.TButton', command=jump_to_delete)
    btn_delete.place(x=370, y=60, width=230, height=80)

    # ==========================
    # 下部操作ボタン
    # ==========================
    def Close():
        App.destroy()

    def Back():
        App.destroy()
        home.Home(account)

    def Refresh():
        App.destroy()
        CreateAndDelete(account)

    btn_refresh = ttk.Button(card, text='更新', style='White.TButton', command=Refresh)
    btn_refresh.place(x=100, y=190, width=150, height=50)

    btn_back = ttk.Button(card, text='ホームに戻る', style='White.TButton', command=Back)
    btn_back.place(x=275, y=190, width=150, height=50)

    btn_quit = ttk.Button(card, text='終了', style='White.TButton', command=Close)
    btn_quit.place(x=450, y=190, width=150, height=50)

    App.mainloop()


if __name__ == "__main__":
    CreateAndDelete('admin')
