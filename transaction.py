# -*- coding: utf-8 -*-
"""
倉庫管理：会計期間のトランザクション処理
機能：
1. 入出庫データ取得
2. FIFO/LIFO/加重平均に基づき在庫原価計算
3. 収益・費用の転記
4. Tkinterで会計期末サマリー表示
"""
import tkinter
import tkinter.ttk
import tkinter.messagebox
import pymysql
from PIL import Image, ImageTk
import home  # 自作モジュール

def Transaction(account):
    # ==========================
    # データベース接続
    # ==========================
    connect = pymysql.Connect(
        host='localhost', port=3306, user='root',
        passwd='123456', database='warehouse', charset='utf8'
    )
    cursor = connect.cursor()

    def doSQL(sql, params=None):
        """SQL実行関数"""
        cursor.execute(sql, params)
        connect.commit()
        return cursor.fetchall()

    # ==========================
    # 会計期間取得
    # ==========================
    App = tkinter.Tk()
    App.title('倉庫管理')
    App['height'] = 200
    App['width'] = 600

    try:
        timeBegin = doSQL("SELECT TIMEBEGIN FROM attribute")[0][0]
    except IndexError:
        tkinter.messagebox.showerror('警告', 'まず開始日を設定してください！')
        App.destroy()
        home.Home(account)
        return

    try:
        timeEnd = doSQL("SELECT TIMEEND FROM attribute")[0][0]
    except IndexError:
        tkinter.messagebox.showerror('警告', 'まず終了日を設定してください！')
        App.destroy()
        home.Home(account)
        return

    method = doSQL("SELECT METHOD FROM attribute")[0][0]  # コスト計算方法

    # ==========================
    # 指定日付までの在庫原価計算
    # ==========================
    def Search(Date, Name, Method):  # Name：商品名, Method：コスト計算方法
        # 入庫データ取得
        inner_imports = doSQL(
            "SELECT * FROM inhouse WHERE DATE <= %s AND NAME = %s",
            (Date, Name)
        )
        inner_imports = [list(i) for i in inner_imports]

        # 出庫データ取得
        inner_exports = doSQL(
            "SELECT * FROM outhouse WHERE DATE <= %s AND NAME = %s",
            (Date, Name)
        )
        inner_exports = [list(i) for i in inner_exports]

        k = 0
        for num in range(len(inner_exports)):
            if inner_exports[num][6] < inner_imports[k][6]:
                inner_imports[k][6] -= inner_exports[num][6]
            else:
                while inner_imports[k][6] < inner_exports[num][6]:
                    inner_exports[num][6] -= inner_imports[k][6]
                    k += 1
                inner_imports[k][6] -= inner_exports[num][6]

        totalValue, totalAmount = 0, 0
        for num in range(k, len(inner_imports)):
            totalAmount += inner_imports[num][6]
            totalValue += inner_imports[num][5] * inner_imports[num][6]

        if Method == 1:  # 先入先出
            return inner_imports[k][5] if totalAmount > 0 else 0
        elif Method == 2:  # 後入先出
            return inner_imports[-1][5] if totalAmount > 0 else 0
        elif Method == 3:  # 加重平均
            return totalValue / totalAmount if totalAmount > 0 else 0

    # ==========================
    # 会計期間内の入出庫取得
    # ==========================
    imports = [list(i) for i in doSQL(
        "SELECT * FROM inhouse WHERE DATE >= %s AND DATE <= %s",
        (timeBegin, timeEnd)
    )]
    exports = [list(i) for i in doSQL(
        "SELECT * FROM outhouse WHERE DATE >= %s AND DATE <= %s",
        (timeBegin, timeEnd)
    )]

    # ==========================
    # 主要勘定科目
    # ==========================
    StockGoods = 0     # 庫存商品
    OtherStockGoods = 0
    BankDeposit = 0
    AccountsPayable = 0
    AccountsReceivable = 0
    RawMaterial = 0
    OtherRawMaterial = 0
    MainBusinessIncome = 0
    MainBusinessCosts = 0
    OtherBusinessIncome = 0
    OtherBusinessCosts = 0

    i, j = 0, 0
    while i < len(imports) and j < len(exports):
        if imports[i][1] <= exports[j][1]:
            # 入庫処理
            record = imports[i]
            qty_value = record[5] * record[6]
            if record[3] in ['貨品購買', '貨品借入', '貨品調入']:
                StockGoods += qty_value
                if record[3] == '貨品購買':
                    BankDeposit -= qty_value
                elif record[3] == '貨品借入':
                    AccountsPayable += qty_value
                else:
                    OtherStockGoods -= qty_value
            elif record[3] in ['材料購買', '材料借入', '材料調入']:
                RawMaterial += qty_value
                if record[3] == '材料購買':
                    BankDeposit -= qty_value
                elif record[3] == '材料借入':
                    AccountsPayable += qty_value
                else:
                    OtherRawMaterial -= qty_value
            elif record[3] == '貨品返還(顧客)':
                MainBusinessIncome -= qty_value
                BankDeposit -= qty_value
                Cost = Search(record[1], record[4], {'先入先出':1,'後入先出':2,'加重平均':3}[method])
                StockGoods += qty_value
                MainBusinessCosts -= Cost * record[6]
            i += 1
        else:
            # 出庫処理
            record = exports[j]
            qty_value = record[5] * record[6]
            if record[3] == '貨品販売':
                BankDeposit += qty_value
                MainBusinessIncome += qty_value
                Cost = Search(record[1], record[4], {'先入先出':1,'後入先出':2,'加重平均':3}[method])
                MainBusinessCosts += Cost * record[6]
                StockGoods -= Cost * record[6]
            elif record[3] == '貨品返還仕入先':
                StockGoods -= qty_value
                BankDeposit += qty_value
            elif record[3] == '貨品貸出':
                AccountsReceivable += qty_value
                StockGoods -= qty_value
            elif record[3] == '貨品移出':
                OtherStockGoods += qty_value
                StockGoods -= qty_value
            elif record[3] == '材料販売':
                BankDeposit += qty_value
                OtherBusinessIncome += qty_value
                OtherBusinessCosts -= qty_value
                RawMaterial -= qty_value
            elif record[3] == '材料返還仕入先':
                RawMaterial -= qty_value
                BankDeposit += qty_value
            elif record[3] == '材料貸出':
                AccountsReceivable += qty_value
                RawMaterial -= qty_value
            elif record[3] == '材料移出':
                OtherRawMaterial += qty_value
                RawMaterial -= qty_value
            j += 1

    # ==========================
    # 利益計算
    # ==========================
    Profit = (MainBusinessIncome + OtherBusinessIncome) - (MainBusinessCosts + OtherBusinessCosts)

    # ==========================
    # Tkinterで表示
    # ==========================
    table = tkinter.ttk.Treeview(App, show='headings')
    table.place(relx=0.004, rely=0.028, relwidth=0.964, relheight=0.95)
    xscroll = tkinter.Scrollbar(table, orient='horizontal', command=table.xview)
    yscroll = tkinter.Scrollbar(table, orient='vertical', command=table.yview)
    xscroll.place(relx=0.028, rely=0.971, relwidth=0.958, relheight=0.024)
    yscroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
    table.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

    table['columns'] = ['A', 'B']
    table.column('A', width=150, anchor='center')
    table.column('B', width=150, anchor='center')
    table.heading('A', text='項目', anchor='center')
    table.heading('B', text='内容', anchor='center')
    table.insert('', 0, values=('会計開始日', timeBegin))
    table.insert('', 1, values=('会計終了日', timeEnd))
    table.insert('', 2, values=('総収入', MainBusinessIncome + OtherBusinessIncome))
    table.insert('', 3, values=('総費用', MainBusinessCosts + OtherBusinessCosts))
    table.insert('', 4, values=('総利益', Profit))

    App.mainloop()
    home.Home(account)


if __name__ == "__main__":
    Transaction('admin')
