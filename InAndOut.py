import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import xlrd
import pymysql
import home, purchase, sellitems


def InAndOut(account):
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
    # メインウィンドウ設定
    # ==========================
    App = tk.Tk()
    App.title('入庫/出庫管理 - Warehousing')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    title_ch = tk.Label(App, text='日 常 在 庫 管 理',
                        bg='#1E3D59', fg='white', font=('メイリオ', 42, 'bold'))
    title_ch.place(relx=0.5, y=80, anchor='center')

    title_en = tk.Label(App, text='Daily Inventory Management',
                        bg='#1E3D59', fg='white', font=('メイリオ', 18))
    title_en.place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白色メインカード
    # ==========================
    card = tk.Frame(App, bg='white', width=700, height=350, relief='ridge', bd=2)
    card.place(relx=0.5, rely=0.65, anchor='center')

    # ==========================
    # ボタンスタイル
    # ==========================
    style = ttk.Style()
    style.configure("Blue.TButton",
                    font=('メイリオ', 18, 'bold'),
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
    # ボタンイベント
    # ==========================
    def jump_to_purchase():
        App.destroy()
        purchase.Purchase(account)

    def jump_to_sellitem():
        App.destroy()
        sellitems.Sellitems(account)

    def Close():
        App.destroy()

    def Back():
        App.destroy()
        home.Home(account)

    def Refresh():
        App.destroy()
        InAndOut(account)

    # ==========================
    # ボタン配置
    # ==========================
    btn_purchase = ttk.Button(card, text='単品入庫', style='White.TButton', command=jump_to_purchase)
    btn_purchase.place(x=60, y=50, width=150, height=120)

    btn_sell = ttk.Button(card, text='単品出庫', style='White.TButton', command=jump_to_sellitem)
    btn_sell.place(x=260, y=50, width=150, height=120)

    btn_import = ttk.Button(card, text='一括インポート', style='White.TButton', command=lambda: Open())
    btn_import.place(x=460, y=50, width=150, height=120)

    btn_refresh = ttk.Button(card, text='更新', style='White.TButton', command=Refresh)
    btn_refresh.place(x=60, y=240, width=150, height=50)

    btn_back = ttk.Button(card, text='戻る', style='White.TButton', command=Back)
    btn_back.place(x=260, y=240, width=150, height=50)

    btn_quit = ttk.Button(card, text='終了', style='White.TButton', command=Close)
    btn_quit.place(x=460, y=240, width=150, height=50)

    # ==========================
    # 一括インポート処理
    # ==========================
    def Open():
        filePath = filedialog.askopenfilename(filetypes=[('Excelファイル', '*.xls')])
        if not filePath:
            return
        try:
            workbook = xlrd.open_workbook(filePath)
            sheet = workbook.sheet_by_index(0)
        except Exception:
            messagebox.showerror('エラー', 'Excelファイルを読み込めません')
            return

        dates = sheet.col_values(0)[1:]
        InOrOut = sheet.col_values(1)[1:]
        attributes = sheet.col_values(2)[1:]
        names = sheet.col_values(3)[1:]
        prices = sheet.col_values(4)[1:]
        quantities = sheet.col_values(5)[1:]
        suppliers = sheet.col_values(6)[1:]

        for i in range(len(dates)):
            if InOrOut[i] == '入庫':
                result = purchase.PurchaseInsert(dates[i], attributes[i], names[i], prices[i], quantities[i], suppliers[i])
            else:
                result = sellitems.SellInsert(dates[i], attributes[i], names[i], prices[i], quantities[i])
            if result == -1:
                messagebox.showerror('警告', f'{i+1}行目のデータ登録失敗！該当アイテムなし')
            elif result == -2:
                messagebox.showerror('警告', f'{i+1}行目のデータ登録失敗！数量が不正')
        messagebox.showinfo('完了', '入出庫情報の一括インポートが完了しました！')

    App.mainloop()


if __name__ == "__main__":
    InAndOut('admin')
