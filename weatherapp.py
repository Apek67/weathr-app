import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = "444efe08ce6e4b7493b114726242412"
# Function to get weather data
def get_weather_data(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to display weather data
def display_weather(data, city):
    current = data['current']
    location = data['location']
    temp_c = current['temp_c']
    condition = current['condition']['text']
    wind_kph = current['wind_kph']
    feels_like = current['feelslike_c']
    humidity = current['humidity']
    aqi = data['current']['air_quality']

    weather_info = (
        f"Weather in {city.title()} ({location['region']}, {location['country']})\n"
        f"Temperature      : {temp_c}°C (Feels like {feels_like}°C)\n"
        f"Condition        : {condition}\n"
        f"Wind Speed       : {wind_kph} km/h\n"
        f"Humidity         : {humidity}%\n"
    )
    if aqi:
        weather_info += f"Air Quality Index: {aqi.get('pm2_5', 'N/A')} PM2.5\n"
    
    return weather_info

# Function to save a city as a favorite
def save_favorite(city, favorites):
    if city not in favorites:
        favorites.append(city)
        return f"{city.title()} added to your favorites!"
    else:
        return f"{city.title()} is already in your favorites."

# Function to handle weather fetching and updating UI
def fetch_weather():
    city = city_entry.get()
    weather_data = get_weather_data(city)
    
    if weather_data:
        weather_info = display_weather(weather_data, city)
        weather_label.config(text=weather_info)
        
        save_option = messagebox.askyesno("Save City", "Do you want to save this city as a favorite?")
        if save_option:
            save_message = save_favorite(city, favorites)
            messagebox.showinfo("Favorite City", save_message)
    else:
        messagebox.showerror("Error", "City not found or an error occurred. Please try again.")

# Main UI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="skyblue")  # Set background color to blue

# List to hold favorite cities
favorites = []

# UI elements
city_label = tk.Label(root, text="Enter City Name:", bg="skyblue", font=("Arial", 14))
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), width=20)
city_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Get Weather", font=("Arial", 14), command=fetch_weather)
fetch_button.pack(pady=20)

weather_label = tk.Label(root, text="", bg="skyblue", font=("Arial", 12), justify="left")
weather_label.pack(pady=10)

# Run the application
root.mainloop()
