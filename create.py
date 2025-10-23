"""
ユーザー作成 / 更新ページ（白カード + ダークブルースタイル、削除ページと統一）
"""
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import createAndDelete


def Create(account):
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
    App.title('倉庫ユーザー作成')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    title_jp = tk.Label(App, text='ユーザー作成 / 更新',
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 42, 'bold'))
    title_jp.place(relx=0.5, y=80, anchor='center')

    title_en = tk.Label(App, text="Create / Update User",
                        bg='#1E3D59', fg='white',
                        font=('メイリオ', 18))
    title_en.place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白カード
    # ==========================
    card = tk.Frame(App, bg='white', width=700, height=350, relief='ridge', bd=2)
    card.place(relx=0.5, rely=0.6, anchor='center')

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
    # 入力欄
    # ==========================
    varAccount = tk.StringVar()
    varPassword = tk.StringVar()
    varAuthority = tk.IntVar(value=1)

    lbl_acc = tk.Label(card, text='アカウント名：', bg='white', fg='#1E3D59', font=('メイリオ', 15))
    lbl_acc.place(x=120, y=30)
    ent_acc = ttk.Entry(card, textvariable=varAccount, font=('メイリオ', 13))
    ent_acc.place(x=260, y=30, width=250, height=35)

    lbl_pwd = tk.Label(card, text='パスワード：', bg='white', fg='#1E3D59', font=('メイリオ', 15))
    lbl_pwd.place(x=120, y=90)
    ent_pwd = ttk.Entry(card, textvariable=varPassword, show='*', font=('メイリオ', 13))
    ent_pwd.place(x=260, y=90, width=250, height=35)

    # ==========================
    # 権限設定
    # ==========================
    auth_frame = tk.LabelFrame(card, text='権限設定', bg='white',
                               fg='#1E3D59', font=('メイリオ', 13, 'bold'),
                               relief='groove')
    auth_frame.place(x=140, y=150, width=380, height=70)

    tk.Radiobutton(auth_frame, text='一般ユーザー', variable=varAuthority, value=1,
                   bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=50, y=0)
    tk.Radiobutton(auth_frame, text='管理者', variable=varAuthority, value=0,
                   bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=200, y=0)

    # ==========================
    # 登録/更新処理
    # ==========================
    def commit():
        sql = "SELECT ID FROM administrators;"
        doSQL(sql)
        ids = [int(i[0]) for i in cursor.fetchall()]

        sql = "SELECT Account FROM administrators;"
        doSQL(sql)
        accounts = [i[0] for i in cursor.fetchall()]

        account_name = varAccount.get().strip()
        password = varPassword.get().strip()

        if account_name == '' or password == '':
            messagebox.showerror('警告', 'アカウント名とパスワードを入力してください！')
            return

        if account_name in accounts:
            # パスワードと権限を更新
            doSQL(f"UPDATE administrators SET PASSWORD='{password}', AUTHORITY='{varAuthority.get()}' WHERE ACCOUNT='{account_name}';")
        else:
            # 新規作成
            new_id = next(i for i in range(1, max(ids + [0]) + 2) if i not in ids)
            doSQL(f"INSERT INTO administrators VALUES ('{new_id}', '{account_name}', '{password}', '{varAuthority.get()}');")

        varAccount.set('')
        varPassword.set('')
        varAuthority.set(1)
        messagebox.showinfo('成功', f'アカウント "{account_name}" が作成 / 更新されました！')

    def back():
        App.destroy()
        createAndDelete.CreateAndDelete(account)

    # ==========================
    # ボタン配置（統一スタイル）
    # ==========================
    btn_commit = ttk.Button(card, text='作成 / 更新', style='White.TButton', command=commit)
    btn_commit.place(x=160, y=270, width=160, height=55)

    btn_back = ttk.Button(card, text='戻る', style='White.TButton', command=back)
    btn_back.place(x=370, y=270, width=160, height=55)

    App.mainloop()


if __name__ == "__main__":
    Create('admin')
