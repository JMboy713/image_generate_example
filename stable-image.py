import requests
import time
import json
with open('secrets.json', 'r') as file:
  secrets = json.load(file)
api_key = secrets["STABLE_DIFFUSION_API"]



start_time=time.time()
response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": api_key,
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "Impressionist style depiction by Claude Monet of a vibrant, atmospheric series of scenes: a softly blurred morning in a library with dappled light filtering through windows, highlighting the person studying among rows of hazy books; friends sharing a meal outdoors, the table set under shimmering trees with light and shadow playing across their faces and the food; and a cozy coffee session, with the cafe's ambient warmth captured in loose, expressive brushstrokes. The artwork conveys a sense of fulfillment and contentment through Monet’s characteristic focus on light and color, trending on Artstation.",
        "output_format": "webp",
    },
)
end_time=time.time()
print(end_time-start_time)

if response.status_code == 200:
    with open("./davinch.webp", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))