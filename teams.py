import requests
import csv


def save_to_csv(data, filename, purpose):
    if not data:
        print("No data to save :(")
        return

    keys = data[0].keys() # get column names from the first dict
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"{purpose} data saved to {filename}. Length: {len(data)} rows!")


def get_all_teams():
    sport_ids = [1, 11, 12, 13, 14, 15, 16]  # MLB, AAA, AA, High-A, A, Rookie
    all_teams = []

    for sport_id in sport_ids:
        url = f'https://statsapi.mlb.com/api/v1/teams?sportId={sport_id}'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to get teams for sportId={sport_id}: {response.text}")

        data = response.json()
        teams = data.get('teams', [])
        for team in teams:
            league = team['league']['name']
            league_id = team['league']['id']
            name = team['name']
            id = team['id']
            all_teams.append({
                'team': name,
                'id': id,
                'league': league,
                'league_id': league_id,
                'abbreviation': team['abbreviation'],
                'debut year': team['firstYearOfPlay'],
                'division': team.get('division', {}).get('name', league),
                'division id': team.get('division', {}).get('id', league_id),
                'level': team['sport']['name'],
                'level id': team['sport']['id'],
                'organization': team.get('parentOrgName', name),
                'org ID': team.get('parentOrgName', id),
                'venue': team['venue']['name'],
                'venue id': team['venue']['id']

            })

    save_to_csv(all_teams, 'teams.csv', "Teams")
    return all_teams

get_all_teams()
