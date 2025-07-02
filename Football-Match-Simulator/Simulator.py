import random
import itertools

# Get teams from user
def get_teams():
    while True:
        teams_input = input("Enter team names (min 2, max 20), separated by commas: ")
        teams = [team.strip() for team in teams_input.split(",")]
        if 2 <= len(teams) <= 20:
            return teams
        print("Please enter between 2 and 20 teams.")

# Generate players and goalkeepers
def generate_players(teams):
    players = {}
    goalkeepers = {}
    for team in teams:
        players[team] = [f"{team}_Player{i+1}" for i in range(5)]
        goalkeepers[team] = f"{team}_GK"
    return players, goalkeepers

# Initialize empty points table
def initialize_points_table(teams):
    return {team: 0 for team in teams}

# Generate full season fixtures (Home and Away)
def generate_full_fixtures(teams):
    one_leg = list(itertools.combinations(teams, 2))  # each team plays every other once
    two_legs = one_leg + [(b, a) for (a, b) in one_leg]  # home and away
    random.shuffle(two_legs)

    # Organize into matchdays
    matchdays = []
    while two_legs:
        today = []
        used_teams = set()
        for match in two_legs[:]:
            t1, t2 = match
            if t1 not in used_teams and t2 not in used_teams:
                today.append(match)
                used_teams.update(match)
                two_legs.remove(match)
        matchdays.append(today)
    return matchdays

# Simulate a matchday
def score(matchday_fixtures, points_table, players, goalkeepers, top_scorers, top_assisters, clean_sheets, matchday_num):
    print(f"\n=== Matchday {matchday_num} ===")
    for home, away in matchday_fixtures:
        home_goals = random.randint(0, 5)
        away_goals = random.randint(0, 5)

        # Track goal scorers and assisters
        for _ in range(home_goals):
            scorer = random.choice(players[home])
            top_scorers[scorer] = top_scorers.get(scorer, 0) + 1
            if random.random() < 0.8:
                assister = random.choice([p for p in players[home] if p != scorer])
                top_assisters[assister] = top_assisters.get(assister, 0) + 1

        for _ in range(away_goals):
            scorer = random.choice(players[away])
            top_scorers[scorer] = top_scorers.get(scorer, 0) + 1
            if random.random() < 0.8:
                assister = random.choice([p for p in players[away] if p != scorer])
                top_assisters[assister] = top_assisters.get(assister, 0) + 1

        # Clean sheets
        if away_goals == 0:
            clean_sheets[goalkeepers[home]] = clean_sheets.get(goalkeepers[home], 0) + 1
        if home_goals == 0:
            clean_sheets[goalkeepers[away]] = clean_sheets.get(goalkeepers[away], 0) + 1

        # Points
        if home_goals > away_goals:
            points_table[home] += 3
            winner = home
        elif away_goals > home_goals:
            points_table[away] += 3
            winner = away
        else:
            points_table[home] += 1
            points_table[away] += 1
            winner = "Draw"

        print(f"\n{home} (Home) vs {away} (Away)")
        print(f"Score: {home_goals} - {away_goals}")
        print(f"Winner: {winner}")

# Awards and leaderboard
def show_awards(top_scorers, top_assisters, clean_sheets):
    print("\n=== 🥇 Golden Boot (Top Scorers) ===")
    for player, goals in sorted(top_scorers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{player}: {goals} goals")

    print("\n=== 🎯 Playmaker Award (Top Assists) ===")
    for player, assists in sorted(top_assisters.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{player}: {assists} assists")

    print("\n=== 🧤 Golden Glove (Clean Sheets) ===")
    for gk, sheets in sorted(clean_sheets.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{gk}: {sheets} clean sheets")

# === MAIN ===
teams = get_teams()
players, goalkeepers = generate_players(teams)
points_table = initialize_points_table(teams)

top_scorers = {}
top_assisters = {}
clean_sheets = {}

matchdays = generate_full_fixtures(teams)
total_matchdays = len(matchdays)

for i, fixtures in enumerate(matchdays, 1):
    input(f"\nPress Enter to simulate Matchday {i}...")
    score(fixtures, points_table, players, goalkeepers, top_scorers, top_assisters, clean_sheets, i)

# Final table
print("\n=== 🧮 Final League Table ===")
for team, pts in sorted(points_table.items(), key=lambda x: x[1], reverse=True):
    print(f"{team}: {pts} points")

# Awards
show_awards(top_scorers, top_assisters, clean_sheets)
#yes ts a 2
print("hi mera dil")