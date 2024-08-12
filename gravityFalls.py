import requests
import random
import string
import os
import mimetypes
from bs4 import BeautifulSoup
import base64
import concurrent.futures
import json
import argparse

# Set to store checked codes
checked_codes = set()

def generate_random_boundary():
    return ''.join(random.choices(string.digits, k=30))

def save_base64_image(code_folder, filename, base64_data):
    img_data = base64.b64decode(base64_data)
    with open(os.path.join(code_folder, filename), 'wb') as f:
        f.write(img_data)

def save_html_with_images(code, content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('img')
    video_tags = soup.find_all('video')
    
    code_folder = os.path.join('codes', code)
    os.makedirs(code_folder, exist_ok=True)
    
    for img in img_tags:
        if 'src' in img.attrs:
            src = img['src']
            if src.startswith('data:image'):
                image_type, base64_data = src.split(',', 1)
                extension = image_type.split('/')[-1].split(';')[0]
                filename = f"image_{img_tags.index(img)}.{extension}"
                save_base64_image(code_folder, filename, base64_data)
                img['src'] = filename
            else:
                img_url = src
                img_filename = os.path.basename(img_url)
                img_path = os.path.join(code_folder, img_filename)
                
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                    
                    img['src'] = img_filename

    for video in video_tags:
        if 'src' in video.attrs:
            video_url = video['src']
            video_filename = os.path.basename(video_url)
            video_path = os.path.join(code_folder, video_filename)
            
            video_response = requests.get(video_url, stream=True)
            if video_response.status_code == 200:
                with open(video_path, 'wb') as video_file:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        video_file.write(chunk)
                
                video['src'] = video_filename

    html_filename = os.path.join(code_folder, f"{code}.html")
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return html_filename

def check_code(code, timeout):
    if code in checked_codes:
        return f"Code '{code}' has already been checked."
    
    checked_codes.add(code)
    
    url = "https://codes.thisisnotawebsitedotcom.com/"
    
    boundary_number = generate_random_boundary()
    boundary = f"-----------------------------{boundary_number}"
    
    payload = f'{boundary}\r\nContent-Disposition: form-data; name="code"\r\n\r\n{code}\r\n{boundary}--'
    
    headers = {
        'Host': 'codes.thisisnotawebsitedotcom.com',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://thisisnotawebsitedotcom.com/',
        'Origin': 'https://thisisnotawebsitedotcom.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': f'multipart/form-data; boundary={boundary[2:]}',
        'Priority': 'u=0',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            code_folder = os.path.join('codes', code)
            os.makedirs(code_folder, exist_ok=True)
            
            if content_type.startswith('image/'):
                extension = mimetypes.guess_extension(content_type) or ''
                filename = os.path.join(code_folder, f"{code}{extension}")
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return f"Code '{code}' exists. Image saved as {filename}"
            
            elif content_type.startswith('video/'):
                extension = mimetypes.guess_extension(content_type) or ''
                filename = os.path.join(code_folder, f"{code}{extension}")
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return f"Code '{code}' exists. Video saved as {filename}"
            
            elif content_type.startswith('text/html'):
                html_filename = save_html_with_images(code, response.text)
                return f"Code '{code}' exists. HTML content saved as {html_filename}"
            
            else:
                text_filename = os.path.join(code_folder, f"{code}.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f'{code} exists. Response saved as {text_filename}')
                return f"Code '{code}' exists. Response saved as {text_filename}"
        else:
            return f"Code '{code}' does not exist. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"An error occurred for code '{code}': {str(e)}"

def process_codes(codes, timeout):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda code: check_code(code, timeout), codes))
    return results

def load_checked_codes():
    try:
        with open('checked_codes.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_checked_codes():
    with open('checked_codes.json', 'w') as f:
        json.dump(list(checked_codes), f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Gravity Falls codes")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout for each request in seconds")
    parser.add_argument("--keywords", nargs='+', help="List of keywords to check")

    parser.add_argument("--file", help="File containing keywords to check (one per line)")
    parser.add_argument("--flip", action="store_true", help="Flip the keywords before checking")
    parser.add_argument("--thorough", action="store_true", help="Check all possible individual keywords, seperated by spaces, including the flipped ones")
    args = parser.parse_args()


    # Load previously checked codes
    checked_codes = load_checked_codes()
    print(args.flip)
    def breakOut(string):
        return string.split(' ')
    def flip(string):
        return string[::-1]
    def argumentFormatter(words):
        if args.flip:

            words = [flip(word) for word in words]
        if args.thorough:
            words += [flip(word) for word in words]
            words += [subword for word in words for subword in breakOut(word)]
            words+= [flip(subword) for subword in words]
        return words
    
    if args.file:
        with open(args.file, 'r') as f:
            codes_to_check=argumentFormatter([line.strip() for line in f])

    elif args.keywords:
        codes_to_check=argumentFormatter([code for code in args.keywords])

    else:
        codes_to_check = [
            "dipper", "mabel", "stan", "stanford", "soos", "wendy", "waddles", "grunkle",
            "ford", "stanley", "fiddleford", "mcgucket", "gideon", "pacifica", "robbie",
            # ... (rest of the default list)
            "fiddleford", "oldman", "toot-toot", "mcboomboompants", "waddlesworth", "octavia", "matpat"
        ]
    
    results = process_codes(codes_to_check, args.timeout)
    
    for code, result in zip(codes_to_check, results):
        print(f"Result for code '{code}':")
        print(result)
        print("---")
    # Save the updated set of checked codes
    save_checked_codes()