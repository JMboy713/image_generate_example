from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Image
import json
import urllib

load_dotenv()

with open('secrets.json', 'r') as file:
  secrets = json.load(file)
api_key = secrets["CHAT_GPT_API"]

client = OpenAI(api_key=api_key)


# DALL-E 3 모델을 사용하여 이미지를 생성합니다.
response = client.images.generate(
    model="dall-e-3",
    prompt="An ancient Greek-style painting depicting a modern-day scene of a person studying in a library, surrounded by books and scrolls. The person is seated at a wooden table with a cup of coffee, deeply engrossed in their work. The library is filled with bookshelves and classical architectural details, blending ancient Greek elements with a contemporary setting. Cinematic composition, trending on ArtStation.",
    size="1024x1024",
    quality="standard",
    n=1,
)

# 생성된 이미지의 URL을 저장합니다.
image_url = response.data[0].url
print(image_url)

Image(url=image_url)
urllib.request.urlretrieve(image_url, "picaso_character.jpg")
