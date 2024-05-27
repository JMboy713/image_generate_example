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
kakao_api_key = secrets["KAKAO_API"]

REST_API_KEY = kakao_api_key

client = OpenAI(api_key=api_key)

# 검증되지 않은 SSL 컨텍스트 생성
context = ssl._create_unverified_context()

# 현재 작업 디렉토리 내에 저장할 디렉토리 설정
save_directory = os.path.join(os.getcwd(), "character3")
os.makedirs(save_directory, exist_ok=True)
def generate_image_description(artist):
    descriptions = {
        # 르네상스 시대
        "Leonardo da Vinci": "An older man with long, flowing white hair and a beard. He has a wise and contemplative expression, often depicted in Renaissance attire.",
        "Michelangelo": "A strong, muscular man with a serious expression. He is often depicted with short, curly hair and wearing simple, artist's clothing.",
        "Raffaello Sanzio": "A young man with delicate features, long brown hair, and a gentle expression. Often seen wearing Renaissance clothing.",
        "Sandro Botticelli": "A man with soft, wavy hair and a thoughtful expression. He is often depicted in elegant Renaissance attire.",
        "Tiziano Vecellio": "An older man with a thick white beard, expressive eyes, and a dignified expression. Often seen wearing rich, Renaissance clothing.",
        "Fra Angelico": "A gentle-looking man with short hair and a serene expression, often depicted in monk's robes.",
        "Jacopo Comin (or Robusti)": "A man with intense, piercing eyes and a strong jawline. Often depicted with short, dark hair and wearing simple, dark clothing.",
        "Masaccio": "A young man with short hair and a serious expression. Often depicted wearing simple, Renaissance artist's attire.",
        "Paolo Uccello": "A man with a sharp, inquisitive look and distinctive features. Often depicted with short hair and wearing Renaissance clothing.",

        # 근대시대
        "Pablo Picasso": "A man with dark, intense eyes and a strong jawline. Often seen with short hair and wearing simple, modern clothing. He has a serious, contemplative expression.",
        "Joan Miró": "A man with lively eyes and a friendly, whimsical expression. Often depicted with short hair and modern, casual clothing.",
        "Wassily Kandinsky": "A man with a thoughtful expression, round glasses, and short hair. Often depicted in early 20th-century clothing.",
        "Paul Cézanne": "An older man with a thick beard, deep-set eyes, and a contemplative expression. Often seen wearing simple, rustic clothing.",
        "Claude Monet": "An older man with a long white beard, round glasses, and a friendly, serene expression. Often depicted wearing a hat and a suit.",
        "Pierre-Auguste Renoir": "A man with a gentle, warm expression and a full beard. Often seen wearing late 19th-century clothing.",
        "Henri Rousseau": "A man with a mustache, a serious expression, and expressive eyes. Often depicted wearing simple, early 20th-century clothing.",
        "Paul Gauguin": "A man with strong features, a thick mustache, and a serious expression. Often depicted wearing rustic, late 19th-century clothing.",
        "Georges Seurat": "A young man with a neat mustache, intense eyes, and a focused expression. Often seen wearing late 19th-century clothing.",
        "Henri de Toulouse-Lautrec": "A man with a distinctive mustache, a top hat, and a playful expression. Often depicted in stylish, late 19th-century clothing.",

        # 현대
        "Jasper Johns": "A man with a thoughtful expression, short hair, and modern casual clothing. Often depicted with a serious, artistic demeanor.",
        "Andy Warhol": "A man with distinctive white hair, round glasses, and a playful expression. Often depicted wearing modern, stylish clothing.",
        "Gerhard Richter": "A man with short hair, a serious expression, and modern casual clothing. Often depicted with a contemplative look.",
        "Bruce Nauman": "A man with a thoughtful expression, short hair, and casual clothing. Often depicted with a serious, artistic demeanor.",
        "Roy Lichtenstein": "A man with a lively expression, short hair, and modern casual clothing. Often depicted with a playful, creative look.",
        "Robert Rauschenberg": "A man with a thoughtful expression, short hair, and casual clothing. Often depicted with a serious, artistic demeanor.",
        "Joseph Beuys": "A man with a distinctive hat, a serious expression, and casual clothing. Often depicted with a thoughtful, intense look.",
        "Ed Ruscha": "A man with short hair, a serious expression, and modern casual clothing. Often depicted with a contemplative look.",
        "Lucian Freud": "A man with a serious expression, short hair, and modern casual clothing. Often depicted with a thoughtful, intense look.",
        "Willem de Kooning": "A man with a lively expression, short hair, and casual clothing. Often depicted with a playful, creative look.",
        "Takashi Murakami": "A man with lively eyes, round glasses, and a playful expression. Often depicted wearing modern, colorful clothing.",
        "Jean-Michel Basquiat": "A man with distinctive dreadlocks, a serious expression, and casual clothing. Often depicted with an intense, artistic look.",
        "David Hockney": "A man with round glasses, a friendly expression, and colorful clothing. Often depicted with a playful, creative look.",
        "Jackson Pollock": "A man with a serious expression, short hair, and casual clothing. Often depicted with a thoughtful, intense look."
    }
    return descriptions.get(artist, "A notable artist with distinctive features.")



def make_prompt(artist, image_description):
    # 화가의 초상화를 기반으로 귀엽고 만화 같은 캐리커쳐를 생성하는 프롬프트 작성하기
    query = (
        f"Create a cute and cartoon-like caricature illustration of the artist {artist} based on the following description: {image_description}. "
        "Focus on exaggerating their most distinctive facial features, expressions, and clothing while retaining their recognizable traits. "
        "Ensure the caricature is whimsical and immediately recognizable as the artist."
    )

    print(query)

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are an expert in caricature design, known for your ability to create exaggerated and humorous depictions of famous individuals."},
        {"role": "system", "content": "Describe a cute and cartoon-like caricature inspired by the portrait of a specific artist. Include details about their appearance, clothing, and distinctive features as seen in their portrait. Focus on exaggerating their most distinctive facial features and expressions while retaining recognizable traits. Ensure the caricature is whimsical and immediately recognizable as the artist."},
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
    ancient_artist=["Polygnotus","Zeuxis","Parrhasius","Apelles","Philoxenus of Eretria","Micon","Exekias","Archelaos of Priene","Pausanias","Patra of Sicyon","Giotto di Bondone","Duccio di Buoninsegna",
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

    artist_list = [renaissance_artists,modern_artists, contemporary_artists]

    for period in artist_list:
        for artist in period:
            description = generate_image_description(artist)
            prompt = make_prompt(artist,description)
            # image_url=t2i(prompt,"")
            image_url=make_painting(prompt)

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


