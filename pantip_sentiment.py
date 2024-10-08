from playwright.sync_api import sync_playwright
import requests
import json

# API Key สำหรับ AI For Thai
apikey = "OkbxIAeqs6zENpMTWDq9tU8vGp1JydYu"
sentiment_api_url = 'https://api.aiforthai.in.th/ssense'

# ฟังก์ชันสำหรับส่งข้อความไปยัง Sentiment Analysis API
def analyze_sentiment(text):
    headers = {
        'Apikey': apikey,
    }
    payload = {
        'text': text
    }
    
    try:
        # ส่ง request ไปยัง API
        response = requests.post(sentiment_api_url, headers=headers, data=payload)

        # ตรวจสอบสถานะการตอบกลับ
        if response.status_code == 200:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                print("Error: Unable to decode JSON from API response")
                return None
        else:
            print(f"Error: Received status code {response.status_code} from API")
            return None
    except requests.RequestException as e:
        print(f"Error: Unable to connect to API - {e}")
        return None

# ฟังก์ชันสำหรับ scrape คอมเมนต์ด้วย Playwright (Firefox)
def scrape_pantip_comments_with_firefox(url):
    try:
        with sync_playwright() as p:
            # เปิด Firefox
            browser = p.firefox.launch(headless=False)  # เปลี่ยนเป็น True ถ้าต้องการรันแบบ headless
            page = browser.new_page()
            page.goto(url)
            
            # รอให้คอมเมนต์โหลด
            page.wait_for_selector('.pt-list-item__title')

            # ดึงคอมเมนต์
            comments = page.query_selector_all('.pt-list-item__title')

            # สร้างลิสต์สำหรับเก็บข้อมูลคอมเมนต์
            comment_texts = []
            for i, comment in enumerate(comments, 1):
                comment_text = comment.inner_text()
                comment_texts.append(comment_text)

            # ปิดเบราว์เซอร์
            browser.close()

            return comment_texts
    except Exception as e:
        print(f"Error scraping comments: {e}")
        return []

# URL ของหน้า Pantip ที่ต้องการ scrape
url = 'https://pantip.com/tag/iPhone_16'

# ดึงคอมเมนต์จากหน้าเว็บ Pantip
comments = scrape_pantip_comments_with_firefox(url)

# วนลูปคอมเมนต์ที่ดึงมา และวิเคราะห์ sentiment
for comment in comments:
    sentiment_result = analyze_sentiment(comment)

    if sentiment_result:
        # ดึงคะแนนและประเภทของ sentiment
        score = sentiment_result['sentiment'].get('score', 'N/A')
        polarity = sentiment_result['sentiment'].get('polarity', 'N/A')

        # แสดงผลลัพธ์ของการวิเคราะห์
        print(f"ข้อความ: {comment}")
        print(f"คะแนน: {score}, ประเภท: {polarity}")
    else:
        print(f"ไม่สามารถวิเคราะห์ sentiment สำหรับคอมเมนต์: {comment}")
    print("-" * 50)
