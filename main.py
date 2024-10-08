import requests
 
url = "https://api.aiforthai.in.th/bully"
 
text = 'ไอปัญญาอ่อน'
 
data = {'text':text}
 
headers = {
    'Apikey': "Your API Key",
    }
 
response = requests.post(url, data=data, headers=headers)
 
print(response.json())