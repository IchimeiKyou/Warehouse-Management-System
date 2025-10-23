import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import home

# データベース接続（既存インターフェースを保持）
connect = pymysql.Connect(
    host='localhost', port=3306, user='root', passwd='123456',
    database='warehouse', charset='utf8'
)
cursor = connect.cursor()

def doSQL(sql):
    cursor.execute(sql)
    connect.commit()

# ホバー効果付きボタンクラス
class HoverButton(tk.Button):
    def __init__(self, master=None, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_bg = kw.get('bg', '#34495e')
        self.hover_bg = kw.get('activebackground', '#357ABD')
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.config(cursor='hand2')

    def on_enter(self, e):
        self['background'] = self.hover_bg

    def on_leave(self, e):
        self['background'] = self.default_bg

# 倉庫設定画面
def Setting(account):
    class WarehouseSetting(tk.Tk):
        def __init__(self):
            super().__init__()
            self.account = account
            self.title('倉庫設定')
            self.geometry('900x600')
            self.resizable(False, False)
            self.configure(bg='#f0f2f5')

            # 左側ナビゲーション
            self.sidebar = tk.Frame(self, width=200, bg='#2c3e50')
            self.sidebar.pack(side='left', fill='y')

            # メイン操作エリア
            self.main_area = tk.Frame(self, bg='white')
            self.main_area.pack(side='right', expand=True, fill='both')

            # タイトル
            tk.Label(self.main_area, text='倉 庫 設 定', font=('メイリオ', 40, 'bold'),
                     bg='white', fg='#2c3e50').pack(pady=(40, 10))
            tk.Label(self.main_area, text='Warehouse Settings', font=('メイリオ', 18),
                     bg='white', fg='#34495e').pack(pady=(0, 30))

            # コスト計算方法
            frame_method = tk.Frame(self.main_area, bg='white')
            frame_method.pack(pady=10, anchor='w', padx=50)
            tk.Label(frame_method, text='(一) デフォルトコスト計算方法 :', font=('メイリオ', 15),
                     bg='white').grid(row=0, column=0, sticky='w')
            self.varMethod = tk.IntVar(value=1)
            tk.Radiobutton(frame_method, text='先入先出', variable=self.varMethod, value=1,
                           font=('メイリオ', 14), bg='white').grid(row=0, column=1, padx=20)
            tk.Radiobutton(frame_method, text='後入先出', variable=self.varMethod, value=2,
                           font=('メイリオ', 14), bg='white').grid(row=0, column=2, padx=20)
            tk.Radiobutton(frame_method, text='加重平均', variable=self.varMethod, value=3,
                           font=('メイリオ', 14), bg='white').grid(row=1, column=1, padx=20)

            # 在庫上限・下限
            frame_limit = tk.Frame(self.main_area, bg='white')
            frame_limit.pack(pady=10, anchor='w', padx=50)
            tk.Label(frame_limit, text='(二) 在庫上限・下限 :', font=('メイリオ', 15), bg='white').grid(row=0, column=0)
            self.varLow = tk.StringVar()
            self.varHigh = tk.StringVar()
            tk.Entry(frame_limit, textvariable=self.varLow, font=('メイリオ', 14), width=10,
                     justify='center').grid(row=0, column=1, padx=10)
            tk.Label(frame_limit, text='--', font=('メイリオ', 14), bg='white').grid(row=0, column=2, padx=5)
            tk.Entry(frame_limit, textvariable=self.varHigh, font=('メイリオ', 14), width=10,
                     justify='center').grid(row=0, column=3, padx=10)

            # 業務締め日
            frame_date = tk.Frame(self.main_area, bg='white')
            frame_date.pack(pady=10, anchor='w', padx=50)
            tk.Label(frame_date, text='(三) 業務締め日 :', font=('メイリオ', 15), bg='white').grid(row=0, column=0, columnspan=6, sticky='w')

            # 開始日
            tk.Label(frame_date, text='開始日 :', font=('メイリオ', 14), bg='white').grid(row=1, column=0, pady=10)
            self.varDate_year_start = tk.StringVar()
            self.varDate_month_start = tk.StringVar()
            self.varDate_day_start = tk.StringVar()
            tk.Entry(frame_date, textvariable=self.varDate_year_start, width=6, font=('メイリオ', 14)).grid(row=1, column=1)
            tk.Label(frame_date, text=' 年 ', font=('メイリオ', 12), bg='white').grid(row=1, column=2)
            tk.Entry(frame_date, textvariable=self.varDate_month_start, width=4, font=('メイリオ', 14)).grid(row=1, column=3)
            tk.Label(frame_date, text=' 月 ', font=('メイリオ', 12), bg='white').grid(row=1, column=4)
            tk.Entry(frame_date, textvariable=self.varDate_day_start, width=4, font=('メイリオ', 14)).grid(row=1, column=5)
            tk.Label(frame_date, text=' 日 ', font=('メイリオ', 12), bg='white').grid(row=1, column=6)

            # 終了日
            tk.Label(frame_date, text='終了日 :', font=('メイリオ', 14), bg='white').grid(row=2, column=0, pady=10)
            self.varDate_year_end = tk.StringVar()
            self.varDate_month_end = tk.StringVar()
            self.varDate_day_end = tk.StringVar()
            tk.Entry(frame_date, textvariable=self.varDate_year_end, width=6, font=('メイリオ', 14)).grid(row=2, column=1)
            tk.Label(frame_date, text=' 年 ', font=('メイリオ', 12), bg='white').grid(row=2, column=2)
            tk.Entry(frame_date, textvariable=self.varDate_month_end, width=4, font=('メイリオ', 14)).grid(row=2, column=3)
            tk.Label(frame_date, text=' 月 ', font=('メイリオ', 12), bg='white').grid(row=2, column=4)
            tk.Entry(frame_date, textvariable=self.varDate_day_end, width=4, font=('メイリオ', 14)).grid(row=2, column=5)
            tk.Label(frame_date, text=' 日 ', font=('メイリオ', 12), bg='white').grid(row=2, column=6)

            # 左側ボタン
            btn_style = {'font': ('メイリオ', 14), 'bg': '#34495e', 'fg': 'white',
                         'activebackground': '#2c3e50', 'width': 18, 'height': 2, 'relief': 'flat'}
            HoverButton(self.sidebar, text='確認', command=self.commit, **btn_style).pack(pady=20)
            HoverButton(self.sidebar, text='戻る', command=self.back, **btn_style).pack(pady=20)
            HoverButton(self.sidebar, text='終了', command=self.destroy, **btn_style).pack(side='bottom', pady=20)

        # ----------------- 確認 -----------------
        def commit(self):
            try:
                # コスト計算方法更新
                if self.varMethod.get() == 1:
                    doSQL("update attribute set METHOD='先入先出'")
                elif self.varMethod.get() == 2:
                    doSQL("update attribute set METHOD='後入先出'")
                else:
                    doSQL("update attribute set METHOD='加重平均'")

                # 在庫上限・下限更新
                low = float(self.varLow.get())
                high = float(self.varHigh.get())
                if low < 0 or high < 0 or low >= high:
                    raise ValueError('在庫上限・下限エラー')
                doSQL(f"update attribute set MIN={low}, MAX={high}")

                # 業務締め日更新
                startDate = f"{self.varDate_year_start.get()}-{self.varDate_month_start.get()}-{self.varDate_day_start.get()}"
                endDate = f"{self.varDate_year_end.get()}-{self.varDate_month_end.get()}-{self.varDate_day_end.get()}"
                doSQL(f"update attribute set TIMEBEGIN='{startDate}', TIMEEND='{endDate}'")
            except:
                messagebox.showerror('エラー', '入力データに誤りがあります！')
                return
            messagebox.showinfo('完了', '倉庫設定を保存しました')
            self.destroy()
            home.Home(self.account)

        def back(self):
            self.destroy()
            home.Home(self.account)

    WarehouseSetting().mainloop()


if __name__ == "__main__":
    Setting('admin')
