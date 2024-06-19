import requests
import telebot

API_KEY = '3'  # Replace with your actual API key
BOT_TOKEN = '7185441196:AAHEmkIXKAWdSH2lVmwd8qZNA0o2aVGEPrI'  # Replace with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def split_chunks(text, max_length):
    """ Splits the given text into chunks of maximum length `max_length`. """
    return (text[i:i+max_length] for i in range(0, len(text), max_length))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the SportsBot! You can use the following commands:\n" +
                     "/leagues\n" +
                     "/teams_in_league <league_name>\n" +
                     "/team <team_name>\n" +
                     "/players <team_name>\n" +
                     "/player <player_name>\n" +
                     "/sports\n" +
                     "/event <event_name>\n" +
                     "/livescores <sport_name>")

@bot.message_handler(commands=['teams_in_league'])
def get_teams_in_league(message):
    league_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if league_name:
        teams = list_teams_in_league(league_name)
        if teams:
            bot.send_message(message.chat.id, teams)
        else:
            bot.send_message(message.chat.id, "No teams found for the given league.")
    else:
        bot.send_message(message.chat.id, "Please provide a league name.")

def list_teams_in_league(league_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/search_all_teams.php?l={league_name}"
    data = fetch_data(url)
    if data and 'teams' in data:
        return "\n".join([team['strTeam'] for team in data['teams']])
    return None

@bot.message_handler(commands=['team'])
def get_team_details(message):
    team_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if team_name:
        team = search_team_by_name(team_name)
        if team:
            bot.send_message(message.chat.id, team)
        else:
            bot.send_message(message.chat.id, "No team found with the given name.")
    else:
        bot.send_message(message.chat.id, "Please provide a team name.")

def search_team_by_name(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchteams.php?t={team_name}"
    data = fetch_data(url)
    if data and 'teams' in data and len(data['teams']) > 0:
        team = data['teams'][0]
        return f"Team: {team['strTeam']}\nStadium: {team['strStadium']}\nFormed Year: {team['intFormedYear']}\nWebsite: {team['strWebsite']}\nDescription: {team['strDescriptionEN']}"
    return None

@bot.message_handler(commands=['players'])
def get_players_in_team(message):
    team_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if team_name:
        players = list_players_in_team(team_name)
        if players:
            for chunk in split_chunks("\n".join(players), 3000):
                bot.send_message(message.chat.id, chunk)
        else:
            bot.send_message(message.chat.id, f"No players found for team '{team_name}'.")
    else:
        bot.send_message(message.chat.id, "Please provide a team name.")

def list_players_in_team(team_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchplayers.php?t={team_name}"
    data = fetch_data(url)
    if data and 'player' in data:
        return [f"Player: {player['strPlayer']}\nPosition: {player['strPosition']}" for player in data['player']]
    return None

@bot.message_handler(commands=['player'])
def get_player_details(message):
    player_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if player_name:
        player = search_player_by_name(player_name)
        if player:
            # Split player details into chunks of 3000 characters
            for chunk in split_chunks(player, 3000):
                bot.send_message(message.chat.id, chunk)
        else:
            bot.send_message(message.chat.id, "No player found with the given name.")
    else:
        bot.send_message(message.chat.id, "Please provide a player name.")

def search_player_by_name(player_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchplayers.php?p={player_name}"
    data = fetch_data(url)
    if data and 'player' in data and len(data['player']) > 0:
        player = data['player'][0]
        return f"Player: {player['strPlayer']}\nTeam: {player['strTeam']}\nNationality: {player['strNationality']}\nPosition: {player['strPosition']}\nDescription: {player['strDescriptionEN']}"
    return None

@bot.message_handler(commands=['sports'])
def get_sports(message):
    sports = list_sports()
    if sports:
        bot.send_message(message.chat.id, sports)
    else:
        bot.send_message(message.chat.id, "No sports found.")

def list_sports():
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/all_sports.php"
    data = fetch_data(url)
    if data and 'sports' in data:
        return "\n".join([sport['strSport'] for sport in data['sports']])
    return None

@bot.message_handler(commands=['leagues'])
def get_leagues(message):
    leagues = list_leagues()
    if leagues:
        bot.send_message(message.chat.id, leagues)
    else:
        bot.send_message(message.chat.id, "No leagues found.")

def list_leagues():
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/all_leagues.php"
    data = fetch_data(url)
    if data and 'leagues' in data:
        return "\n".join([league['strLeague'] for league in data['leagues']])
    return None

@bot.message_handler(commands=['event'])
def get_event_details(message):
    event_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if event_name:
        event = search_event_by_name(event_name)
        if event:
            bot.send_message(message.chat.id, event)
        else:
            bot.send_message(message.chat.id, "No event found with the given name.")
    else:
        bot.send_message(message.chat.id, "Please provide an event name.")

def search_event_by_name(event_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/searchevents.php?e={event_name}"
    data = fetch_data(url)
    if data and 'event' in data and len(data['event']) > 0:
        event = data['event'][0]
        return f"Event: {event['strEvent']}\nDate: {event['dateEvent']}\nTime: {event['strTime']}\nLeague: {event['strLeague']}\nDescription: {event['strDescriptionEN']}"
    return None

@bot.message_handler(commands=['livescores'])
def get_live_scores(message):
    sport_name = message.text.split(' ', 1)[1].strip().lower() if len(message.text.split(' ', 1)) > 1 else ''
    if sport_name:
        scores = fetch_live_scores(sport_name)
        if scores:
            for chunk in split_chunks(scores, 3000):
                bot.send_message(message.chat.id, chunk)
        else:
            bot.send_message(message.chat.id, "No live scores found for the given sport.")
    else:
        bot.send_message(message.chat.id, "Please provide a sport name.")

def fetch_live_scores(sport_name):
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/latest{sport_name.lower()}.php"
    data = fetch_data(url)
    if data and 'events' in data:
        return "\n".join([f"{event['strEvent']} - {event['intHomeScore']}:{event['intAwayScore']}" for event in data['events']])
    return None

def main():
    bot.polling()

if __name__ == "__main__":
    main()
