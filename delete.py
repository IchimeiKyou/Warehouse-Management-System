"""
ユーザー削除ページ（白カード + ダークブルースタイル）
"""
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from PIL import Image, ImageTk

import createAndDelete


def Delete(account):
    # ==========================
    # データベース接続
    # ==========================
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        database='warehouse',
        charset='utf8'
    )
    cursor = connect.cursor()

    def doSQL(sql):
        cursor.execute(sql)
        connect.commit()

    # ==========================
    # メインウィンドウ設定
    # ==========================
    App = tk.Tk()
    App.title('倉庫ユーザー削除')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    title_jp = tk.Label(App, text='システムユーザー削除',
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 42, 'bold'))
    title_jp.place(relx=0.5, y=80, anchor='center')

    title_en = tk.Label(App, text="Delete System User",
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 18))
    title_en.place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白カード
    # ==========================
    card = tk.Frame(App, bg='white', width=700, height=320, relief='ridge', bd=2)
    card.place(relx=0.5, rely=0.55, anchor='center')

    # ==========================
    # スタイル統一
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
    # 入力欄
    # ==========================
    varAccount = tk.StringVar()
    info_label = tk.Label(card, text='', bg='white', fg='#1E3D59',
                          font=('メイリオ', 13))

    lbl_acc = tk.Label(card, text='アカウント名：', bg='white',
                       fg='#1E3D59', font=('メイリオ', 15))
    lbl_acc.place(x=70, y=70)
    ent_acc = ttk.Entry(card, textvariable=varAccount, font=('メイリオ', 13))
    ent_acc.place(x=220, y=70, width=250, height=35)

    # ==========================
    # 機能関数
    # ==========================
    def search():
        user = varAccount.get().strip()
        if user == '':
            messagebox.showerror('警告', 'アカウント名を入力してください！')
            return
        sql = "SELECT ACCOUNT, AUTHORITY FROM administrators WHERE ACCOUNT='%s';" % user
        doSQL(sql)
        result = cursor.fetchall()
        if not result:
            messagebox.showerror('エラー', '該当アカウントは存在しません！')
            info_label.config(text='')
            return
        acc, auth = result[0]
        role = '管理者' if auth == 0 else '一般ユーザー'
        info_label.config(text=f"名前：{acc}     ユーザータイプ：{role}")
        info_label.place(x=100, y=130)

    def delete_user():
        user = varAccount.get().strip()
        if user == '':
            messagebox.showerror('警告', 'アカウント名を入力してください！')
            return
        doSQL("SELECT ACCOUNT FROM administrators WHERE ACCOUNT='%s';" % user)
        if cursor.fetchone() is None:
            messagebox.showerror('エラー', '該当アカウントは存在しません！')
            return
        confirm = messagebox.askyesno('削除確認', f'ユーザー "{user}" を削除してもよろしいですか？')
        if confirm:
            doSQL("DELETE FROM administrators WHERE ACCOUNT='%s';" % user)
            messagebox.showinfo('成功', f'ユーザー "{user}" が削除されました！')
            varAccount.set('')
            info_label.config(text='')

    def back():
        App.destroy()
        createAndDelete.CreateAndDelete(account)

    # ==========================
    # ボタン配置
    # ==========================
    btn_search = ttk.Button(card, text='検索', style='White.TButton', command=search)
    btn_search.place(x=500, y=70, width=120, height=35)

    btn_delete = ttk.Button(card, text='ユーザー削除', style='White.TButton', command=delete_user)
    btn_delete.place(x=160, y=220, width=160, height=55)

    btn_back = ttk.Button(card, text='戻る', style='White.TButton', command=back)
    btn_back.place(x=370, y=220, width=160, height=55)

    App.mainloop()


if __name__ == "__main__":
    Delete('admin')
