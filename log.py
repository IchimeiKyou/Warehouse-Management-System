import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import home

def initialization():
    # ==========================
    # データベース接続
    # ==========================
    connect = pymysql.Connect(
        host='localhost', port=3306, user='root', passwd='123456',
        database='warehouse', charset='utf8'
    )
    cursor = connect.cursor()

    # ==========================
    # メインウィンドウ設定
    # ==========================
    root = tk.Tk()
    root.title('倉庫管理システムログイン')
    root.geometry('500x400')
    root.resizable(False, False)
    root.configure(bg='#1E3D59')  # 深蓝背景

    # ----------------- タイトル -----------------
    tk.Label(root, text='倉庫管理システムログイン', font=('メイリオ', 26, 'bold'), bg='#1E3D59', fg='white').pack(pady=30)
    tk.Label(root, text='Warehouse Management System Login', font=('メイリオ', 14), bg='#1E3D59', fg='white').pack(pady=0)

    # ----------------- 入力フォーム -----------------
    frame = tk.Frame(root, bg='#1E3D59')
    frame.pack(pady=10)

    tk.Label(frame, text='アカウント:', font=('メイリオ', 14), bg='#1E3D59', fg='white').grid(row=0, column=0, padx=10, pady=15, sticky='e')
    tk.Label(frame, text='パスワード:', font=('メイリオ', 14), bg='#1E3D59', fg='white').grid(row=1, column=0, padx=10, pady=15, sticky='e')

    varName = tk.StringVar()
    varPwd = tk.StringVar()
    entryName = tk.Entry(frame, textvariable=varName, font=('メイリオ', 14))
    entryName.grid(row=0, column=1, padx=10, pady=15, ipadx=10, ipady=5)
    entryPwd = tk.Entry(frame, textvariable=varPwd, font=('メイリオ', 14), show='*')
    entryPwd.grid(row=1, column=1, padx=10, pady=15, ipadx=10, ipady=5)

    # Enterでログイン
    entryPwd.bind('<Return>', lambda event: login())

    # ----------------- ボタン -----------------
    btn_frame = tk.Frame(root, bg='#1E3D59')
    btn_frame.pack(pady=20)

    style = ttk.Style()
    style.configure('White.TButton', font=('メイリオ', 14, 'bold'), foreground='#1E3D59', background='white')
    style.map('White.TButton', background=[('active', '#E5E5E5')])

    def login():
        cursor.execute("SELECT ACCOUNT FROM administrators;")
        accounts = [i[0] for i in cursor.fetchall()]
        if varName.get() not in accounts:
            messagebox.showerror('エラー', '該当アカウントが存在しません！')
            return
        cursor.execute("SELECT PASSWORD FROM administrators WHERE ACCOUNT = %s;", (varName.get(),))
        password = cursor.fetchone()[0]
        if varPwd.get() != password:
            messagebox.showerror('エラー', 'アカウントまたはパスワードが間違っています！')
            return
        root.destroy()
        home.Home(varName.get())

    login_btn = ttk.Button(btn_frame, text='ログイン', command=login, style='White.TButton')
    login_btn.grid(row=0, column=0, padx=20, ipadx=10, ipady=5)
    quit_btn = ttk.Button(btn_frame, text='終了', command=root.destroy, style='White.TButton')
    quit_btn.grid(row=0, column=1, padx=20, ipadx=10, ipady=5)

    root.mainloop()


if __name__ == "__main__":
    initialization()
