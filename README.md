# determine_invest_day
投資信託に毎月積み立て投資をする場合に、月の積立日による成績の差を計算するPythonスクリプトです。

# How to use
* 以下のHPから投資信託の設定来データ(.csv)をダウンロードして、ファンド名をファイル名とします。

  1. [eMAXIS Slim 全世界株式（オール・カントリー）](https://www.am.mufg.jp/fund/253425.html)
  2. [eMAXIS Slim 米国株式（S&P500）](https://emaxis.jp/fund/253266.html)
  3. [SBI・V・S&P500インデックス・ファンド](https://apl.wealthadvisor.jp/webasp/sbi_am/pc/basic/chart/2019092601_chart.html)
  4. [＜購入・換金手数料なし＞ニッセイNASDAQ100インデックスファンド](https://www.nam.co.jp/fundinfo/nn100if/main.html)
  5. [iFreeNEXT FANG+インデックス](https://www.daiwa-am.co.jp/funds/detail/3346/detail_top.html)

* スクリプトを実行します。
  - `python determine_invest_day.py`
  - 上位3つのリターンとなる日、および最小～最大リターンの差が出力されます。
* Jupyter notebookで実行すると、上記に加えて、グラフで日毎の成績を表示します。

# Reference
* [オルカン他投資信託の約定日(月初～月末)別リターンの分析 - 白旗製作所](https://dededemio.hatenablog.jp/entry/2024/01/23/184000)
