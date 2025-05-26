import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import os
import json

current_dir = os.getcwd()
final_dir = os.path.join(current_dir, 'data')

def file_path(path:str):
    if not os.path.exists(final_dir):
       os.makedirs(final_dir)
    db_path = os.path.join(final_dir, path)
    return db_path

respons_path = os.path.join(current_dir, 'png')
def respons_png(path:str):
    if not os.path.exists(respons_path):
       os.makedirs(respons_path)
    db_path = os.path.join(respons_path, path)
    return db_path

def generate_qrcode(username,size="600x600"):
    try:
       
        png=''
        file_size=file_path(f"private_{username}.json")
        with open(file_size, "r",encoding="utf-8") as file:
            data = json.load(file)

        avatar_url = data.get("avatar_url", "")
        if not avatar_url:
            try:
                print("Foydalanuvchida rasm yo'q.\n shuning uchun unga QR code yaratib beriladi.!")
                png += f"https://api.qrserver.com/v1/create-qr-code/?data={response}&size={size}"
                response = requests.get(png)
                if response.status_code == 200:
                    data=respons_png(f"{username}.png")
                    with open(data, "wb") as f:
                        f.write(response.content)
                    print(f"QR kod saqlandi: png/{username}.png")
                else:
                    print("Xatolik yuz berdi")
            except Exception as eror:
                print(f"Dasturda xato bo`ladi.!\n{eror}")
        else:
            try:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    png_path=respons_png(f"github_{username}_logo.jpg")
                    with open(png_path, "wb") as img_file:
                        img_file.write(response.content)
                    print("Rasm muvaffaqiyatli yuklab olindi.")
                else:
                    print(f"Rasmni yuklab bo'lmadi. Status: {response.status_code}")
            except Exception as eror:
                print(f"Dasturda xato bo`ladi.!\n{eror}")
    except(FileNotFoundError):
        print(f"Fayil topilmadi.!")

# search data
def search_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        user_data = response.json()
        return user_data
    except HTTPError as http_err:
        print(f"HTTP xatosi yuz berdi: {http_err} (Status kod: {response.status_code})")
    except Timeout:
        print("So‘rov vaqti tugadi (timeout). Iltimos, qayta urinib ko‘ring.")
    except RequestException as err:
        print(f"Biror xato yuz berdi: {err}")
    except Exception as e:
        print(f"Noma'lum xato: {e}")

# get beautuful
def user_info():
    username = input("GitHub foydalanuvchi nomini kiriting: ")
    if not username:
        print("Foydalanuvchi nomi kiritilmagan. Dastur tugatildi.")
        
    url = f"https://api.github.com/users/{username}" #otaboyevsardorbek1

    user_data = search_data(url)
    if user_data:
        kalit_sozlar = [
            "login", "avatar_url", "html_url", "followers_url",
            "repos_url", "name", "company",
            "blog", "location", "bio", "public_repos",
            "followers", "following", "created_at", "updated_at"
        ]
        result = {key: user_data.get(key, "Ma'lumot mavjud emas") for key in kalit_sozlar}
        data=file_path(f"private_{username}.json")
        with open(data, "w") as file:
            json.dump(result, file, indent=4)
        print(generate_qrcode(username))
        return (f"Foydalanuvchi ma'lumotlari saqlandi: data/{username}.json")
        
    else:
        return(f"Foydalanuvchi ma'lumotlari olinmadi: {username} nomli foydalanuvchi topilmadi.")
    
# # get beautuful
# def user_info():
#     username = input("GitHub foydalanuvchi nomini kiriting: ")
#     if not username:
#         print("Foydalanuvchi nomi kiritilmagan. Dastur tugatildi.")
#         return
#     url = f"https://api.github.com/users/{username}" #otaboyevsardorbek1

#     user_data = search_data(url)
#     if user_data:
#         kalit_sozlar = [
#             "login", "avatar_url", "html_url", "followers_url",
#             "repos_url", "name", "company",
#             "blog", "location", "bio", "public_repos",
#             "followers", "following", "created_at", "updated_at"
#         ]
#         result = {key: user_data.get(key, "Ma'lumot mavjud emas") for key in kalit_sozlar}
#         data=file_path(f"private_{username}.json")
#         with open(data, "w") as file:
#             json.dump(result, file, indent=4)
#         print(f"Foydalanuvchi ma'lumotlari saqlandi: data/{username}.json")
#         qrcode = generate_qrcode(username)
#         print(f"{qrcode}")
#     else:
#         return(f"Foydalanuvchi ma'lumotlari olinmadi: {username} nomli foydalanuvchi topilmadi.")