import google.generativeai as genai
import os
import requests

# 1. 履歴の読み込み（最大3回分の実行結果を保持）
HISTORY_FILE = 'history.txt'
history = []
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        # 実行1回分を1行のデータとして読み込む
        history = [line.strip() for line in f.readlines() if line.strip()]

# 2. プロンプト読み込みとGemini実行
with open('fxLimitsearch.txt', 'r', encoding='utf-8') as f:
    user_prompt = f.read()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(user_prompt, tools=[{"google_search_retrieval": {}}])

# 改行を排除して比較用の1行データを作成
new_result = response.text.strip()
comparison_key = new_result.replace('\n', ' ') 

# 3. 過去3回分のいずれかと一致するか判定
if comparison_key in history:
    print("過去3回分のいずれかと内容が一致するため、通知をスキップしました。")
else:
    # Discord通知
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook_url and new_result:
        requests.post(webhook_url, json={"content": new_result})
    
    # 履歴を更新（最新の3回分を保持）
    history.insert(0, comparison_key)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(history[:3]))
