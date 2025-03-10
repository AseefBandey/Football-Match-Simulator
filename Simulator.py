import random

# Get input from user for teams
def get_teams():
    while True:
        teams_input = input("Enter the names of the teams (minimum 2, maximum 20), separated by commas: ")
        teams = [team.strip() for team in teams_input.split(",")]
        
        if 2 <= len(teams) <= 20:
            return teams
        else:
            print("Please enter between 2 and 20 teams.")

# Initialize Points Table with Goal Difference (GD)
def initialize_points_table(teams):
    return {team: {"points": 0, "GD": 0} for team in teams}  # Each team has Points & Goal Difference

# Generate Round-Robin Fixtures (Home & Away) with Balanced Scheduling
def generate_fixtures(teams):
    fixtures = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            fixtures.append((teams[i], teams[j]))  # Match 1 (Home)
            fixtures.append((teams[j], teams[i]))  # Match 2 (Away)

    random.shuffle(fixtures)  # Initial shuffle

    # Ensure teams don’t play back-to-back matches
    final_fixtures = []
    used_teams = set()

    while fixtures:
        for match in fixtures[:]:  # Iterate over a copy of the list
            team1, team2 = match
            if team1 not in used_teams and team2 not in used_teams:
                final_fixtures.append(match)
                used_teams = {team1, team2}  # Mark these teams as used in this round
                fixtures.remove(match)
                break  # Move to the next round

        if not fixtures:  # If all fixtures are scheduled, break
            break

        used_teams.clear()  # Reset the used teams for the next round

    return final_fixtures

# Simulate Matches and Update Points & GD
def simulate_matches(fixtures, points_table):
    match_results = []
    print("\n=== Simulating Matches ===")
    
    for team1, team2 in fixtures:
        team1_goals = random.randint(0, 5)
        team2_goals = random.randint(0, 5)
        
        # Determine Winner & Update Points
        if team1_goals > team2_goals:
            winner = team1
            points_table[team1]["points"] += 3
        elif team2_goals > team1_goals:
            winner = team2
            points_table[team2]["points"] += 3
        else:
            winner = "Draw"
            points_table[team1]["points"] += 1
            points_table[team2]["points"] += 1

        # Update Goal Difference (GD)
        points_table[team1]["GD"] += (team1_goals - team2_goals)
        points_table[team2]["GD"] += (team2_goals - team1_goals)

        # Store Match Result
        match_results.append({
            "team1": team1,
            "team2": team2,
            "team1_goals": team1_goals,
            "team2_goals": team2_goals,
            "winner": winner
        })

        # Print Match Summary
        print(f"\n{team1} vs {team2}")
        print(f"Score: {team1_goals} - {team2_goals}")
        print(f"Winner: {winner}")

    return match_results

# Display Final Standings
def display_points_table(points_table):
    print("\n=== Final Points Table ===")
    sorted_table = sorted(points_table.items(), key=lambda x: (x[1]["points"], x[1]["GD"]), reverse=True)
    for team, data in sorted_table:
        print(f"{team}: {data['points']} points, GD: {data['GD']}")

# Main Execution
teams = get_teams()
points_table = initialize_points_table(teams)
fixtures = generate_fixtures(teams)

print("\n=== Fixtures ===")
for i, (team1, team2) in enumerate(fixtures, 1):
    print(f"Match {i}: {team1} vs {team2}")

match_results = simulate_matches(fixtures, points_table)
display_points_table(points_table)
