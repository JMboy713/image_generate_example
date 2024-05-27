from openai import OpenAI
from dotenv import load_dotenv
import json
from IPython.display import Image
import urllib

load_dotenv()
with open('secrets.json', 'r') as file:
  secrets = json.load(file)
api_key = secrets["CHAT_GPT_API"]

client = OpenAI(api_key=api_key)

question = input("오늘의 하루는 어땠어?")
artist=input("어떤 화가로 그려줄까?")



# 질문 작성하기
query = question+"라는 내용을 "+artist+"의 화풍으로 그릴 수있게 프롬프트를 생성해줘"
print(query)



response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "In your art diary entry today, please respond to the following prompt in a specific artist's style but you have to not mention the specific artist name."},
    {"role": "system", "content": "Describe the scene you want to illustrate. Please provide a detailed description and mention the key characteristics of the style you want to emulate (e.g., impressionistic, vibrant colors, soft lighting) without naming specific artists."},
    {"role": "user", "content": query}
  ]
)


# ChatGPT API 호출하기
answer = response.choices[0].message.content
print(answer)

# DALL-E 3 모델을 사용하여 이미지를 생성합니다.
response = client.images.generate(
    model="dall-e-3",
    prompt=answer,
    size="1024x1024",
    quality="standard",
    n=1,
)

# 생성된 이미지의 URL을 저장합니다.
image_url = response.data[0].url
print(image_url)