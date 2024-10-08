import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# API Key สำหรับ AI For Thai
apikey = "Your API Key"
sentiment_api_url = 'https://api.aiforthai.in.th/ssense'
# URL ของเว็บที่ต้องการ scrape
url = 'https://pantip.com/topic/42955493'
# ส่ง request ไปยัง URL
res = requests.get(url)
# ดึง HTML ของหน้าเว็บมา
html_page = res.content
# สร้าง BeautifulSoup object
soup = BeautifulSoup(html_page, 'html.parser')
# ดึงข้อความทั้งหมดจากหน้าเว็บ
txts = soup.find_all(string=True)
# กรองข้อความที่มีคำว่า 'iPhone 16' หรือ 'Xiaomi 15 Pro'
txts = [txt for txt in txts if 'iPhone 16' in txt or 'Xiaomi 14T Pro' in txt]
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
# สร้างลิสต์สำหรับเก็บข้อมูล
data = []
# วนลูปข้อความ และวิเคราะห์ sentiment
for txt in txts:
    sentiment_result = analyze_sentiment(txt)

    # ดึงคะแนนและประเภทของ sentiment
    score = sentiment_result['sentiment'].get('score', 'N/A')
    polarity = sentiment_result['sentiment'].get('polarity', 'N/A')

    # เพิ่มผลลัพธ์ลงในลิสต์
    data.append([txt, score, polarity])
# สร้าง DataFrame
df = pd.DataFrame(data, columns=['ข้อความ', 'คะแนน', 'ประเภท'])
# ฟังก์ชันสำหรับใส่สีให้กับคอลัมน์ประเภท sentiment
def highlight_sentiment(val):
    if val == 'positive':
        color = 'green'
    elif val == 'negative':
        color = 'red'
    elif val == 'neutral':
        color = 'gray'
    else:
        color = 'white'
    return f'background-color: {color}'
# ฟังก์ชันสำหรับใส่สีให้กับคอลัมน์คะแนน
def highlight_score(val):
    try:
        score = float(val)
        if score > 50:
            color = 'green'
        elif score == 50:
            color = 'yellow'
        else:
            color = 'red'
    except:
        color = 'white'
    return f'background-color: {color}'
# ใช้ฟังก์ชันสำหรับจัดรูปแบบตาราง (ใช้ map() แทน applymap())
styled_df = df.style.map(highlight_sentiment, subset=['ประเภท']) \
                     .map(highlight_score, subset=['คะแนน'])
# แสดงตารางพร้อมการจัดสี
styled_df