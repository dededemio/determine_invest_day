# 毎月積み立て投資の約定日別リターンの違いを計算
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams['font.family'] = "Yu Gothic"

# 設定来データの整理
def organize_data():
    file = "eMAXIS Slim 全世界株式（オール・カントリー）.csv"
    df = pd.read_csv(file, encoding="shift-jis", header=1, index_col=0)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.to_csv(os.path.splitext(file)[0]+"_修正.csv", encoding="utf-8-sig")

    file = "eMAXIS Slim 米国株式（S&P500）.csv"
    df = pd.read_csv(file, encoding="shift-jis", header=1, index_col=0)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.to_csv(os.path.splitext(file)[0]+"_修正.csv", encoding="utf-8-sig")

    file = "＜購入・換金手数料なし＞ニッセイNASDAQ100インデックスファンド.csv"
    df = pd.read_csv(file, encoding="shift-jis", header=0, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y年%m月%d日")
    df = df.drop(df.columns[0], axis=1)
    df = df.sort_index()
    df.to_csv(os.path.splitext(file)[0]+"_修正.csv", encoding="utf-8-sig")

    file = "SBI・V・S&P500インデックス・ファンド.csv"
    df = pd.read_csv(file, encoding="shift-jis", header=0, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df = df.sort_index()
    df.to_csv(os.path.splitext(file)[0]+"_修正.csv", encoding="utf-8-sig")

    file = "iFreeNEXT FANG+インデックス.csv"
    df = pd.read_csv(file, encoding="shift-jis", header=0, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df = df.sort_index()
    df.to_csv(os.path.splitext(file)[0]+"_修正.csv", encoding="utf-8-sig")

# 毎月決まった日時に定期的に1万円購入した時のリターンを計算
def calc_return_by_day_of_month(df, title):
    return_by_day= []
    for d in np.arange(1, 31, 1):
        # 土日祝日は翌営業日買い付けのため、後ろ方向に穴埋め
        df_fill = df.asfreq("D", method="bfill") 
        # データ最初と最後の月途中のデータは削除
        first_month = df_fill.index[0].month
        first_year = df_fill.index[0].year
        last_month = df_fill.index[-1].month
        last_year = df_fill.index[-1].year
        df_fill = df_fill[(df_fill.index.year!=first_year) | (df_fill.index.month!=first_month)] # 最初に日付が1日になるまでのデータを削除
        df_fill = df_fill[(df_fill.index.year!=last_year) | (df_fill.index.month!=last_month)] # 最後の月末以降のデータを削除
        # 指定した日付に対応する価格を取得
        price_by_day = df_fill[df_fill.index.day==d][df_fill.columns[0]] # 毎月d日の基準価額
        # 2月は29日、30日が無い場合がある。この場合月末日買い付けとし、2月末日データを入れる
        if (d==29) or (d==30):
            price_by_day = price_by_day.resample("M", convention="end").ffill() # 毎月でリサンプル
            price_idx_feb = price_by_day[price_by_day.index.month==2].index # 2月末日の日付
            price_feb = [df_fill[df_fill.index==p][df_fill.columns[0]].values[0] for p in price_idx_feb] # 2月末日データをdf_fillから取得
            price_by_day[price_by_day.index.month==2]=price_feb # 2月末日データを代入
        # 総取得価格・取得株数と評価額からリターンを計算
        price_acquisition = price_by_day.sum() # 取得価格
        num_of_stocks = len(price_by_day) # 取得株数
        # print(num_of_stocks)
        price_estimate = num_of_stocks * df.tail(1)[df.columns[0]] # 評価額
        gain = (price_estimate - price_acquisition) / price_acquisition # リターン
        return_by_day.append(gain.values[0]*100)
    # リターンの上位3日の日付を表示
    top_3_idx = sorted(range(len(return_by_day)), key=lambda i: return_by_day[i], reverse=True)[:3]
    print(title+"の最大リターン日: "+str(top_3_idx))
    print("最小と最大のリターン差[%]: "+str(round(np.max(return_by_day)-np.min(return_by_day),1)))
    # 比較をグラフで出す
    plt.figure()
    plt.bar(np.arange(1, 31, 1), return_by_day)
    plt.grid()
    plt.title("毎月積み立て投資 約定日別リターンの違い\n"+title)
    plt.xlabel("日付")
    plt.ylabel("リターン[%]")
    diff = np.max(return_by_day) - np.min(return_by_day)
    plt.ylim([np.min(return_by_day)-diff/10, np.max(return_by_day)+diff/10])

# 株価ごとの日別リターン計算-----------------------------
if __name__ == "__main__":
    organize_data()
    files = os.listdir(os.getcwd())
    csvfiles = [f for f in files if "修正.csv" in f]
    for file in csvfiles:
        df = pd.read_csv(file, encoding="utf-8-sig", index_col=0, parse_dates=[0])
        title = file.split("_")[0]
        calc_return_by_day_of_month(df, title)
