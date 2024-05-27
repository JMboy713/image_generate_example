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
        "prompt": "Frozen-inspired animation style of a fulfilling day spent studying and socializing. The scene opens in a grand, ornate library with ice sculptures and shimmering frozen bookshelves, showing a character deeply engrossed in reading under a magical, glowing chandelier made of icicles. Next, the scene shifts to a bustling, snow-themed restaurant where a group of friends dressed in winter attire are gathered around a table, joyfully sharing a hearty meal under twinkling lights. The final scene takes place in a cozy, ice-crafted café, where the friends are wrapped in scarves, enjoying steaming cups of coffee amidst soft snowfall visible through frosty windows. Each setting is rendered with vibrant, icy colors and delicate snowflake details, reflecting the enchanting visual style of the Frozen movies, with a cinematic composition, trending on ArtStation.",
        "output_format": "webp",
    },
)
end_time=time.time()
print(end_time-start_time)

if response.status_code == 200:
    with open("./zibri.webp", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))