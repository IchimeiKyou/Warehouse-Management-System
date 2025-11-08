## 概要
- 本倉庫管理システムは、Python（tkinter・pymysql・pandas）および MySQL を用いて設計・開発いたしました。入庫・出庫から在庫照会、統計分析に至る在庫の全工程管理および自動レポート生成を実現しております。
- また、管理者および一般ユーザーの階層別権限制御をサポートしており、在庫の上下限に応じた自動警告、データの一括インポート、異常トランザクションのロールバック機能を備えることで、データの一貫性と信頼性を確保しております。
- さらに、直感的に操作可能な GUI を提供し、Excel 形式でのデータエクスポートも可能であるため、在庫管理の効率およびデータ処理精度を大幅に向上させることができました。
## ファイル
```text
倉庫管理システム
├── InAndOut.py  # 商品・原材料の入出庫を管理します。データの検証、データベースへの登録、在庫取引の取得を含みます。
├── create.py  # 新しい在庫品目、会計科目、関連データベースレコードを作成する機能を提供します。
├── createAndDelete.py  # システム内の在庫品目、会計科目、補助レコードの作成と削除の機能を統合します。
├── delete.py  # 在庫品目、会計科目、関連データベースレコードの削除を処理し、確認ダイアログを表示します。
├── home.py  # ログイン後のホーム画面。倉庫管理システムの全機能へのナビゲーションを提供します。
├── log.py  # ユーザーのログインとログ記録を管理します。認証情報を検証し、ログイン履歴を記録します。
├── main.py  # 倉庫管理システムのメインエントリーポイント。データベース接続を初期化し、ホーム画面を起動します。
├── periodsummary.py  # 選択した会計期間の総収入、総費用、純利益などの期間集計を生成します。
├── purchase.py  # 商品および原材料の購入取引を処理し、在庫および会計記録を更新します。
├── sellitems.py  # 販売取引を処理します。収益計算、在庫減少、原価配分を含みます。
├── setting.py  # 会計期間、原価計算方法、ユーザー設定など、システムの設定を管理します。
├── statistics.py  # 指定期間の在庫、売上、費用の統計分析を提供します。チャートや集計レポートの生成も可能です。
├── subledger.py  # 補助元帳の詳細を管理します。在庫の動き、原材料、関連する会計仕訳を含みます。
└── transaction.py  # 会計期間中のすべての取引を処理します。FIFO/LIFO/加重平均法で売上原価を計算し、期間利益を算出します。
```
- ### login (ログイン/登录)
![login](./image/login.png)
- ### home (ホーム/主页)
![home](./image/home.png)
- ### statistic (統計/统计)
![statistic](./image/statistic.png)
- ### summary (集計/汇总)
![summary](./image/summary.png)
- ### detail (明細/明细)
![detail](./image/detail.png)
- ### userManagement (ユーザー管理/用户管理)
![userManagement](./image/userManagement.png)
- ### addUser (ユーザー作成/用户添加)
![addUser](./image/addUser.png)
- ### deleteUser (ユーザー削除/用户删除)
![deleteUser](./image/deleteUser.png)
- ### setting (設定/设置)
![setting](./image/setting.png)

---

## Overview
- This warehouse management system was designed and developed using Python (tkinter, pymysql, pandas) and MySQL. It enables comprehensive inventory workflow management, from inbound and outbound operations to inventory queries and statistical analysis, as well as automated report generation.
- The system supports hierarchical access control for administrators and general users, implements automatic alerts based on inventory thresholds, allows bulk data import, and provides rollback of abnormal transactions, ensuring data consistency and reliability.
- In addition, it offers an intuitive GUI for operations and supports Excel export, significantly improving inventory management efficiency and data processing accuracy.
## Files
``` text
Software Mangement System
├── InAndOut.py  # Handles import and export of goods and materials. Includes data validation, database insertion, and retrieval for inventory transactions.
├── create.py  # Provides functions to create new inventory items, accounts, or related database records.
├── createAndDelete.py  # Combines creation and deletion functionalities for inventory items, accounts, and auxiliary records in the system.
├── delete.py  # Handles deletion of inventory items, accounts, or related database records, with confirmation dialogs.
├── home.py  # Main home screen after login. Provides navigation to all functionalities of the warehouse management system.
├── log.py  # Manages user login and logging events. Validates credentials and records login history.
├── main.py  # Main entry point for the warehouse management system. Initializes database connection and launches the home interface.
├── periodsummary.py  # Generates period summaries including total income, total costs, and net profit for a selected accounting period.
├── purchase.py  # Handles purchase transactions of goods and raw materials, updates inventory and accounting records.
├── sellitems.py  # Handles sales transactions, including revenue calculation, inventory reduction, and cost allocation.
├── setting.py  # Manages system configuration and settings, such as accounting period, cost method, and user preferences.
├── statistics.py  # Provides statistical analysis of inventory, sales, and costs over a given period. Can generate charts or summaries.
├── subledger.py  # Manages subsidiary ledger details, including inventory movements, raw materials, and related accounting entries.
└── transaction.py  # Processes all transactions during an accounting period. Calculates cost of goods sold using FIFO/LIFO/Weighted Average and computes period profit.
```
---
## 概述
- 本仓库管理系统使用 Python（tkinter、pymysql、pandas）和 MySQL 设计并开发，实现了从入库、出库到库存查询和统计分析的全流程管理，并支持自动报表生成。
- 系统支持管理员和普通用户的分层权限控制，具备根据库存上下限自动预警、批量数据导入及异常交易回滚功能，确保数据的一致性和可靠性。
- 此外，提供直观的 GUI 操作，并支持 Excel 导出，大幅提升了库存管理效率和数据处理精度。
## 文件结构
```text
仓库管理系统
├── InAndOut.py  # 管理商品和原材料的入库和出库。包括数据验证、数据库插入以及库存交易的查询。
├── create.py  # 提供创建新库存物品、会计科目或相关数据库记录的功能。
├── createAndDelete.py  # 整合系统中库存物品、会计科目及辅助记录的创建和删除功能。
├── delete.py  # 处理库存物品、会计科目或相关数据库记录的删除，并提供确认对话框。
├── home.py  # 登录后的主界面，提供仓库管理系统所有功能的导航。
├── log.py  # 管理用户登录及日志记录，验证凭证并记录登录历史。
├── main.py  # 仓库管理系统的主入口，初始化数据库连接并启动主界面。
├── periodsummary.py  # 生成会计期间的汇总，包括总收入、总成本和净利润。
├── purchase.py  # 处理商品和原材料的采购交易，更新库存和会计记录。
├── sellitems.py  # 处理销售交易，包括收入计算、库存减少和成本分配。
├── setting.py  # 管理系统配置与设置，如会计期间、成本方法及用户偏好。
├── statistics.py  # 提供指定期间的库存、销售及成本统计分析，可生成图表或汇总。
├── subledger.py  # 管理辅助账明细，包括库存流动、原材料及相关会计分录。
└── transaction.py  # 处理会计期间的所有交易。使用 FIFO/LIFO/加权平均法计算销售成本并计算期间利润。
```
