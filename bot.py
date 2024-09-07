import telebot
import sqlite3

bot_token = '6929626685:AAFnr3s8hhujqNWKepFBs_chekaFzJ7h-rE'
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