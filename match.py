import random
import itertools

# Ask user to input team names
def get_teams():
    while True:
        teams_input = input("Enter team names (min 2, max 20), separated by commas: ")
        teams = [team.strip() for team in teams_input.split(",") if team.strip()]
        if 2 <= len(teams) <= 20:
            return teams
        print("❗ Please enter between 2 and 20 valid team names.")

# Generate players and goalkeepers for each team
def generate_players(teams):
    players = {}
    goalkeepers = {}
    for team in teams:
        players[team] = [f"{team}_Player{i+1}" for i in range(5)]
        goalkeepers[team] = f"{team}_GK"
    return players, goalkeepers

# Initialize team points
def initialize_points_table(teams):
    return {team: 0 for team in teams}

# Create home & away fixtures
def generate_full_fixtures(teams):
    one_leg = list(itertools.combinations(teams, 2))
    two_legs = one_leg + [(b, a) for (a, b) in one_leg]
    random.shuffle(two_legs)

    matchdays = []
    while two_legs:
        today = []
        used = set()
        for match in two_legs[:]:
            home, away = match
            if home not in used and away not in used:
                today.append(match)
                used.update(match)
                two_legs.remove(match)
        matchdays.append(today)
    return matchdays

# Simulate a single matchday
def simulate_matchday(fixtures, points, players, gks, scorers, assisters, clean_sheets, day):
    print(f"\n=== 📅 Matchday {day} ===")
    for home, away in fixtures:
        home_goals = random.randint(0, 5)
        away_goals = random.randint(0, 5)

        # Update scorers and assisters
        for _ in range(home_goals):
            scorer = random.choice(players[home])
            scorers[scorer] = scorers.get(scorer, 0) + 1
            if random.random() < 0.8:
                assister = random.choice([p for p in players[home] if p != scorer])
                assisters[assister] = assisters.get(assister, 0) + 1

        for _ in range(away_goals):
            scorer = random.choice(players[away])
            scorers[scorer] = scorers.get(scorer, 0) + 1
            if random.random() < 0.8:
                assister = random.choice([p for p in players[away] if p != scorer])
                assisters[assister] = assisters.get(assister, 0) + 1

        # Clean sheets
        if away_goals == 0:
            clean_sheets[gks[home]] = clean_sheets.get(gks[home], 0) + 1
        if home_goals == 0:
            clean_sheets[gks[away]] = clean_sheets.get(gks[away], 0) + 1

        # Update points
        if home_goals > away_goals:
            points[home] += 3
            result = f"{home} wins"
        elif away_goals > home_goals:
            points[away] += 3
            result = f"{away} wins"
        else:
            points[home] += 1
            points[away] += 1
            result = "Draw"

        print(f"\n{home} 🏠 {home_goals} - {away_goals} 🛫 {away}")
        print(f"Result: {result}")

# Display top performers
def show_awards(scorers, assisters, clean_sheets):
    print("\n=== 🏆 Season Awards ===")

    print("\n🥇 Golden Boot (Top Scorers)")
    for player, goals in sorted(scorers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{player} - {goals} goals")

    print("\n🎯 Playmaker Award (Top Assists)")
    for player, assists in sorted(assisters.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{player} - {assists} assists")

    print("\n🧤 Golden Glove (Clean Sheets)")
    for gk, sheets in sorted(clean_sheets.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{gk} - {sheets} clean sheets")

# === MAIN PROGRAM ===
def main():
    teams = get_teams()
    players, gks = generate_players(teams)
    points = initialize_points_table(teams)

    scorers = {}
    assisters = {}
    clean_sheets = {}

    matchdays = generate_full_fixtures(teams)

    for i, fixtures in enumerate(matchdays, start=1):
        input(f"\nPress Enter to simulate Matchday {i}...")
        simulate_matchday(fixtures, points, players, gks, scorers, assisters, clean_sheets, i)

    print("\n=== 📊 Final League Table ===")
    for team, pts in sorted(points.items(), key=lambda x: x[1], reverse=True):
        print(f"{team}: {pts} pts")

    show_awards(scorers, assisters, clean_sheets)

# Run it
if __name__ == "__main__":
    main()

#for in