import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import home

def PeriodSummary(account):
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
    App.title('業務データ集計 - Warehousing')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    tk.Label(App, text='業 務 デ ー タ 集 計', bg='#1E3D59', fg='white', font=('メイリオ', 36, 'bold')).place(relx=0.5, y=90, anchor='center')
    tk.Label(App, text='Business Data Summary', bg='#1E3D59', fg='white', font=('メイリオ', 18)).place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白色カード
    # ==========================
    card = tk.Frame(App, bg='white', width=820, height=140, relief='ridge', bd=2)
    card.place(relx=0.5, y=200, anchor='n')

    # ==========================
    # 日付入力
    # ==========================
    varDate_year_start = tk.StringVar()
    varDate_month_start = tk.StringVar()
    varDate_day_start = tk.StringVar()
    varDate_year_end = tk.StringVar()
    varDate_month_end = tk.StringVar()
    varDate_day_end = tk.StringVar()

    tk.Label(card, text='開始日:', bg='white', font=('メイリオ', 12)).place(x=20, y=20)
    tk.Entry(card, textvariable=varDate_year_start, width=10, justify='center').place(x=95, y=20)
    tk.Label(card, text='年', bg='white', font=('メイリオ', 12)).place(x=150, y=20)
    tk.Entry(card, textvariable=varDate_month_start, width=6, justify='center').place(x=175, y=20)
    tk.Label(card, text='月', bg='white', font=('メイリオ', 12)).place(x=213, y=20)
    tk.Entry(card, textvariable=varDate_day_start, width=6, justify='center').place(x=235, y=20)
    tk.Label(card, text='日', bg='white', font=('メイリオ', 12)).place(x=276, y=20)

    tk.Label(card, text='終了日:', bg='white', font=('メイリオ', 12)).place(x=320, y=20)
    tk.Entry(card, textvariable=varDate_year_end, width=10, justify='center').place(x=400, y=20)
    tk.Label(card, text='年', bg='white', font=('メイリオ', 12)).place(x=455, y=20)
    tk.Entry(card, textvariable=varDate_month_end, width=6, justify='center').place(x=480, y=20)
    tk.Label(card, text='月', bg='white', font=('メイリオ', 12)).place(x=518, y=20)
    tk.Entry(card, textvariable=varDate_day_end, width=6, justify='center').place(x=540, y=20)
    tk.Label(card, text='日', bg='white', font=('メイリオ', 12)).place(x=581, y=20)

    # ==========================
    # 核心検索
    # ==========================
    def Search():
        try:
            start_val = int(varDate_year_start.get())*10000 + int(varDate_month_start.get())*100 + int(varDate_day_start.get())
            end_val = int(varDate_year_end.get())*10000 + int(varDate_month_end.get())*100 + int(varDate_day_end.get())
        except ValueError:
            messagebox.showerror('エラー', '日付入力が不完全または不正です！')
            return
        if start_val >= end_val:
            messagebox.showerror('エラー', '終了日は開始日より後である必要があります！')
            return

        dateStart = f"{varDate_year_start.get()}-{varDate_month_start.get()}-{varDate_day_start.get()} 00:00:00"
        dateEnd = f"{varDate_year_end.get()}-{varDate_month_end.get()}-{varDate_day_end.get()} 23:59:59"

        table_frame = tk.Frame(App, bg='white')
        table_frame.place(relx=0.5, y=320, anchor='n', width=860, height=220)

        table = ttk.Treeview(table_frame, show='headings', columns=['項目', '数量'])
        table.pack(fill='both', expand=True)
        for col in table['columns']:
            table.heading(col, text=col)
            table.column(col, anchor='center', width=400)

        project = ['貨品仕入', '貨品借入', '貨品移入', '材料仕入', '材料借入', '材料移入',
                   '貨品返品(顧客)', '貨品販売', '貨品返品(供給元)', '貨品貸出', '貨品移出',
                   '材料返品(供給元)', '材料貸出', '材料移出']

        for i, proj in enumerate(project):
            if proj in ['貨品仕入', '貨品借入', '貨品移入', '材料仕入', '材料借入', '材料移入', '貨品返品(顧客)']:
                sql = f"SELECT QUANTITY FROM inhouse WHERE ATTRIBUTE='{proj}' AND DATE>='{dateStart}' AND DATE<='{dateEnd}'"
            else:
                sql = f"SELECT QUANTITY FROM outhouse WHERE ATTRIBUTE='{proj}' AND DATE>='{dateStart}' AND DATE<='{dateEnd}'"
            doSQL(sql)
            quantities = [k[0] for k in cursor.fetchall()]
            total = sum(quantities) if quantities else 0
            table.insert('', 'end', values=(proj, total))

    def Reset():
        varDate_year_start.set('')
        varDate_month_start.set('')
        varDate_day_start.set('')
        varDate_year_end.set('')
        varDate_month_end.set('')
        varDate_day_end.set('')

    def Back():
        App.destroy()
        home.Home(account)

    def Close():
        App.destroy()

    # ==========================
    # ボタン
    # ==========================
    btn_search = ttk.Button(card, text='検索', command=Search, style='White.TButton')
    btn_search.place(x=70, y=70, width=120, height=40)
    btn_reset = ttk.Button(card, text='リセット', command=Reset, style='White.TButton')
    btn_reset.place(x=250, y=70, width=120, height=40)
    btn_back = ttk.Button(card, text='戻る', command=Back, style='White.TButton')
    btn_back.place(x=430, y=70, width=120, height=40)
    btn_close = ttk.Button(card, text='終了', command=Close, style='White.TButton')
    btn_close.place(x=610, y=70, width=120, height=40)

    # ==========================
    # スタイル
    # ==========================
    style = ttk.Style()
    style.configure("Blue.TButton", font=('メイリオ', 12, 'bold'), foreground='white', background='#1E3D59')
    style.map("Blue.TButton", background=[('active', '#244E73')])
    style.configure("White.TButton", font=('メイリオ', 12, 'bold'), foreground='#1E3D59', background='white')
    style.map("White.TButton", background=[('active', '#E5E5E5')])

    App.mainloop()


if __name__ == "__main__":
    PeriodSummary('admin')
