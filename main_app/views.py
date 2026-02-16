import csv
import io
import requests
import json
from django.shortcuts import render


def shelter_search_view(request):
    csv_url = "https://www.opendata.metro.tokyo.lg.jp/soumu/130001_evacuation_center.csv"
    shelter_list = []

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(csv_url, headers=headers)
        response.encoding = 'cp932'

        # 生のテキストを行ごとに分割
        lines = response.text.splitlines()

        # --- 修正ポイント：実データがある行を探す ---
        # 1行目が空の場合があるため、'避難所_施設名称'が含まれる行をヘッダーとして特定
        header_index = 0
        for i, line in enumerate(lines):
            if '避難所_施設名称' in line:
                header_index = i
                break

        # ヘッダー以降のデータのみを対象にする
        f = io.StringIO('\n'.join(lines[header_index:]))
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get('避難所_施設名称')
            # 施設名が入っていない行、またはヘッダー行そのものはスキップ
            if not name or name == '避難所_施設名称':
                continue

            shelter_list.append({
                'name': name.strip(),
                'address': row.get('所在地住所', '').strip(),
                'lat': row.get('緯度', '').strip(),
                'lon': row.get('経度', '').strip(),
            })

    except Exception as e:
        print(f"Error: {e}")

    # サーバーのターミナルに件数を表示（デバッグ用）
    print(f"DEBUG: 読み込み件数 = {len(shelter_list)}件")

    shelter_json = json.dumps(shelter_list, ensure_ascii=False)
    return render(request, 'main_app/shelter_search.html', {'shelter_json': shelter_json})
