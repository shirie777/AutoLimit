import google.generativeai as genai
import os
import requests

# 1. 履歴の読み込み
HISTORY_FILE = 'history.txt'
history = []
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history = [line.strip() for line in f.readlines() if line.strip()]

# 2. プロンプト読み込みとGemini実行
with open('fxLimitsearch.txt', 'r', encoding='utf-8') as f:
    user_prompt = f.read()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Proモデルを指定
model = genai.GenerativeModel('gemini-1.5-pro')

# 検索ツールを有効化して実行
response = model.generate_content(
    user_prompt,
    tools=[{"google_search_retrieval": {}}]
)

# 3. 同一判定と通知
new_result = response.text.strip()
comparison_key = new_result.replace('\n', ' ') 

if comparison_key not in history:
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook_url and new_result:
        requests.post(webhook_url, json={"content": new_result})
    
    # 履歴を更新（最新3世代）
    history.insert(0, comparison_key)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(history[:3]))
