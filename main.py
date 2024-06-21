from bot import bot, API_TOKEN
import telebot
from telebot import types
import requests
from datetime import datetime, timedelta
import pytz

# Replace with your Telegram Bot token and Football Data API token
FOOTBALL_API_TOKEN = 'bb887f7ffe4f40f89d38bd2fc37cfd45'

bot = telebot.TeleBot(API_TOKEN)

EURO_2024_COMPETITION_ID = 'EC'  # Euro 2024 competition ID

KENYA_TZ = pytz.timezone('Africa/Nairobi')

# Function to get API data
def get_api_data(endpoint, params=None):
    url = f'https://api.football-data.org/v4/{endpoint}'
    headers = {'X-Auth-Token': FOOTBALL_API_TOKEN}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()

# Function to convert UTC time to local time
def convert_utc_to_local_time(utc_time_str, tz):
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    local_time = utc_time.astimezone(tz)
    return local_time.strftime('%Y-%m-%d %H:%M')

# Command to start the bot and display welcome message with inline keyboard
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Standings', callback_data='standings'),
               types.InlineKeyboardButton(text='Upcoming Matches', callback_data='upcoming'),
               types.InlineKeyboardButton(text='Top Scorers', callback_data='topscorers'),
               types.InlineKeyboardButton(text='Top Assists', callback_data='topassists'),
               types.InlineKeyboardButton(text='Disciplinary Records', callback_data='disciplinary'),
               types.InlineKeyboardButton(text='Historical Data', callback_data='history'))
    bot.send_message(message.chat.id, "Welcome to the Euro 2024 Bot! Select an option:", reply_markup=markup)

# Handle callback queries from inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'standings':
        send_standings(call.message)
    elif call.data == 'upcoming':
        send_upcoming_fixtures(call.message)
    elif call.data == 'topscorers':
        send_top_scorers(call.message)
    elif call.data == 'topassists':
        send_top_assists(call.message)
    elif call.data == 'disciplinary':
        send_disciplinary_records(call.message)
    elif call.data == 'history':
        send_historical_data(call.message)

# Command to fetch and send league standings
def send_standings(message):
    try:
        standings = get_competition_standings(EURO_2024_COMPETITION_ID)
        response = "Euro 2024 Standings:\n"
        for group in standings:
            response += f"\nGroup {group['group']}:\n"
            for team in group['table']:
                response += f"{team['position']}. {team['team']['name']} - {team['points']} points\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching standings: {str(e)}")

# Function to get league standings
def get_competition_standings(competition_id):
    data = get_api_data(f'competitions/{competition_id}/standings')
    standings = data['standings']
    return standings

# Command to fetch and send upcoming fixtures
def send_upcoming_fixtures(message):
    try:
        upcoming_matches = get_upcoming_fixtures()
        if not upcoming_matches:
            bot.send_message(message.chat.id, "No upcoming matches found.")
            return
        
        response = "Upcoming Euro 2024 Fixtures:\n"
        for match in upcoming_matches:
            match_time = convert_utc_to_local_time(match['utcDate'], KENYA_TZ)
            response += f"{match_time} - {match['homeTeam']['name']} vs {match['awayTeam']['name']}\n"
            response += "------------------------\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching upcoming fixtures: {str(e)}")

# Function to get upcoming fixtures
def get_upcoming_fixtures():
    today = datetime.now().strftime('%Y-%m-%d')
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    matches = get_matches_by_date(EURO_2024_COMPETITION_ID, today, future_date)
    scheduled_matches = [match for match in matches if match['status'] == 'SCHEDULED']
    return scheduled_matches

# Command to fetch and send top scorers
def send_top_scorers(message):
    try:
        top_scorers = get_top_scorers(EURO_2024_COMPETITION_ID)
        response = "Euro 2024 Top Scorers:\n"
        for scorer in top_scorers:
            response += f"{scorer['player']['name']} - {scorer['numberOfGoals']} goals\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching top scorers: {str(e)}")

# Function to get top scorers
def get_top_scorers(competition_id):
    params = {'limit': 10}  # Fetch top 10 scorers
    data = get_api_data(f'competitions/{competition_id}/scorers', params)
    scorers = data['scorers']
    return scorers

# Command to fetch and send top assists
def send_top_assists(message):
    try:
        top_assists = get_top_assists(EURO_2024_COMPETITION_ID)
        response = "Euro 2024 Top Assists:\n"
        for assist in top_assists:
            response += f"{assist['player']['name']} - {assist['numberOfAssists']} assists\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching top assists: {str(e)}")

# Function to get top assists
def get_top_assists(competition_id):
    data = get_api_data(f'competitions/{competition_id}/assists')
    assists = data['assists']
    return assists

# Command to fetch and send disciplinary records
def send_disciplinary_records(message):
    try:
        disciplinary_records = get_disciplinary_records(EURO_2024_COMPETITION_ID)
        response = "Euro 2024 Disciplinary Records:\n"
        for record in disciplinary_records:
            response += f"{record['player']['name']} - Yellow Cards: {record['yellowCards']}, Red Cards: {record['redCards']}\n"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching disciplinary records: {str(e)}")

# Function to get disciplinary records
def get_disciplinary_records(competition_id):
    data = get_api_data(f'competitions/{competition_id}/disciplinary')
    disciplinary_records = data['disciplinary']
    return disciplinary_records

# Command to fetch and send historical data
def send_historical_data(message):
    try:
        historical_data = get_historical_data(EURO_2024_COMPETITION_ID)
        response = "Euro 2024 Historical Data:\n"
        # Add logic to format and display historical data
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while fetching historical data: {str(e)}")

# Function to get historical data
def get_historical_data(competition_id):
    # Implement logic to fetch historical data from API
    # Example: Fetch past winners, notable matches, etc.
    return []

# Command to fetch and send matches by date
def get_matches_by_date(competition_id, date_from, date_to):
    params = {'dateFrom': date_from, 'dateTo': date_to}
    data = get_api_data(f'competitions/{competition_id}/matches', params)
    matches = data['matches']
    return matches

# Start polling
bot.polling()
