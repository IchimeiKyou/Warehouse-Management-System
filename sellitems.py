import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import InAndOut


def Sellitems(account):
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
    App.title('出庫管理 - Warehousing')
    App.geometry('900x600')
    App.config(bg='#1E3D59')
    App.resizable(False, False)

    # ==========================
    # タイトル
    # ==========================
    tk.Label(App, text='貨品 / 材料 出庫', bg='#1E3D59', fg='white',
             font=('メイリオ', 42, 'bold')).place(relx=0.5, y=80, anchor='center')
    tk.Label(App, text='Sell / Material Outbound', bg='#1E3D59', fg='white',
             font=('メイリオ', 18)).place(relx=0.5, y=140, anchor='center')

    # ==========================
    # 白色カード
    # ==========================
    card = tk.Frame(App, bg='white', width=700, height=380, relief='ridge', bd=2)
    card.place(relx=0.5, rely=0.65, anchor='center')

    # ==========================
    # スタイル
    # ==========================
    style = ttk.Style()
    style.configure("Blue.TButton", font=('メイリオ', 15, 'bold'),
                    background='#1E3D59', foreground='white', borderwidth=0)
    style.map("Blue.TButton", background=[('active', '#244E73')])

    style.configure("White.TButton", font=('メイリオ', 15, 'bold'),
                    background='white', foreground='#1E3D59', borderwidth=2)
    style.map("White.TButton", background=[('active', '#E5E5E5')])

    # ==========================
    # 入力フィールド
    # ==========================
    varName = tk.StringVar()
    varAttribute = tk.StringVar()
    varDate_year = tk.StringVar()
    varDate_month = tk.StringVar()
    varDate_day = tk.StringVar()
    varDate_hour = tk.StringVar()
    varDate_minute = tk.StringVar()
    varAmount = tk.StringVar()
    varPrice = tk.StringVar()

    tk.Label(card, text='出庫品名:', bg='white', fg='#1E3D59', font=('メイリオ', 15)).place(x=50, y=40)
    tk.Entry(card, textvariable=varName, font=('メイリオ', 13), justify='center').place(x=160, y=40, width=150, height=30)

    tk.Label(card, text='出庫属性:', bg='white', fg='#1E3D59', font=('メイリオ', 15)).place(x=340, y=40)
    ttk.Combobox(card, values=('貨品販売', '貨品供給者返却', '貨品貸出', '貨品移出',
                               '材料供給者返却', '材料貸出', '材料移出'),
                 textvariable=varAttribute, font=('メイリオ', 13)).place(x=450, y=40, width=200, height=30)

    tk.Label(card, text='出庫時間:', bg='white', fg='#1E3D59', font=('メイリオ', 15)).place(x=50, y=100)
    tk.Entry(card, textvariable=varDate_year, font=('メイリオ', 10), justify='center').place(x=160, y=100, width=50, height=30)
    tk.Label(card, text='年', bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=215, y=100)
    tk.Entry(card, textvariable=varDate_month, font=('メイリオ', 10), justify='center').place(x=240, y=100, width=40, height=30)
    tk.Label(card, text='月', bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=285, y=100)
    tk.Entry(card, textvariable=varDate_day, font=('メイリオ', 10), justify='center').place(x=310, y=100, width=40, height=30)
    tk.Label(card, text='日', bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=355, y=100)
    tk.Entry(card, textvariable=varDate_hour, font=('メイリオ', 10), justify='center').place(x=380, y=100, width=40, height=30)
    tk.Label(card, text='時', bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=425, y=100)
    tk.Entry(card, textvariable=varDate_minute, font=('メイリオ', 10), justify='center').place(x=450, y=100, width=40, height=30)
    tk.Label(card, text='分', bg='white', fg='#1E3D59', font=('メイリオ', 12)).place(x=495, y=100)

    tk.Label(card, text='出庫数量:', bg='white', fg='#1E3D59', font=('メイリオ', 15)).place(x=50, y=160)
    tk.Entry(card, textvariable=varAmount, font=('メイリオ', 12), justify='center').place(x=160, y=160, width=100, height=30)
    tk.Label(card, text='出庫単価:', bg='white', fg='#1E3D59', font=('メイリオ', 15)).place(x=290, y=160)
    tk.Entry(card, textvariable=varPrice, font=('メイリオ', 12), justify='center').place(x=400, y=160, width=100, height=30)

    # ==========================
    # データ挿入ロジック
    # ==========================
    def Insert(date, attribute, name, price, amount):
        if amount == '' or float(amount) <= 0 or price == '' or float(price) <= 0:
            return -1

        sql = "select max(LIST) from outhouse;"
        doSQL(sql)
        lis = cursor.fetchall()[0][0] or 0

        sql = "select max(ID) from commodity;"
        doSQL(sql)
        IDCommodity = cursor.fetchall()[0][0] or 0

        sql = "select NAME from commodity;"
        doSQL(sql)
        NameCommodity = [i[0] for i in cursor.fetchall()] if cursor.fetchall() else []

        sql = "select max(ID) from material;"
        doSQL(sql)
        IDMaterial = cursor.fetchall()[0][0] or 0

        sql = "select NAME from material;"
        doSQL(sql)
        NameMaterial = [i[0] for i in cursor.fetchall()] if cursor.fetchall() else []

        try:
            if attribute[:2] == '貨品':
                sql = "select QUANTITY from commodity where NAME='%s'"
            else:
                sql = "select QUANTITY from material where NAME='%s'"
            cursor.execute(sql % name)
            result = cursor.fetchall()
            quantity = float(result[0][0]) if result else 0

            data = (lis + 1, date, attribute[:2], attribute, name, float(price),
                    float(amount), quantity - float(amount))

            sql_insert = "INSERT INTO outhouse(LIST, DATE, TYPE, ATTRIBUTE, NAME, PRICE, QUANTITY, BALANCE) " \
                         "VALUES ('%d','%s','%s','%s','%s','%f','%f','%f');"
            cursor.execute(sql_insert % data)

        except Exception as e:
            print(e)
            connect.rollback()
            return -1

        # ------------------- 更新 commodity または material -------------------
        if attribute[:2] == '貨品':
            if name not in NameCommodity:
                connect.rollback()
                return -1
            sql = "SELECT QUANTITY FROM commodity WHERE NAME='%s'"
            cursor.execute(sql % name)
            quantity = float(cursor.fetchall()[0][0])
            if quantity < float(amount):
                connect.rollback()
                return -2
            sql = "UPDATE commodity SET QUANTITY='%f' WHERE NAME='%s'"
            cursor.execute(sql % (quantity - float(amount), name))
        else:
            if name not in NameMaterial:
                connect.rollback()
                return -1
            sql = "SELECT QUANTITY FROM material WHERE NAME='%s'"
            cursor.execute(sql % name)
            quantity = float(cursor.fetchall()[0][0])
            if quantity < float(amount):
                connect.rollback()
                return -2
            sql = "UPDATE material SET QUANTITY='%f' WHERE NAME='%s'"
            cursor.execute(sql % (quantity - float(amount), name))

        connect.commit()
        return 0

    def commit():
        date = f"{varDate_year.get()}-{varDate_month.get()}-{varDate_day.get()} {varDate_hour.get()}:{varDate_minute.get()}:00"
        result = Insert(date, varAttribute.get(), varName.get(), varPrice.get(), varAmount.get())
        if result == -1:
            messagebox.showerror("エラー", "存在しない品目または不完全なデータ！")
            return
        elif result == -2:
            messagebox.showerror("エラー", "在庫不足！")
            return
        messagebox.showinfo("成功", "出庫情報を登録しました！")
        Sellitems(account)
        App.destroy()

    def Back():
        App.destroy()
        InAndOut.InAndOut(account)

    # ==========================
    # ボタン
    # ==========================
    ttk.Button(card, text='確認', style='White.TButton', command=commit).place(x=160, y=300, width=160, height=50)
    ttk.Button(card, text='戻る', style='White.TButton', command=Back).place(x=370, y=300, width=160, height=50)

    App.mainloop()


if __name__ == "__main__":
    Sellitems('admin')
