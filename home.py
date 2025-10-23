import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pymysql
import InAndOut, statistics, subledger, transaction, createAndDelete, periodsummary, setting  # 自定义文件

# データベース接続
connect = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456', database='warehouse', charset='utf8')
cursor = connect.cursor()


def doSQL(sql):
    cursor.execute(sql)
    connect.commit()


def Home(account):
    """ 権限に応じて画面を切り替え """
    sql = "SELECT AUTHORITY FROM administrators WHERE ACCOUNT = '%s';"
    doSQL(sql % account)
    Authority = cursor.fetchall()[0][0]
    is_admin = Authority == 0
    MainApp(account, is_admin)


class HoverButton(tk.Button):
    """ マウスオーバー効果付きボタン """
    def __init__(self, master=None, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = kw.get('bg', '#34495e')
        self.activeBackground = kw.get('activebackground', '#357ABD')
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self.activeBackground

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class MainApp(tk.Tk):
    """ メイン画面（一般ユーザーと管理者共通） """

    def __init__(self, account, is_admin=False):
        super().__init__()
        self.account = account
        self.is_admin = is_admin

        # 基本ウィンドウ設定
        self.title('倉庫管理システム')
        self.geometry('900x700')
        self.resizable(False, False)
        self.configure(bg='#f0f2f5')

        # ----------------- サイドバー -----------------
        self.sidebar = tk.Frame(self, width=200, bg='#2c3e50')
        self.sidebar.pack(side='left', fill='y')

        # ----------------- メイン表示エリア -----------------
        self.main_area = tk.Frame(self, bg='white')
        self.main_area.pack(side='right', expand=True, fill='both')

        # メインタイトル
        tk.Label(self.main_area, text='倉庫管理システム', font=('メイリオ', 40, 'bold'), bg='white', fg='#2c3e50').pack(pady=40)
        tk.Label(self.main_area, text='Warehouse Management Information System', font=('メイリオ', 18), bg='white', fg='#34495e').pack()

        # ----------------- ボタンリスト -----------------
        btn_list = [
            ('在庫統計', self.jump_to_statistics),
            ('業務データ集計', self.jump_to_period),
            ('入出庫明細帳', subledger.Subleger)
        ]

        if self.is_admin:
            btn_list += [
                ('日常在庫管理', self.jump_to_management),
                ('期末業務繰越', self.jump_to_transaction),
                ('権限管理', self.jump_to_createAndDelete),
                ('倉庫設定', self.jump_to_setting)
            ]

        for text, cmd in btn_list:
            btn = HoverButton(self.sidebar, text=text, font=('メイリオ', 14), bg='#34495e', fg='white',
                              activebackground='#357ABD', relief='flat', command=cmd, width=20, height=2)
            btn.pack(pady=5)

        # ----------------- 下部操作ボタン -----------------
        refresh_btn = HoverButton(self.sidebar, text='更新', font=('メイリオ', 12), bg='#34495e', fg='white',
                                  activebackground='#357ABD', relief='flat', command=self.refresh, width=20, height=2)
        refresh_btn.pack(side='bottom', pady=10)

        quit_btn = HoverButton(self.sidebar, text='終了', font=('メイリオ', 12), bg='#34495e', fg='white',
                               activebackground='#e74c3c', relief='flat', command=self.destroy, width=20, height=2)
        quit_btn.pack(side='bottom', pady=10)

    # ----------------- 画面遷移関数 -----------------
    def jump_to_statistics(self):
        self.destroy()
        statistics.Statistics(self.account)

    def jump_to_period(self):
        self.destroy()
        periodsummary.PeriodSummary(self.account)

    def jump_to_management(self):
        self.destroy()
        InAndOut.InAndOut(self.account)

    def jump_to_transaction(self):
        self.destroy()
        transaction.Transaction(self.account)

    def jump_to_createAndDelete(self):
        self.destroy()
        createAndDelete.CreateAndDelete(self.account)

    def jump_to_setting(self):
        self.destroy()
        setting.Setting(self.account)

    def refresh(self):
        self.destroy()
        MainApp(self.account, self.is_admin)


if __name__ == "__main__":
    Home('admin')
