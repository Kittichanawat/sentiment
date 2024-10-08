import requests
from bs4 import BeautifulSoup
import json

# API Key สำหรับ AI For Thai
apikey = "Your API key"
sentiment_api_url = 'https://api.aiforthai.in.th/ssense'

# URL ของเว็บที่ต้องการ scrape
url = 'https://droidsans.com/'

# ส่ง request ไปยัง URL
res = requests.get(url)

# ดึง HTML ของหน้าเว็บมา
html_page = res.content

# สร้าง BeautifulSoup object
soup = BeautifulSoup(html_page, 'html.parser')

# ดึงข้อความทั้งหมดจากหน้าเว็บ
txts = soup.find_all(text=True)

# กรองข้อความที่มีคำว่า 'iPhone 16' หรือ 'iPhone16'
txts = [txt for txt in txts if 'iPhone 16' in txt or 'iPhone16' in txt]

# ฟังก์ชันสำหรับส่งข้อความไปยัง Sentiment Analysis API
def analyze_sentiment(text):
    headers = {
        'Apikey': apikey,
    }
    payload = {
        'text': text
    }
    response = requests.post(sentiment_api_url, headers=headers, data=payload)
    return response.json()

# แสดงผลลัพธ์และวิเคราะห์ sentiment
for txt in txts:
    print(f"ข้อความ: {txt}")
    
    # เรียกใช้ Sentiment Analysis
    sentiment_result = analyze_sentiment(txt)
    
    # แสดงผลลัพธ์ของ sentiment
    print("ผลวิเคราะห์ Sentiment:", json.dumps(sentiment_result, ensure_ascii=False, indent=4))
