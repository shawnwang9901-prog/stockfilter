import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 定義要監控的股票（可自行自由增減）
stock_list = [
    # === AI 伺服器與代工巨頭 ===
    "2330.TW",   # 台積電
    "2317.TW",   # 鴻海
    "2454.TW",   # 聯發科
    "2382.TW",   # 廣達
    "3231.TW",   # 緯創
    "2356.TW",   # 英業達
    "2308.TW",   # 台達電
    "2324.TW",   # 仁寶
    "1582.TW",   # 信驊
    
    # === 散熱與機殼（短線波動極大） ===
    "3017.TW",   # 奇鋐
    "3324.TWO",  # 雙鴻
    "3653.TW",   # 健策
    "3013.TW",   # 晟銘電
    "8210.TW",   # 藍天
    "6125.TW",   # 廣運
    
    # === 矽光子與 CPO 概念股 ===
    "3363.TWO",  # 上詮
    "4979.TWO",  # 華星光
    "3450.TW",   # 聯鈞
    "6451.TW",   # 訊芯-KY
    "3081.TWO",  # 聯亞
    
    # === 半導體設備與先進封裝（CoWoS） ===
    "3131.TW",   # 弘塑
    "3583.TW",   # 辛耘
    "6187.TWO",  # 萬潤
    "2486.TW",   # 一詮
    "5443.TWO",  # 均豪
    "2467.TW",   # 志聖
    
    # === 重電、綠能、線纜（主力最愛炒作題材） ===
    "1513.TW",   # 中興電
    "1519.TW",   # 華城
    "1503.TW",   # 士電
    "1605.TW",   # 華新
    "1609.TW",   # 大亞
    "6806.TW",   # 森崴能源
    
    # === 機器人與自動化概念 ===
    "2359.TW",   # 所羅門
    "9960.TW",   # 邁達特
    "4583.TW",   # 台灣精銳
    "2365.TW",   # 昆盈
    
    # === 熱門 IC 設計與 IP 股 ===
    "3035.TW",   # 智原
    "3661.TW",   # 世芯-KY
    "3443.TW",   # 創意
    "6643.M",    # M31 (註：部分系統代碼可能為 6643.TWO，若抓不到可改)
    "8054.TWO",  # 安國
    
    # === 航運與傳統高成交量人氣股 ===
    "2603.TW",   # 長榮
    "2609.TW",   # 陽明
    "2615.TW",   # 萬海
    "2610.TW",   # 華航
    "2618.TW",   # 長榮航
    
    # === 其他近期強勢人氣指標 ===
    "2344.TW",   # 華邦電
    "2408.TW",   # 南亞科
    "2337.TW"    # 旺宏
]

qualified_stocks = []

print("開始分析今日數據...")

for stock_id in stock_list:
    try:
        ticker = yf.Ticker(stock_id)
        df = ticker.history(period="20d")
        if df.empty or len(df) < 5: continue
        
        # 算 5 日均線
        df['MA5'] = df['Close'].rolling(window=5).mean()
        today = df.iloc[-1]
        yesterday = df.iloc[-2]
        
        # 主要篩選條件：今天量大於 3000 (應急）張，且股價突破 5日線
        vol_chk = (today['Volume'] / 1000) > 1000
        price_chk = (yesterday['Close'] < yesterday['MA5']) and (today['Close'] > today['MA5'])
        
        if vol_chk and price_chk:
            qualified_stocks.append({
                "code": stock_id.replace(".TW", ""),
                "price": round(today['Close'], 2),
                "volume": int(today['Volume'] / 1000),
                "pct": round(((today['Close'] - yesterday['Close']) / yesterday['Close']) * 100, 2)
            })
    except Exception as e:
        print(f"錯誤 {stock_id}: {e}")

# 2. 編排網頁畫面美觀 (使用現代化的 Bootstrap 5 介面)
update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>短線強勢股篩選器</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; font-family: 'PingFang TC', sans-serif; }}
        .card {{ border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .table-hover tbody tr:hover {{ background-color: #f1f3f5; }}
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="card p-4 mb-4 bg-dark text-white text-center">
                    <h1 class="display-5 fw-bold">選股就該躺著選∠( ᐛ 」∠)＿</h1>
                    <p class="text-muted mb-0">更新時間：{update_time}</p>
                </div>
                
                <div class="card p-4">
                    <h3 class="mb-3 text-secondary">量化結果（自定義）</h3>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>股票代碼</th>
                                    <th>今日收盤價</th>
                                    <th>今日漲跌幅</th>
                                    <th>成交量 (張)</th>
                                </tr>
                            </thead>
                            <tbody>
"""

if not qualified_stocks:
    html_content += "<tr><td colspan='4' class='text-center text-muted py-4'>今日無符合條件股票</td></tr>"
else:
    for s in qualified_stocks:
        color = "text-danger" if s['pct'] > 0 else "text-success"
        sign = "+" if s['pct'] > 0 else ""
        html_content += f"""
                                <tr>
                                    <td><span class="badge bg-primary fs-6">{s['code']}</span></td>
                                    <td class="fw-bold">${s['price']}</td>
                                    <td class="{color} fw-bold">{sign}{s['pct']}%</td>
                                    <td>{s['volume']:,} 張</td>
                                </tr>
        """

html_content += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# 3. 輸出儲存成網頁檔案
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("網頁更新成功！")