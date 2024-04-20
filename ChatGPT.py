from openai import OpenAI
import json

with open('secrets.json', 'r') as file:
  secrets = json.load(file)
api_key = secrets["CHAT_GPT_API"]

client = OpenAI(api_key=api_key)

question = input("오늘의 하루는 어땠어?")
artist=input("어떤 화가로 그려줄까?")



# 질문 작성하기
query = question+"라는 내용을 "+artist+"의 화풍으로 그려줘"
print(query)



response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "In your art diary entry today, please respond to the following prompt in a specific artist's style."},
    {"role": "system", "content": "Describe the scene you want to illustrate and mention the name of the artist whose style you want to emulate. Please provide a detailed description so we can generate an image using DALLE."},
    {"role": "user", "content":query}
  ]
)


# ChatGPT API 호출하기
answer = response.choices[0].message.content
print(answer)