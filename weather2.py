import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO

# draw rounded corner images
def make_rounded_image(image_path, corner_radius):
    img = Image.open(image_path).convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    draw.rounded_rectangle(
        [(0, 0), (width, height)], 
        corner_radius, 
        fill=255
    )
    img.putalpha(mask)
    return img

# api fetch
def fetch_api(city):
    api_key = 'a1cb2b7a2320b8b7f2d566f5f11c4552'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror(f"{response.status_code}", "City Not Found")
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Check Network Connection")

# search weather 
def search_weather():
    city = city_entry.get()
    data = fetch_api(city)
    if data:
        weather_main = data['weather'][0]['main']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']
        
        weather_label.config(text=f"Weather: {weather_main}")
        temp_label.config(text=f"Temperature: {temp} °F")
        feels_like_label.config(text=f"Feels Like: {feels_like} °F")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed} mph")
        
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url)
        icon_data = icon_response.content
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo  # keep a reference to avoid garbage collection

root = tk.Tk()
root.title("Weather")
root.geometry("500x600")
root.resizable(0,0)
root.configure(bg='#ccccb3')
Bg = root.cget("bg")
icon = PhotoImage(file='icon.png')
root.iconphoto(False, icon)

heading = Label(root, text="WEATHER APP", font=("poppins,bold,20"), background=Bg)
heading.place(x=180, y=10)

image = 'logowaether.png'
corner_radius = 50
rounded_image = make_rounded_image(image, corner_radius)
tk_image = ImageTk.PhotoImage(rounded_image)

image_label = tk.Label(root, image=tk_image)
image_label.place(x=130, y=60)

city_entry = tk.Entry(root, background="#999", width=15, fg="#000", font=("TimesNewRoman, 20"))
city_entry.place(x=130, y=280)

search_button = Button(root, background="#999", width=5, fg="#000", text="search", command=search_weather)
search_button.place(x=370, y=280)

icon_label = Label(root, background=Bg)
icon_label.place(x=130, y=320)

weather_label = Label(root, text="", font=("poppins, 15"), background=Bg)
weather_label.place(x=130, y=400)

temp_label = Label(root, text="", font=("poppins, 15"), background=Bg)
temp_label.place(x=130, y=440)

feels_like_label = Label(root, text="", font=("poppins, 15"), background=Bg)
feels_like_label.place(x=130, y=480)

wind_speed_label = Label(root, text="", font=("poppins, 15"), background=Bg)
wind_speed_label.place(x=130, y=520)



root.mainloop()
