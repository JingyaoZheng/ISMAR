from openai import OpenAI
client = OpenAI(
    base_url="https://api.wlai.vip/v1",
    api_key='sk-PmkJ8W9PRiwWoH6VOEeebB1PCEjcYKXplSDVFnPT9x3JyKS3',
)
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
    {"role": "system", "content": """
     You are a notification classifier. You will be given a notification with the information of the sedner, the application source and the content of the notification. 
     You will have to classify the urgency levels of the notification into 2 categories: Urgent and Non-Urgent. 1 for Urgent and 0 for Non-Urgent.
     Please generate your answer either by 1 or 0."""},
    {"role": "user", "content": "The sender of the notification is 'Friend1', the application source is 'WhatsApp', and the content is 'Thanks Once I get the funds I will.'"},
    ]
)

print(response.choices[0].message.content)