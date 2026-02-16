import requests
import csv
import io

# 1. 直接ファイルをダウンロードできる「直リンク」を指定
# カタログサイトのURLではなく、実際のファイルへのURLです
csv_url = "https://www.opendata.metro.tokyo.lg.jp/soumu/130001_evacuation_center.csv"

def print_csv_top_10(url):
    try:
        # ブラウザからのアクセスを装うためのヘッダー（拒否防止）
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # ステータスコードが200（成功）か確認
        response.raise_for_status()

        # 2. 文字コードの設定（東京都は utf-8-sig が一般的）
        # --- 修正ポイント：文字コードを cp932 (Shift-JIS) に変更 ---
        response.encoding = 'cp932'

        # 3. CSVとして読み込む
        # response.text をファイルのように扱える io.StringIO に渡す
        f = io.StringIO(response.text)
        reader = csv.reader(f)

        print("--- CSVの先頭10行を表示します ---")
        for i, row in enumerate(reader):
            if i >= 10: # 10行超えたら終了
                break
            print(f"行{i+1}: {row}")

    except requests.exceptions.RequestException as e:
        print(f"ネットワークエラー: {e}")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    print_csv_top_10(csv_url)