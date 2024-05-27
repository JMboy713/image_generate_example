import os
import ssl

import requests
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
kakao_api_key = secrets["KAKAO_API"]

REST_API_KEY = kakao_api_key

save_directory = os.path.join(os.getcwd(), "painting_Karlo")
os.makedirs(save_directory, exist_ok=True)




def make_prompt(artist, question):
    # 질문 작성하기
    query = "Generate a prompt that can depict the content of the "+question+" in the style of the "+artist
    print(query)


    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "In your art diary entry today, please respond to the following prompt in a specific artist's style but you have to not mention the specific artist name."},
        {"role": "system", "content": "Describe the scene you want to illustrate. Please provide a detailed description and mention the key characteristics of the style you want to emulate (e.g., impressionistic, vibrant colors, soft lighting) without naming specific artists."},
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

def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1",
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "height": 1024,
            "width": 1024
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response.get("images")[0].get("image")

def main():
    diary_text="오늘 하루 풋살을 재미있게 차고, 친구들과 화목을 다졌어. 그리고 고기와 술을 같이 먹으면서 화합을 도모했지. 아주 좋은 하루였어!"
    ancient_artists=["Polygnotus","Zeuxis","Parrhasius","Apelles","Philoxenus of Eretria","Micon","Exekias","Archelaos of Priene","Pausanias","Patra of Sicyon","Giotto di Bondone","Duccio di Buoninsegna",
                 "Cimabue","Jan van Eyck","Lorenzo Monaco","Fra Angelico","Masolino da Panicale","Altichiero da Zevio","Hans Memling","Francesco Traini"]
    renaissance_artists = [
        "Leonardo da Vinci",  # 레오나르도 다빈치
        "Michelangelo",  # 미켈란젤로
        "Raffaello Sanzio",  # 라파엘로 산치
        "Sandro Botticelli",  # 산드로 보티첼리
        "Tiziano Vecellio",  # Titian (티치아노)
        "Fra Angelico",  # 프라 안젤리코
        "Jacopo Comin (or Robusti)",  # Tintoretto (틴토레토)
        "Masaccio",  # 마사초
        "Paolo Uccello"  # 파올로 우첼로
    ]

    # 근대시대
    modern_artists = [
        "Pablo Picasso",  # 파블로 피카소
        "Joan Miró",  # 호안 미로
        "Wassily Kandinsky",  # 바실리 칸딘스키
        "Paul Cézanne",  # 폴 세잔
        "Claude Monet",  # 클로드 모네
        "Pierre-Auguste Renoir",  # 피에르-오귀스트 르누아르
        "Henri Rousseau",  # 앙리 루소
        "Paul Gauguin",  # 폴 고갱
        "Georges Seurat",  # 조르주 쇠라
        "Henri de Toulouse-Lautrec"  # 앙리 드 툴루즈 로트렉
    ]

    # 현대
    contemporary_artists = [
        "Jasper Johns",  # 재스퍼 존스
        "Andy Warhol",  # 앤디 워홀
        "Gerhard Richter",  # 게르하르트 리히터
        "Bruce Nauman",  # 브루스 나우먼
        "Roy Lichtenstein",  # 로이 리히텐슈타인
        "Robert Rauschenberg",  # 로버트 라우셴버그
        "Joseph Beuys",  # 요셉 보이스
        "Ed Ruscha",  # 에드 루샤
        "Lucian Freud",  # 루시안 프로이트
        "Willem de Kooning",  # 윌렘 드 쿠닝
        "Takashi Murakami",  # 무라카미 다카시
        "Jean-Michel Basquiat",  # 장 미셸 바스키아
        "David Hockney",  # 데이비드 호크니
        "Jackson Pollock"  # 잭슨 폴록
    ]

    artist_list = [renaissance_artists, modern_artists, contemporary_artists]

    url_list =[]
    for period in artist_list:
        for artist in period:
            prompt = make_prompt(diary_text, artist)
            image_url=t2i(prompt,"")

            # 이미지 다운로드
            # response = urllib.request.urlopen(image_url, context=context)
            # image_path = f"{artist}.jpg"

            # 이미지 다운로드
            response = urllib.request.urlopen(image_url, context=context)
            image_path = os.path.join(save_directory, f"{artist}.jpg")

            # 이미지 파일로 저장
            with open(image_path, 'wb') as f:
                f.write(response.read())

            print(f"Image saved as {image_path}")
            # print(image_url)
            # Image(url=image_url)
            # urllib.request.urlretrieve(image_url,artist+".jpg",context=context)

if __name__ == "__main__":
    main()


