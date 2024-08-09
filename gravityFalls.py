import requests
import random
import string
import os
import mimetypes
from bs4 import BeautifulSoup
import base64
import concurrent.futures
import json

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
    
    code_folder = os.path.join('codes', code)
    os.makedirs(code_folder, exist_ok=True)
    
    for img in img_tags:
        if 'src' in img.attrs:
            src = img['src']
            if src.startswith('data:image'):
                # Handle base64 encoded image
                image_type, base64_data = src.split(',', 1)
                extension = image_type.split('/')[-1].split(';')[0]
                filename = f"image_{img_tags.index(img)}.{extension}"
                save_base64_image(code_folder, filename, base64_data)
                img['src'] = filename
            else:
                # Handle URL image
                img_url = src
                img_filename = os.path.basename(img_url)
                img_path = os.path.join(code_folder, img_filename)
                
                # Download and save the image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                    
                    # Update the img src to point to the local file
                    img['src'] = img_filename

    # Save the modified HTML
    html_filename = os.path.join(code_folder, f"{code}.html")
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return html_filename

def check_code(code):
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
        response = requests.post(url, data=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            code_folder = os.path.join('codes', code)
            os.makedirs(code_folder, exist_ok=True)
            
            if content_type.startswith('image/'):
                # It's an image
                extension = mimetypes.guess_extension(content_type) or ''
                filename = os.path.join(code_folder, f"{code}{extension}")
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return f"Code '{code}' exists. Image saved as {filename}"
            
            elif content_type.startswith('text/html'):
                # It's HTML content
                html_filename = save_html_with_images(code, response.text)
                return f"Code '{code}' exists. HTML content saved as {html_filename}"
            
            else:
                # It's plain text or other content
                text_filename = os.path.join(code_folder, f"{code}.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                return f"Code '{code}' exists. Response saved as {text_filename}"
        else:
            return f"Code '{code}' does not exist. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"An error occurred for code '{code}': {str(e)}"

def process_codes(codes):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check_code, codes))
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
    # Load previously checked codes
    checked_codes = load_checked_codes()

    # Example list of codes to check
    codes_to_check = [
    "Dipper", "Mabel", "Stan", "Ford", "Soos", "Wendy", "Bill", "Mystery", "Waddles",
    "Weirdmageddon", "Journal", "Pacifica", "Gideon", "Gnomes", "Summerween", "Bottomless",
    "TimeBaby", "Shmebulock", "Pines", "Cipher", "Multibear", "Manotaurs", "Pterodactyl",
    "Gobblewonker", "Robbie", "Susan", "Toby", "McGucket", "Blendin", "Rumble", "Candy",
    "Grenda", "Axolotl", "Tad", "Shacktron", "Dungeons", "Smile", "Northwest", "Mermando",
    "Chutzpar", "Quentin", "Woodpecker", "Trembley", "Dip", "Grunkle", "Corduroy", "Ramirez",
    "Gleeful", "Valentino", "Determined", "Blandin", "Strange", "Dip"
]
    
    results = process_codes(codes_to_check)
    
    for code, result in zip(codes_to_check, results):
        print(f"Result for code '{code}':")
        print(result)
        print("---")

    # Save the updated set of checked codes
    save_checked_codes()