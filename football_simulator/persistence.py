"""
Module for saving and loading season data.
"""
import json
import os
from dataclasses import asdict
from typing import Dict, Any, Optional
from datetime import datetime

from .models import League, Team, Player, Match, MatchStats


def _serialize_match_stats(stats: MatchStats) -> Dict[str, Any]:
    """Convert MatchStats to a dictionary."""
    return asdict(stats)


def _deserialize_match_stats(data: Dict[str, Any]) -> MatchStats:
    """Create MatchStats from a dictionary."""
    return MatchStats(**data)


def _serialize_player(player: Player) -> Dict[str, Any]:
    """Convert Player to a dictionary."""
    return asdict(player)


def _deserialize_player(data: Dict[str, Any]) -> Player:
    """Create Player from a dictionary."""
    return Player(**data)


def _serialize_team(team: Team) -> Dict[str, Any]:
    """Convert Team to a dictionary."""
    data = asdict(team)
    data['players'] = [_serialize_player(p) for p in team.players]
    return data


def _deserialize_team(data: Dict[str, Any]) -> Team:
    """Create Team from a dictionary."""
    players_data = data.pop('players')
    team = Team(**data)
    team.players = [_deserialize_player(p) for p in players_data]
    return team


def _serialize_match(match: Match) -> Dict[str, Any]:
    """Convert Match to a dictionary."""
    return {
        'home_team': _serialize_team(match.home_team),
        'away_team': _serialize_team(match.away_team),
        'home_goals': match.home_goals,
        'away_goals': match.away_goals,
        'scorers': [_serialize_player(p) for p in match.scorers],
        'assisters': [_serialize_player(p) for p in match.assisters],
        'home_stats': _serialize_match_stats(match.home_stats),
        'away_stats': _serialize_match_stats(match.away_stats),
        'completed': match.completed
    }


def _deserialize_match(data: Dict[str, Any]) -> Match:
    """Create Match from a dictionary."""
    return Match(
        home_team=_deserialize_team(data['home_team']),
        away_team=_deserialize_team(data['away_team']),
        home_goals=data['home_goals'],
        away_goals=data['away_goals'],
        scorers=[_deserialize_player(p) for p in data['scorers']],
        assisters=[_deserialize_player(p) for p in data['assisters']],
        home_stats=_deserialize_match_stats(data['home_stats']),
        away_stats=_deserialize_match_stats(data['away_stats']),
        completed=data['completed']
    )


def _serialize_league(league: League) -> Dict[str, Any]:
    """Convert League to a dictionary."""
    return {
        'name': league.name,
        'teams': [_serialize_team(t) for t in league.teams],
        'matches': [_serialize_match(m) for m in league.matches],
        'current_matchday': league.current_matchday
    }


def _deserialize_league(data: Dict[str, Any]) -> League:
    """Create League from a dictionary."""
    teams = [_deserialize_team(t) for t in data['teams']]
    matches = [_deserialize_match(m) for m in data['matches']]
    league = League(data['name'], teams)
    league.matches = matches
    league.current_matchday = data['current_matchday']
    return league


def save_league(league: League, save_dir: str = "saves") -> str:
    """
    Save the league state to a JSON file.
    
    Args:
        league: The league to save
        save_dir: Directory to save the file in
        
    Returns:
        The path to the saved file
    """
    # Create saves directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"league_save_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)
    
    # Serialize and save
    data = _serialize_league(league)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    return filepath


def load_league(filepath: str) -> League:
    """
    Load a league from a save file.
    
    Args:
        filepath: Path to the save file
        
    Returns:
        The loaded League object
        
    Raises:
        FileNotFoundError: If the save file doesn't exist
        json.JSONDecodeError: If the save file is invalid
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return _deserialize_league(data)


def list_saves(save_dir: str = "saves") -> list[str]:
    """
    List all available save files.
    
    Args:
        save_dir: Directory containing save files
        
    Returns:
        List of save file paths
    """
    if not os.path.exists(save_dir):
        return []
        
    return [
        os.path.join(save_dir, f)
        for f in os.listdir(save_dir)
        if f.startswith("league_save_") and f.endswith(".json")
    ]


def get_latest_save(save_dir: str = "saves") -> Optional[str]:
    """
    Get the path to the most recent save file.
    
    Args:
        save_dir: Directory containing save files
        
    Returns:
        Path to the most recent save file, or None if no saves exist
    """
    saves = list_saves(save_dir)
    return max(saves, key=os.path.getctime) if saves else None 