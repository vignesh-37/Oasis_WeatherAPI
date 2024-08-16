from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import messagebox as mb
from tkinter import PhotoImage
from PIL import Image,ImageTk,ImageDraw 
import requests


# draw rounded corner images
def make_rounded_image(image_path, corner_radius):
    # Open the image
    img = Image.open(image_path).convert("RGBA")
    
    # Create a mask to round the edges
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw rounded rectangle on the mask
    width, height = img.size
    draw.rounded_rectangle(
        [(0, 0), (width, height)], 
        corner_radius, 
        fill=255
    )
    
    # Apply the rounded mask to the image
    img.putalpha(mask)
    
    return img
#api featch
def featch_api(city):
    api_key='a1cb2b7a2320b8b7f2d566f5f11c4552'
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror(f"{response.status_code}","city Not Found")
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error","Check Network Connection")
        
#search weather 
def search_weather():
    city = city_entry.get()
    data = featch_api(city)
    print(data)
    print(data['weather'][0]['main'])
    print(data['main']['temp'],  data['main']['feels_like'])
    print(data['wind']['speed'])
    
root = tk.Tk()
root.title("Weather")
root.geometry("500x800")
root.resizable(0,0)
root.configure(bg='#fff')
Bg = root.cget("bg")
icon = PhotoImage(file='icon.png')
root.iconphoto(False, icon)

heading=Label(root,text="WEATHER APP",font=("poppins,20,bold"),background=Bg)
heading.place(x=180,y=10)

image ='logowaether.png'
cornorRadious=50
rounded_image=make_rounded_image(image,cornorRadious)
tk_image=ImageTk.PhotoImage(rounded_image)

image_label=tk.Label(root,image=tk_image)
image_label.place(x=130,y=60)

city_entry=tk.Entry(root,background="#999",width=20,fg="#000",font=("poppins,20"))
city_entry.place(x=130,y=280)


search_button=Button(root,background="#999",width=5,fg="#000",text="search",command=search_weather)
search_button.place(x=350,y=280)



root.mainloop()