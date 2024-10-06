import requests
 
url = "https://api.aiforthai.in.th/bully"
 
text = 'หมาน่ารัก'
 
data = {'text':text}
 
headers = {
    'Apikey': "OkbxIAeqs6zENpMTWDq9tU8vGp1JydYu",
    }
 
response = requests.post(url, data=data, headers=headers)
 
print(response.json())