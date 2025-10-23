"""
本ファイルは商品入出庫明細を生成（期間指定、完成）
アルゴリズム：入庫・出庫データを読み取り、日時優先で出力
"""
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog
import pymysql
import os
from openpyxl import Workbook


def Subleger():
    connect = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', database='warehouse',
                              charset='utf8')
    cursor = connect.cursor()

    def doSQL(sql):
        cursor.execute(sql)
        connect.commit()

    App = tkinter.Tk()
    App.title("入出庫明細")
    App['height'] = 650
    App['width'] = 800

    table = tkinter.ttk.Treeview(App, show='headings')
    table.place(relx=0.004, rely=0.028, relwidth=0.964, relheight=0.85)

    xscroll = tkinter.Scrollbar(table, orient='horizontal', command=table.xview)
    yscroll = tkinter.Scrollbar(table, orient='vertical', command=table.yview)
    xscroll.place(relx=0.028, rely=0.971, relwidth=0.958, relheight=0.024)
    yscroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
    table.configure(xscrollcommand=xscroll.set)
    table.configure(yscrollcommand=yscroll.set)

    table['columns'] = ['date', 'type', 'attribute', 'name', 'in-num', 'in-price', 'in-total', 'out-num', 'out-price', 'out-total',
                        'left-num']

    table.column('date', width=130, anchor='center')
    table.column('type', width=130, anchor='center')
    table.column('attribute', width=100, anchor='center')
    table.column('name', width=100, anchor='center')
    table.column('in-num', width=100, anchor='center')
    table.column('in-price', width=100, anchor='center')
    table.column('in-total', width=100, anchor='center')
    table.column('out-num', width=100, anchor='center')
    table.column('out-price', width=100, anchor='center')
    table.column('out-total', width=100, anchor='center')
    table.column('left-num', width=100, anchor='center')

    table.heading('date', text='日付', anchor='center')
    table.heading('type', text='入出庫区分', anchor='center')
    table.heading('attribute', text='業務属性', anchor='center')
    table.heading('name', text='品名', anchor='center')
    table.heading('in-num', text='入庫数量', anchor='center')
    table.heading('in-price', text='入庫単価', anchor='center')
    table.heading('in-total', text='入庫合計', anchor='center')
    table.heading('out-num', text='出庫数量', anchor='center')
    table.heading('out-price', text='出庫単価', anchor='center')
    table.heading('out-total', text='出庫合計', anchor='center')
    table.heading('left-num', text='残高数量', anchor='center')

    sql = "SELECT DATE, ATTRIBUTE, NAME, PRICE, QUANTITY, BALANCE FROM inhouse;"
    doSQL(sql)
    In = [i for i in cursor.fetchall()]

    sql = "SELECT DATE, ATTRIBUTE, NAME, PRICE, QUANTITY, BALANCE FROM outhouse;"
    doSQL(sql)
    Out = [i for i in cursor.fetchall()]

    i, j, k = 0, 0, 0
    result = []

    while i < len(In) and j < len(Out):
        if In[i][0] <= Out[j][0]:
            table.insert('', k, value=(In[i][0], '入庫', In[i][1], In[i][2], In[i][3], In[i][4],
                                       float(In[i][3]) * float(In[i][4]), '', '', '', In[i][5]))
            result.append([In[i][0], '入庫', In[i][1], In[i][2], In[i][3], In[i][4],
                           float(In[i][3]) * float(In[i][4]), '', '', '', In[i][5]])
            i += 1
            k += 1
        else:
            table.insert('', k, value=(Out[j][0], '出庫', Out[j][1], Out[j][2], '', '', '', Out[j][3],
                                       Out[j][4], float(Out[j][3]) * float(Out[j][4]), Out[j][5]))
            result.append([Out[j][0], '出庫', Out[j][1], Out[j][2], '', '', '', Out[j][3],
                           Out[j][4], float(Out[j][3]) * float(Out[j][4]), Out[j][5]])
            j += 1
            k += 1
    while i < len(In):
        table.insert('', k, value=(In[i][0], '入庫', In[i][1], In[i][2], In[i][3], In[i][4],
                                   float(In[i][3]) * float(In[i][4]), '', '', '', In[i][5]))
        result.append([In[i][0], '入庫', In[i][1], In[i][2], In[i][3], In[i][4],
                       float(In[i][3]) * float(In[i][4]), '', '', '', In[i][5]])
        i += 1
        k += 1
    while j < len(Out):
        table.insert('', k, value=(Out[j][0], '出庫', Out[j][1], Out[j][2], '', '', '', Out[j][3],
                                   Out[j][4], float(Out[j][3]) * float(Out[j][4]), Out[j][5]))
        result.append([Out[j][0], '出庫', Out[j][1], Out[j][2], '', '', '', Out[j][3],
                       Out[j][4], float(Out[j][3]) * float(Out[j][4]), Out[j][5]])
        j += 1
        k += 1

    table.insert('', k, value=('', '', '', '', '', '', '', '', '', '', ''))

    def Close():
        App.destroy()

    s = tkinter.ttk.Style()
    s.configure('my.TButton', font=('メイリオ', 12), background='silver')

    buttonClose = tkinter.ttk.Button(App, text='閉じる', style='my.TButton', command=Close)
    buttonClose.place(x=250, y=580, width=100, height=40)

    def toExcel():
        try:
            columns = ['入出庫日', '入出庫区分', '業務属性', '品名', '入庫数量', '入庫単価', '入庫合計',
                       '出庫数量', '出庫単価', '出庫合計', '残高数量']
            if result:
                wb = Workbook()
                wb1 = wb.create_sheet('index', 0)
                wb1.title = '入出庫明細データ'
                filename = tkinter.filedialog.asksaveasfilename(filetypes=[('xlsx', '*.xlsx')], initialdir='C:\\')
                filename = filename + '.xlsx'
                wb1.append(columns)
                for row in result:
                    wb1.append(row)
                wb.save(filename)
                tkinter.messagebox.showinfo("完了", "ファイルを保存しました！")
            else:
                tkinter.messagebox.showinfo("警告", "データが取得できませんでした！")
        except Exception as E:
            print(E)
            tkinter.messagebox.showinfo("エラー", "ファイル保存中にエラーが発生しました。再試行してください！")

    buttonExcel = tkinter.ttk.Button(App, text='Excelに出力', style='my.TButton', command=toExcel)
    buttonExcel.place(x=450, y=580, width=120, height=40)

    App.mainloop()


if __name__ == '__main__':
    Subleger()
