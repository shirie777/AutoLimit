import google.generativeai as genai
import os
import requests

# 1. ファイルからプロンプトを読み込む
with open('fxLimitsearch.txt', 'r', encoding='utf-8') as f:
    user_prompt = f.read()

# 2. Gemini APIの設定
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-3-flash')

# 3. ネット検索ツールを有効化して実行
# プロンプトに従い、Geminiが自ら検索して分析
response = model.generate_content(
    user_prompt,
    tools=[{"google_search_retrieval": {}}]
)

# 4. 結果をDiscordへ通知
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
if response.text and webhook_url:
    requests.post(webhook_url, json={"content": response.text})