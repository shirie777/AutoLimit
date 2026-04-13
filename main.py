import google.generativeai as genai
import os

# API設定（実績のある標準的な書き方）
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# 【重要】検索ツール（tools）を一切使わずに実行
try:
    response = model.generate_content("Hello. Just say 'Success' if you can read this.")
    print(response.text)
except Exception as e:
    print(f"Error logic: {e}")
