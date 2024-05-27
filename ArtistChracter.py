import os
import ssl

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

# 검증되지 않은 SSL 컨텍스트 생성
context = ssl._create_unverified_context()

# 현재 작업 디렉토리 내에 저장할 디렉토리 설정
save_directory = os.path.join(os.getcwd(), "character")
os.makedirs(save_directory, exist_ok=True)




def make_prompt(artist):
    # 화가의 초상화를 기반으로 캐릭터화하는 프롬프트 작성하기
    query = f"Create a character illustration based on the portrait of the artist {artist}. Describe their appearance, clothing, and any distinctive features they might have as seen in their portrait. Ensure the character has a stylized, cartoon-like appearance while retaining key identifiable features from the portrait."

    print(query)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are an expert in character design, known for your ability to create visually stunning and personality-rich characters inspired by famous artists."},
        {"role": "system", "content": "Describe a character inspired by the portrait of a specific artist. Include details about their appearance, clothing, and distinctive features as seen in their portrait. Make sure the character looks stylized and cartoon-like while retaining key identifiable features from the portrait. Also, mention the artistic style that reflects the artist's work."},
        {"role": "user", "content": query}
      ]
    )
    return response.choices[0].message.content



def make_painting(prompt):
    # DALL-E 3 모델을 사용하여 이미지를 생성합니다.
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # 생성된 이미지의 URL을 저장합니다.
    image_url = response.data[0].url
    return image_url

def main():
    artist_list=["Polygnotus","Zeuxis","Parrhasius","Apelles","Philoxenus of Eretria","Micon","Exekias","Archelaos of Priene","Pausanias","Patra of Sicyon","Giotto di Bondone","Duccio di Buoninsegna",
                 "Cimabue","Jan van Eyck","Lorenzo Monaco","Fra Angelico","Masolino da Panicale","Altichiero da Zevio","Hans Memling","Francesco Traini"]

    url_list =[]

    prompt = make_prompt("Vincent Van Gogh")
    image_url=make_painting(prompt)

    # 이미지 다운로드
    response = urllib.request.urlopen(image_url, context=context)
    image_path = os.path.join(save_directory, "반고흐.jpg")

    # 이미지 파일로 저장
    with open(image_path, 'wb') as f:
        f.write(response.read())

    print(f"Image saved as {image_path}")
    # for artist in artist_list:
    #     prompt = make_prompt(artist)
    #     image_url=make_painting(prompt)
    #
    #     # 이미지 다운로드
    #     response = urllib.request.urlopen(image_url, context=context)
    #     image_path = os.path.join(save_directory, f"{artist}.jpg")
    #
    #     # 이미지 파일로 저장
    #     with open(image_path, 'wb') as f:
    #         f.write(response.read())
    #
    #     print(f"Image saved as {image_path}")
        # print(image_url)
        # Image(url=image_url)
        # urllib.request.urlretrieve(image_url,artist+".jpg",context=context)

if __name__ == "__main__":
    main()


