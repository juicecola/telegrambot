Telegram Football Bot
This Telegram bot allows users to fetch information about football teams, players, and leagues using commands. The bot interacts with the TheSportsDB API to retrieve data.

Features
/teams <league_name>: Lists all teams in a specified league.
/players <team_name>: Lists all players in a specified team.
/player <player_name>: Provides details about a specified player.
Prerequisites
Python 3.x
A Telegram bot token from BotFather
An API key from TheSportsDB
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/telegram-football-bot.git
cd telegram-football-bot
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Create a .env file in the project directory and add your API key and bot token:

plaintext
Copy code
API_KEY=your_api_key_here
BOT_TOKEN=your_bot_token_here
Usage
Run the bot:

bash
Copy code
python3 main.py
Open Telegram and find your bot by its username. Start a chat with the bot and use the following commands:

/teams <league_name>: Replace <league_name> with the name of the league (e.g., English Premier League).

bash
Copy code
/teams English Premier League
/players <team_name>: Replace <team_name> with the name of the team (e.g., Arsenal).

bash
Copy code
/players Arsenal
/player <player_name>: Replace <player_name> with the name of the player (e.g., Lionel Messi).

bash
Copy code
/player Lionel Messi
Example
Command: /teams english premier league
Response:
diff
Copy code
Teams in the league:
- Arsenal
- Chelsea
- Manchester United
- Liverpool
- ... (other teams)
Command: /players arsenal
Response:
makefile
Copy code
Player: Bukayo Saka
Team: Arsenal
Nationality: England
Position: Midfielder
Description: (Description of Bukayo Saka)

Player: Emile Smith Rowe
Team: Arsenal
Nationality: England
Position: Midfielder
Description: (Description of Emile Smith Rowe)

... (other players)
Command: /player lionel messi
Response:
makefile
Copy code
Player: Lionel Messi
Team: Paris Saint-Germain
Nationality: Argentina
Position: Forward
Description: (Description of Lionel Messi)
Code Structure
main.py: The main script that contains the bot's functionality and handlers for different commands.
requirements.txt: List of required Python packages.
.env: File containing your API key and bot token (not included in the repository for security reasons).
Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
