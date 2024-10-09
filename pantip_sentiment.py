from playwright.async_api import async_playwright
import asyncio
import requests
import pandas as pd

# API Key สำหรับ AI For Thai
apikey = "Your API Key"
sentiment_api_url = 'https://api.aiforthai.in.th/ssense'

# ฟังก์ชันสำหรับส่งข้อความไปยัง Sentiment Analysis API
async def analyze_sentiment(text):
    headers = {
        'Apikey': apikey,
    }
    payload = {
        'text': text
    }

    try:
        # ส่ง request ไปยัง API แบบ synchronous แต่เนื่องจาก requests ไม่ใช่ async ใช้ await ใน asyncio
        response = await asyncio.to_thread(requests.post, sentiment_api_url, headers=headers, data=payload)

        # ตรวจสอบสถานะการตอบกลับ
        if response.status_code == 200:
            try:
                return response.json()
            except requests.JSONDecodeError:
               
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: Unable to connect to API - {e}")
        return None

# ฟังก์ชันสำหรับ scrape คอมเมนต์ด้วย Playwright (ในโหมด headless)
async def scrape_pantip_comments_headless(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # เปิดเบราว์เซอร์ในโหมด headless
        page = await browser.new_page()
        await page.goto(url)

        # รอให้คอมเมนต์โหลด
        await page.wait_for_selector('.pt-list-item__title')

        # ดึงคอมเมนต์
        comments = await page.query_selector_all('.pt-list-item__title')
        comment_texts = [await comment.inner_text() for comment in comments]

        # ปิดเบราว์เซอร์
        await browser.close()

        return comment_texts

# ฟังก์ชันหลักที่รันบน asyncio loop
async def main():
    url = 'https://pantip.com/tag/iPhone_16'
    comments = await scrape_pantip_comments_headless(url)

    # กรองเฉพาะคอมเมนต์ที่มีคำว่า "iPhone 16"
    filtered_comments = [comment for comment in comments if 'iPhone 16' in comment]

    if not filtered_comments:
        print("ไม่มีคอมเมนต์ที่เกี่ยวกับ 'iPhone 16'")
        return

    # สร้างลิสต์สำหรับเก็บข้อมูล
    data = []

    # วนลูปคอมเมนต์ที่ดึงมา และวิเคราะห์ sentiment
    for comment in filtered_comments:
        sentiment_result = await analyze_sentiment(comment)

        if sentiment_result:
            # ดึงคะแนนและประเภทของ sentiment
            score = sentiment_result.get('sentiment', {}).get('score', 'N/A')
            polarity = sentiment_result.get('sentiment', {}).get('polarity', 'N/A')

            # เก็บข้อมูลในลิสต์
            data.append([comment, score, polarity])
        else:
            data.append([comment, 'N/A', 'N/A'])

    # สร้าง DataFrame
    df = pd.DataFrame(data, columns=['ข้อความ', 'คะแนน', 'ประเภท'])

    # ฟังก์ชันสำหรับใส่สีให้กับประเภทของ sentiment
    def highlight_sentiment(val):
        color = 'white'
        if val == 'positive':
            color = 'green'
        elif val == 'negative':
            color = 'red'
        elif val == 'neutral':
            color = 'gray'
        return f'background-color: {color}'

    # ฟังก์ชันสำหรับใส่สีให้กับคอลัมน์คะแนน
    def highlight_score(val):
        try:
            score = float(val)
            if score > 50:
                return 'background-color: green'
            elif score == 50:
                return 'background-color: yellow'
            else:
                return 'background-color: red'
        except:
            return 'background-color: white'

    # ใช้ map() ในการใส่สีตามประเภท sentiment
    styled_df = df.style \
                   .map(highlight_sentiment, subset=['ประเภท']) \
                   .map(highlight_score, subset=['คะแนน'])

    # แสดง DataFrame พร้อมการจัดสี
    return styled_df

# เรียกใช้งานฟังก์ชันหลัก
await main()
