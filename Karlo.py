import requests
import json

with open('secrets.json', 'r') as file:
  secrets = json.load(file)
api_key = secrets["KAKAO_API"]

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = api_key

# 이미지 생성하기 요청
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
    return response

# 프롬프트에 사용할 제시어
prompt = "A vibrant and colorful depiction of a student's day, utilizing Luis Mendo's pop art style. The morning begins with a study session in the library, portrayed with bold, block colors and repetitive patterns to emphasize the routine. The narrative progresses to a lunch scene with friends, represented as a series of bright, almost neon-colored images of food and laughing faces, echoing Warhol's fascination with consumer culture. The day concludes with a coffee scene, stylized with high-contrast colors and a commercial graphic design feel, mimicking the iconic visual language of Warhol's works."
negative_prompt = ""

# 이미지 생성하기 REST API 호출
response = t2i(prompt, negative_prompt)

# 응답의 첫 번째 이미지 생성 결과 출력하기

result=response.get("images")[0].get("image")
print(result)