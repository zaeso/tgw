import telebot
import sqlite3
import matplotlib.pyplot as plt
import io
from PIL import Image
bot_token = ''
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['weather'])
def handle_weather_request(message):
    args = message.text.split()
    requested_date = args[1] if len(args) > 1 else None
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        if requested_date:
            cursor.execute("SELECT * FROM WeatherData WHERE Date = ?", (requested_date,))
        else:
            cursor.execute("SELECT * FROM WeatherData ORDER BY Date DESC LIMIT 1")
        weather_data = cursor.fetchone()

    if weather_data:
        date, max_temp, humidity, wind_speed, cloud_cover, precipitation, dew_point = weather_data

        
        plt.figure(figsize=(8, 6))
        plt.bar(['Max Temp', 'Humidity', 'Wind Speed', 'Cloud Cover', 'Precipitation', 'Dew Point'], 
                [max_temp, humidity, wind_speed, cloud_cover, precipitation, dew_point])
        plt.title(f"Weather data for {date}")
        plt.ylabel("Values")
        plt.xticks(rotation=45)

       
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = Image.open(buf)

        
        bot.send_photo(message.chat.id, image)

        response = f"Weather data for {date}:\n\n"
        response += f"Maximum Temperature: {max_temp}°C\n"
        response += f"Humidity: {humidity}%\n"
        response += f"Wind Speed: {wind_speed} m/s\n"
        response += f"Cloud Cover: {cloud_cover}\n"
        response += f"Precipitation: {precipitation} mm\n"
        response += f"Dew Point: {dew_point}°C"
    else:
        response = "No weather data found for the requested date."

    bot.reply_to(message, response)

bot.polling()
