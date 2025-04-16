import pandas as pd
import requests
import time
import csv


# define load_teams function
def load_teams():
    return pd.read_csv("teams.csv")

# get list of teams
teams_df = load_teams()

# define get_roster function
def get_roster(team_id):
    url = f'https://statsapi.mlb.com/api/v1/teams/{team_id}/roster?rosterType=all'
    response = requests.get(url)
    return response.json().get('roster', [])

def collect_rosters():
    teams = teams_df
    all_players = []

    for _, team in teams.iterrows():
        print(f"Getting roster for {team['team']}...")
        roster = get_roster(team['id'])
        if not roster:
            continue

        for player in roster:
            person = player['person']
            player_id = person['id']
            name = person['fullName']
            position = player.get('position', {}).get('abbreviation')
            number = player.get('jerseyNumber')

            player_data = {
                'team': team['team'],
                'name': name,
                'number': number,
                'position': position,
                'level': team['level'],
                'organization': team['organization'],
                'mlb_id': player_id,
                'team_id': team['id'],
            }

            all_players.append(player_data)

        time.sleep(0.1)  # be polite to the API

    return all_players


def save_to_csv(data, filename='rosters.csv'):
    fieldnames = ['team', 'name', 'number', 'position', 'level', 'organization', 'mlb_id', 'team_id']
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    all_rosters = collect_rosters()
    save_to_csv(all_rosters)
    print("Saved to rosters.csv ✅")
