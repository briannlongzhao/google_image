from simple_image_download import simple_image_download
from tqdm import tqdm
import json
import shutil
import os


prompt_json = "/lab/briannlz/conceptnet/prompt_fixed_template_bg_200.json"
prompt_json = "VOC_background_captions.json"

skip_list = []
#skip_list = ["a real image of an empty large white building with a large white roof","a real image of an empty dirt hill","a colored photo of an empty rock by the ocean","a colored photo of an empty side of the road", "a colored photo of an empty dirt field"]

def parse_prompt_json(path):
    with open(path) as f:
        d = json.load(f)
    prompt_list = []
    for k,v in d["JPEGImages"].items():
        prompt_list += v
    return sorted(list(set(prompt_list)))

def parse_prompt_json(path):
    with open(path) as f:
        d = json.load(f)
    prompt_list = []
    for k,v in d["background"].items():
        prompt_list += v
    prompt_list = [x.split(', ')[0] for x in prompt_list]
    return sorted(list(set(prompt_list)))

def check_prompt(path, target_num):
    total = 0
    for img in os.listdir(path):
        if os.path.getsize(os.path.join(path,img)) < 1000:
            os.remove(os.path.join(path,img))

prompt_list = parse_prompt_json(prompt_json)
print(prompt_list)
downloader = simple_image_download.simple_image_download()
#downloader.directory = dst_dir
img_per_prompt = int(9057/len(prompt_list))
total = 0
for prompt in tqdm(prompt_list):
    if prompt in skip_list:
        continue
    prompt_dir = os.path.join("simple_images", prompt)
    if os.path.exists(prompt_dir):
        print("skip", prompt_dir)
        continue
    print("downloading", prompt)
    downloader.download(prompt, limit=200+(img_per_prompt))

# post processing
for prompt in prompt_list:
    prompt_dir = os.path.join("simple_images", prompt)
    for image in tqdm(os.listdir(prompt_dir)):
        image_path = os.path.join(prompt_dir, image)
        image_size = os.path.getsize(image_path)
        if image_size <= 5000:
            os.remove(image_path)
        else:
            total += 1

print("total image", total)
