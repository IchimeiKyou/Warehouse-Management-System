"""
在庫検索統計画面（白色カード + 濃紺スタイル）
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql
import home


def Statistics(account):
    # ==========================
    # データベース接続
    # ==========================
    connect = pymysql.Connect(
        host='localhost', port=3306, user='root', passwd='123456',
        database='warehouse', charset='utf8'
    )
    cursor = connect.cursor()

    def doSQL(sql):
        cursor.execute(sql)
        connect.commit()

    # ==========================
    # メインウィンドウ
    # ==========================
    App = tk.Tk()
    App.title('在庫検索統計 - Warehousing')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    title_jp = tk.Label(App, text='在 庫 検 索 統 計',
                        bg='#1E3D59', fg='white', font=('メイリオ', 36, 'bold'))
    title_jp.place(relx=0.5, y=90, anchor='center')

    title_en = tk.Label(App, text='Search and Statistics',
                        bg='#1E3D59', fg='white', font=('メイリオ', 18))
    title_en.place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白色カード
    # ==========================
    card = tk.Frame(App, bg='white', width=800, height=220, relief='ridge', bd=2)
    card.place(relx=0.5, y=200, anchor='n')

    # ==========================
    # 日付入力
    # ==========================
    varDate_year = tk.StringVar()
    varDate_month = tk.StringVar()
    varDate_day = tk.StringVar()

    tk.Label(card, text='検索日:', bg='white', font=('メイリオ', 14)).place(x=20, y=30)
    tk.Entry(card, textvariable=varDate_year, font=('メイリオ', 12), justify='center').place(x=110, y=28, width=80)
    tk.Label(card, text='年', bg='white', font=('メイリオ', 12)).place(x=200, y=30)
    tk.Entry(card, textvariable=varDate_month, font=('メイリオ', 12), justify='center').place(x=230, y=28, width=50)
    tk.Label(card, text='月', bg='white', font=('メイリオ', 12)).place(x=290, y=30)
    tk.Entry(card, textvariable=varDate_day, font=('メイリオ', 12), justify='center').place(x=320, y=28, width=50)
    tk.Label(card, text='日', bg='white', font=('メイリオ', 12)).place(x=380, y=30)

    # ==========================
    # 統計方法選択
    # ==========================
    method = '先入先出'
    varMethod = tk.IntVar(value=1 if method == '先入先出' else 2 if method == '後入先出' else 3)

    tk.Radiobutton(card, text='先入先出(FIFO)', variable=varMethod, value=1, bg='white', font=('メイリオ', 12)).place(x=20, y=90)
    tk.Radiobutton(card, text='後入先出(LIFO)', variable=varMethod, value=2, bg='white', font=('メイリオ', 12)).place(x=200, y=90)
    tk.Radiobutton(card, text='加重平均(加重平均単価)', variable=varMethod, value=3, bg='white', font=('メイリオ', 12)).place(x=380, y=90)

    # ==========================
    # 検索関数
    # ==========================
    def Search():
        doSQL("SELECT NAME FROM commodity;")
        names = [i[0] for i in cursor.fetchall()]
        doSQL("SELECT NAME FROM material;")
        names.extend([i[0] for i in cursor.fetchall()])

        result = []
        date = f"{varDate_year.get()}-{varDate_month.get()}-{varDate_day.get()} 23:59:59"

        for i in names:
            doSQL(f"SELECT * FROM inhouse WHERE date <= '{date}' AND NAME = '{i}';")
            imports = [list(r) for r in cursor.fetchall()]
            doSQL(f"SELECT * FROM outhouse WHERE date <= '{date}' AND NAME = '{i}';")
            exports = [list(r) for r in cursor.fetchall()]

            k = 0
            for j in range(len(exports)):
                if k >= len(imports):
                    break
                if exports[j][6] < imports[k][6]:
                    imports[k][6] -= exports[j][6]
                else:
                    while k < len(imports) and imports[k][6] < exports[j][6]:
                        exports[j][6] -= imports[k][6]
                        k += 1
                    if k < len(imports):
                        imports[k][6] -= exports[j][6]

            totalAmount = sum([imp[6] for imp in imports[k:]])
            totalValue = sum([imp[5] * imp[6] for imp in imports[k:]])
            if varMethod.get() == 1:
                unit_price = imports[k][5] if totalAmount > 0 else 0
            elif varMethod.get() == 2:
                unit_price = imports[-1][5] if totalAmount > 0 else 0
            else:
                unit_price = round(totalValue / totalAmount, 2) if totalAmount > 0 else 0

            result.append((i, totalAmount, unit_price, totalValue))

        # ==========================
        # 表表示
        # ==========================
        table_frame = tk.Frame(App, bg='white')
        table_frame.place(relx=0.5, y=450, anchor='n', width=860, height=120)

        table = ttk.Treeview(table_frame, show='headings', columns=['品名', '在庫数量', '単価', '在庫価値'])
        table.pack(fill='both', expand=True)
        for col in table['columns']:
            table.heading(col, text=col)
            table.column(col, anchor='center', width=200)

        for row in result:
            table.insert('', 'end', values=row)

    # ==========================
    # リセット関数
    # ==========================
    def Reset():
        varDate_year.set('')
        varDate_month.set('')
        varDate_day.set('')
        varMethod.set(1)

    # ==========================
    # 戻る・閉じる
    # ==========================
    def Back():
        App.destroy()
        home.Home(account)

    def Close():
        App.destroy()

    # ==========================
    # ボタン
    # ==========================
    style = ttk.Style()
    style.configure("Blue.TButton", font=('メイリオ', 12, 'bold'), foreground='white', background='#1E3D59')
    style.map("Blue.TButton", background=[('active', '#244E73')])
    style.configure("White.TButton", font=('メイリオ', 12, 'bold'), foreground='#1E3D59', background='white')
    style.map("White.TButton", background=[('active', '#E5E5E5')])

    btn_search = ttk.Button(card, text='検索', command=Search, style='White.TButton')
    btn_search.place(x=70, y=150, width=120, height=40)
    btn_reset = ttk.Button(card, text='リセット', command=Reset, style='White.TButton')
    btn_reset.place(x=250, y=150, width=120, height=40)
    btn_back = ttk.Button(card, text='戻る', command=Back, style='White.TButton')
    btn_back.place(x=430, y=150, width=120, height=40)
    btn_close = ttk.Button(card, text='終了', command=Close, style='White.TButton')
    btn_close.place(x=610, y=150, width=120, height=40)

    App.mainloop()


if __name__ == "__main__":
    Statistics('admin')
