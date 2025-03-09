import random

def get_teams():
    while True:
        teams_input = input("Enter the names of the teams (minimum 2, maximum 20), separated by commas: ")
        teams = [team.strip() for team in teams_input.split(",")]
        
        
        if 2 <= len(teams) <= 20:
            return teams
        else:
            print("Please enter between 2 and 20 teams.")


def initialize_points_table(teams):
    return {team: 0 for team in teams}

def Fixtures(teams):
    
    shuffled_teams = teams.copy()
    random.shuffle(shuffled_teams)
    
    fixtures = []
    while len(shuffled_teams) >= 2:
        
        team1 = random.choice(shuffled_teams)
        shuffled_teams.remove(team1)
        
        
        team2 = random.choice(shuffled_teams)
        shuffled_teams.remove(team2)
        
        
        fixtures.append((team1, team2))
    
    
    if len(shuffled_teams) == 1:
        print(f"\n{shuffled_teams[0]} gets a bye (no match this round).")
    
    return fixtures

def score(result, points_table):
    match_results = []
    print("\n=== Simulating Matches ===")
    for pair in result:
        team1, team2 = pair
        
        team1_goals = random.randint(0, 5)
        team2_goals = random.randint(0, 5)
        
        
        if team1_goals > team2_goals:
            winner = team1
            points_table[team1] += 3
        elif team2_goals > team1_goals:
            winner = team2
            points_table[team2] += 3
        else:
            winner = "Draw"
            points_table[team1] += 1
            points_table[team2] += 1
        
        
        match_results.append({
            "team1": team1,
            "team2": team2,
            "team1_goals": team1_goals,
            "team2_goals": team2_goals,
            "winner": winner
        })
        
        
        print(f"\n{team1} vs {team2}")
        print(f"Score: {team1_goals} - {team2_goals}")
        print(f"Winner: {winner}")
    
    return match_results


team = get_teams()


points_table = initialize_points_table(team)


result = Fixtures(team)
print("\n=== Fixtures ===")
for i, fixture in enumerate(result, 1):
    print(f"Match {i}: {fixture[0]} vs {fixture[1]}")


match_results = score(result, points_table)


print("\n=== Points Table ===")
sorted_points = sorted(points_table.items(), key=lambda x: x[1], reverse=True)
for team, points in sorted_points:
    print(f"{team}: {points} points")


 