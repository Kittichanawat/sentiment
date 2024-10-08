import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL ของเว็บที่ต้องการ scrape
url = 'https://pantip.com/topic/42955493'

# ส่ง request ไปยัง URL
res = requests.get(url)

# ดึง HTML ของหน้าเว็บมา
html_page = res.content

# สร้าง BeautifulSoup object
soup = BeautifulSoup(html_page, 'html.parser')

# ดึงความคิดเห็นจากหน้าเว็บ (ความคิดเห็นที่อยู่ใน div ที่มี class "display-post-story")
comments = soup.find_all('div', class_='display-post-story')

# ดึงเฉพาะข้อความในความคิดเห็น
txts = [comment.get_text(strip=True) for comment in comments]

# กรองข้อความที่มีคำว่า 'iPhone 16' หรือ 'Xiaomi 14T Pro'
txts = [txt for txt in txts if 'iPhone 16' in txt or 'Xiaomi 14T Pro' in txt]

# สร้างลิสต์สำหรับเก็บข้อมูล
data = []

# วนลูปข้อความที่ถูกดึงมา
for txt in txts:
    # เพิ่มข้อมูลลงในลิสต์
    data.append([txt])

# สร้าง DataFrame
df = pd.DataFrame(data, columns=['ความคิดเห็น'])

# แสดง DataFrame
df
