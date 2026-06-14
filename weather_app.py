import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# ==========================
# API KEY
# ==========================
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ==========================
# COLORS
# ==========================
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT = "#38bdf8"
TEXT = "#f8fafc"

# ==========================
# WEATHER ICONS
# ==========================
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️"
}


def get_weather():

    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return

    try:

        status_label.config(text="Loading...")
        root.update()

        # -------------------------
        # Current Weather
        # -------------------------

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            messagebox.showerror("Error", "City not found")
            return

        data = response.json()

        city_name = data["name"]

        temp = data["main"]["temp"]

        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        wind = data["wind"]["speed"]

        weather_main = data["weather"][0]["main"]

        description = data["weather"][0]["description"].title()

        icon = weather_icons.get(weather_main, "🌍")

        # -------------------------
        # Weather Tip
        # -------------------------

        if temp > 35:
            tip = "🥤 Stay hydrated and avoid long sun exposure."
        elif temp < 15:
            tip = "🧥 Carry a jacket today."
        else:
            tip = "😊 Pleasant weather today."

        # -------------------------
        # Forecast
        # -------------------------

        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        forecast_response = requests.get(
            forecast_url,
            timeout=10
        )

        forecast_data = forecast_response.json()

        forecast_text.delete("1.0", tk.END)

        for item in forecast_data["list"][::8]:

            date = item["dt_txt"].split()[0]

            f_temp = item["main"]["temp"]

            desc = item["weather"][0]["main"]

            f_icon = weather_icons.get(desc, "🌍")

            forecast_text.insert(
                tk.END,
                f"{f_icon} {date}   {f_temp:.1f}°C\n"
            )

        # -------------------------
        # Update UI
        # -------------------------

        city_label.config(text=f"📍 {city_name}")

        temp_label.config(
            text=f"{icon} {round(temp)}°C"
        )

        desc_label.config(
            text=description
        )

        details_label.config(
            text=
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind: {wind} m/s\n"
            f"🤗 Feels Like: {round(feels_like)}°C"
        )

        tip_label.config(text=tip)

        status_label.config(
            text="Weather data loaded successfully"
        )

    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            "Connection Error",
            "No Internet Connection"
        )

    except requests.exceptions.Timeout:
        messagebox.showerror(
            "Timeout",
            "Request Timed Out"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


# ==========================
# WINDOW
# ==========================

root = tk.Tk()

root.title("Weather Dashboard")

root.geometry("700x750")

root.configure(bg=BG_COLOR)

root.resizable(False, False)

# ==========================
# TITLE
# ==========================

title = tk.Label(
    root,
    text="🌤 Weather Dashboard",
    bg=BG_COLOR,
    fg=TEXT,
    font=("Segoe UI", 24, "bold")
)

title.pack(pady=20)

# ==========================
# SEARCH
# ==========================

city_entry = tk.Entry(
    root,
    font=("Segoe UI", 14),
    width=25,
    justify="center"
)

city_entry.pack(pady=10)

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)

search_btn = tk.Button(
    root,
    text="Get Weather",
    command=get_weather,
    bg=ACCENT,
    fg="black",
    font=("Segoe UI", 12, "bold"),
    width=15
)

search_btn.pack(pady=10)

# ==========================
# CARD
# ==========================

card = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=20,
    pady=20
)

card.pack(
    pady=20,
    padx=20,
    fill="x"
)

city_label = tk.Label(
    card,
    text="📍 Search a City",
    bg=CARD_COLOR,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
)

city_label.pack()

temp_label = tk.Label(
    card,
    text="--°C",
    bg=CARD_COLOR,
    fg=ACCENT,
    font=("Segoe UI", 42, "bold")
)

temp_label.pack()

desc_label = tk.Label(
    card,
    text="Weather Description",
    bg=CARD_COLOR,
    fg=TEXT,
    font=("Segoe UI", 14)
)

desc_label.pack()

details_label = tk.Label(
    card,
    text="",
    bg=CARD_COLOR,
    fg=TEXT,
    font=("Segoe UI", 12)
)

details_label.pack(pady=10)

# ==========================
# FORECAST
# ==========================

forecast_title = tk.Label(
    root,
    text="📅 5-Day Forecast",
    bg=BG_COLOR,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
)

forecast_title.pack()

forecast_text = tk.Text(
    root,
    height=8,
    width=45,
    bg=CARD_COLOR,
    fg="white",
    font=("Consolas", 12),
    bd=0
)

forecast_text.pack(pady=10)

# ==========================
# WEATHER TIP
# ==========================

tip_label = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="#facc15",
    font=("Segoe UI", 12, "bold")
)

tip_label.pack(pady=10)

# ==========================
# DATE/TIME
# ==========================

now = datetime.now()

current_date = now.strftime("%d %B %Y")
current_time = now.strftime("%I:%M %p")

date_label = tk.Label(
    root,
    text=f"📅 {current_date}    🕒 {current_time}",

    bg=BG_COLOR,
    fg="#94a3b8",
    font=("Segoe UI", 11)
)

date_label.pack(pady=10)

status_label = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="#22c55e",
    font=("Segoe UI", 10)
)

status_label.pack()

root.mainloop()