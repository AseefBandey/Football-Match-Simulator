"""
Command-line interface for the football simulator.
"""
import sys
import os
from typing import List, Dict, Optional
import random
from PyInquirer import prompt, Separator
from colorama import init, Fore, Style
from tqdm import tqdm
import time

from .models import League, Team, Player, Match, MatchStats
from .persistence import save_league, load_league, list_saves, get_latest_save

# Initialize colorama
init()

def create_team(name: str) -> Team:
    """Create a team with players."""
    positions = ["GK"] + ["DEF"] * 4 + ["MID"] * 4 + ["FWD"] * 2
    players = []
    
    # Create goalkeeper
    gk = Player(f"{name}_GK1", name, "GK")
    players.append(gk)
    
    # Create outfield players
    for i, pos in enumerate(positions[1:], 1):
        player = Player(f"{name}_P{i}", name, pos)
        players.append(player)
    
    return Team(name, players)

def get_teams() -> List[Team]:
    """Get teams from user input."""
    questions = [
        {
            'type': 'input',
            'name': 'teams',
            'message': 'Enter team names (comma-separated, 2-20 teams):',
            'validate': lambda answer: 2 <= len(answer.split(',')) <= 20 or 'Please enter between 2 and 20 teams'
        }
    ]
    
    answers = prompt(questions)
    if not answers:  # User pressed Ctrl+C
        sys.exit(0)
        
    team_names = [name.strip() for name in answers['teams'].split(',')]
    return [create_team(name) for name in team_names]

def display_match_stats(match: Match):
    """Display detailed match statistics."""
    print(f"\n{Fore.CYAN}Match Statistics{Style.RESET_ALL}")
    print(f"{'':20} {Fore.GREEN}HOME{Style.RESET_ALL}  {Fore.YELLOW}AWAY{Style.RESET_ALL}")
    print("-" * 40)
    
    # Possession
    print(f"{'Possession':20} {match.home_stats.possession:4.1f}%  {match.away_stats.possession:4.1f}%")
    
    # Shots
    print(f"{'Shots':20} {match.home_stats.shots:4}  {match.away_stats.shots:4}")
    print(f"{'Shots on Target':20} {match.home_stats.shots_on_target:4}  {match.away_stats.shots_on_target:4}")
    
    # Corners
    print(f"{'Corners':20} {match.home_stats.corners:4}  {match.away_stats.corners:4}")
    
    # Passes
    print(f"{'Passes':20} {match.home_stats.passes:4}  {match.away_stats.passes:4}")
    print(f"{'Pass Accuracy':20} {match.home_stats.pass_accuracy:4.1f}%  {match.away_stats.pass_accuracy:4.1f}%")
    
    # Fouls and Cards
    print(f"{'Fouls':20} {match.home_stats.fouls:4}  {match.away_stats.fouls:4}")
    print(f"{'Yellow Cards':20} {match.home_stats.yellow_cards:4}  {match.away_stats.yellow_cards:4}")
    print(f"{'Red Cards':20} {match.home_stats.red_cards:4}  {match.away_stats.red_cards:4}")

def display_match_result(match: Match):
    """Display a match result with colors."""
    print(f"\n{Fore.CYAN}Match Result:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{match.home_team.name}{Style.RESET_ALL} {match.home_goals} - {match.away_goals} {Fore.YELLOW}{match.away_team.name}{Style.RESET_ALL}")
    
    if match.scorers:
        print(f"\n{Fore.CYAN}Scorers:{Style.RESET_ALL}")
        for scorer in match.scorers:
            print(f"⚽ {scorer.name}")
            
    if match.assisters:
        print(f"\n{Fore.CYAN}Assists:{Style.RESET_ALL}")
        for assister in match.assisters:
            print(f"👟 {assister.name}")
            
    # Display detailed match statistics
    display_match_stats(match)

def display_league_table(league: League):
    """Display the league table with colors."""
    print(f"\n{Fore.CYAN}League Table{Style.RESET_ALL}")
    print(f"{'Pos':4} {'Team':<20} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>3} {'GA':>3} {'GD':>4} {'Pts':>4}")
    print("-" * 55)
    
    for pos, team in enumerate(league.get_league_table(), 1):
        color = Fore.GREEN if pos <= 4 else Fore.RED if pos >= len(league.teams) - 2 else Style.RESET_ALL
        print(f"{color}{pos:2}. {team.name:<20} {team.matches_played:3} {team.wins:3} {team.draws:3} "
              f"{team.losses:3} {team.goals_for:3} {team.goals_against:3} {team.goal_difference:4} "
              f"{team.points:4}{Style.RESET_ALL}")

def display_stats(league: League):
    """Display various statistics."""
    print(f"\n{Fore.CYAN}Top Scorers{Style.RESET_ALL}")
    for pos, player in enumerate(league.get_top_scorers(), 1):
        print(f"{pos}. {player.name:<20} {player.goals} goals")
        
    print(f"\n{Fore.CYAN}Top Assisters{Style.RESET_ALL}")
    for pos, player in enumerate(league.get_top_assisters(), 1):
        print(f"{pos}. {player.name:<20} {player.assists} assists")
        
    print(f"\n{Fore.CYAN}Clean Sheets{Style.RESET_ALL}")
    for pos, player in enumerate(league.get_top_clean_sheets(), 1):
        print(f"{pos}. {player.name:<20} {player.clean_sheets} clean sheets")
        
    print(f"\n{Fore.CYAN}Disciplinary Table{Style.RESET_ALL}")
    for pos, player in enumerate(league.get_disciplinary_table(), 1):
        print(f"{pos}. {player.name:<20} {player.yellow_cards}🟨 {player.red_cards}🟥")
        
    print(f"\n{Fore.CYAN}Pass Masters (min. 100 passes){Style.RESET_ALL}")
    for pos, player in enumerate(league.get_pass_masters(), 1):
        print(f"{pos}. {player.name:<20} {player.pass_accuracy:.1f}% ({player.passes_completed}/{player.passes})")

def display_team_stats(team: Team):
    """Display detailed statistics for a team."""
    print(f"\n{Fore.CYAN}Team Statistics: {team.name}{Style.RESET_ALL}")
    print(f"{'Average Possession':25} {team.average_possession:5.1f}%")
    print(f"{'Shot Accuracy':25} {team.shot_accuracy:5.1f}%")
    print(f"{'Pass Accuracy':25} {team.pass_accuracy:5.1f}%")
    print(f"{'Clean Sheets':25} {team.clean_sheets}")
    print(f"{'Yellow Cards':25} {team.yellow_cards}")
    print(f"{'Red Cards':25} {team.red_cards}")
    print(f"{'Total Fouls':25} {team.fouls}")

def load_or_new_league() -> League:
    """Prompt user to load a save or start a new league."""
    saves = list_saves()
    
    if not saves:
        print("No saved leagues found. Starting a new league...")
        return League("Simulation League", get_teams())
        
    questions = [
        {
            'type': 'list',
            'name': 'action',
            'message': 'Would you like to load a saved league or start a new one?',
            'choices': ['Start New League', 'Load Latest Save', 'Choose Save File']
        }
    ]
    
    answers = prompt(questions)
    if not answers:  # User pressed Ctrl+C
        sys.exit(0)
        
    action = answers['action']
    
    if action == 'Start New League':
        return League("Simulation League", get_teams())
    elif action == 'Load Latest Save':
        latest = get_latest_save()
        if not latest:
            print("No saves found. Starting a new league...")
            return League("Simulation League", get_teams())
        return load_league(latest)
    else:  # Choose Save File
        save_choices = [
            {
                'type': 'list',
                'name': 'save_file',
                'message': 'Choose a save file:',
                'choices': [os.path.basename(f) for f in saves]
            }
        ]
        save_answer = prompt(save_choices)
        if not save_answer:  # User pressed Ctrl+C
            sys.exit(0)
            
        chosen_save = next(s for s in saves if os.path.basename(s) == save_answer['save_file'])
        return load_league(chosen_save)

def simulate_season():
    """Main function to simulate a football season."""
    print(f"{Fore.CYAN}Welcome to Football Match Simulator!{Style.RESET_ALL}")
    
    # Load or create new league
    league = load_or_new_league()
    
    if not league.matches:  # New league
        league.generate_fixtures()
    
    total_matchdays = len(league.matches) // (len(league.teams) // 2)
    
    while True:
        if league.current_matchday >= total_matchdays:
            print(f"\n{Fore.GREEN}Season completed!{Style.RESET_ALL}")
            break
            
        questions = [
            {
                'type': 'list',
                'name': 'action',
                'message': 'What would you like to do?',
                'choices': [
                    'Simulate next matchday',
                    'View league table',
                    'View statistics',
                    'View team details',
                    'Save game',
                    'Exit'
                ]
            }
        ]
        
        answers = prompt(questions)
        if not answers:  # User pressed Ctrl+C
            sys.exit(0)
            
        action = answers['action']
        
        if action == 'Simulate next matchday':
            print(f"\n{Fore.CYAN}Simulating Matchday {league.current_matchday + 1}{Style.RESET_ALL}")
            matches = league.simulate_matchday()
            
            # Show progress bar
            for _ in tqdm(range(10), desc="Simulating matches", ncols=70):
                time.sleep(0.1)
                
            for match in matches:
                display_match_result(match)
                
        elif action == 'View league table':
            display_league_table(league)
            
        elif action == 'View statistics':
            display_stats(league)
            
        elif action == 'View team details':
            team_choices = [
                {
                    'type': 'list',
                    'name': 'team',
                    'message': 'Select a team:',
                    'choices': [team.name for team in league.teams]
                }
            ]
            team_answer = prompt(team_choices)
            if team_answer:
                selected_team = next(team for team in league.teams if team.name == team_answer['team'])
                display_team_stats(selected_team)
                
        elif action == 'Save game':
            save_path = save_league(league)
            print(f"\n{Fore.GREEN}Game saved to: {save_path}{Style.RESET_ALL}")
            
        else:  # Exit
            # Ask to save before exit if there are unsaved changes
            if league.current_matchday > 0:
                save_question = [
                    {
                        'type': 'confirm',
                        'name': 'save',
                        'message': 'Would you like to save before exiting?',
                        'default': True
                    }
                ]
                save_answer = prompt(save_question)
                if save_answer and save_answer['save']:
                    save_path = save_league(league)
                    print(f"\n{Fore.GREEN}Game saved to: {save_path}{Style.RESET_ALL}")
            sys.exit(0)
    
    # Show final standings and stats
    print("\nFinal Results:")
    display_league_table(league)
    display_stats(league)
    
    # Ask to save completed season
    save_question = [
        {
            'type': 'confirm',
            'name': 'save',
            'message': 'Would you like to save this completed season?',
            'default': True
        }
    ]
    save_answer = prompt(save_question)
    if save_answer and save_answer['save']:
        save_path = save_league(league)
        print(f"\n{Fore.GREEN}Season saved to: {save_path}{Style.RESET_ALL}")

def main():
    """Entry point for the CLI."""
    try:
        simulate_season()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main() 