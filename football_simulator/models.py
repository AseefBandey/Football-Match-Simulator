"""
Core models for the football simulator.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random
import itertools


@dataclass
class Player:
    name: str
    team: str
    position: str
    rating: float = field(default_factory=lambda: random.uniform(60, 90))
    goals: int = 0
    assists: int = 0
    clean_sheets: int = 0
    form: float = field(default_factory=lambda: random.uniform(0.8, 1.2))
    yellow_cards: int = 0
    red_cards: int = 0
    shots: int = 0
    shots_on_target: int = 0
    passes: int = 0
    passes_completed: int = 0
    tackles: int = 0
    tackles_won: int = 0
    minutes_played: int = 0

    def __str__(self) -> str:
        return f"{self.name} ({self.team})"

    @property
    def pass_accuracy(self) -> float:
        """Calculate pass accuracy percentage."""
        if not self.passes:
            return 0.0
        return (self.passes_completed / self.passes) * 100

    @property
    def shot_accuracy(self) -> float:
        """Calculate shot accuracy percentage."""
        if not self.shots:
            return 0.0
        return (self.shots_on_target / self.shots) * 100

    @property
    def tackle_success(self) -> float:
        """Calculate tackle success percentage."""
        if not self.tackles:
            return 0.0
        return (self.tackles_won / self.tackles) * 100


@dataclass
class MatchStats:
    """Statistics for a single team in a match."""
    possession: float = 50.0
    shots: int = 0
    shots_on_target: int = 0
    corners: int = 0
    fouls: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    offsides: int = 0
    passes: int = 0
    passes_completed: int = 0
    tackles: int = 0
    tackles_won: int = 0

    @property
    def pass_accuracy(self) -> float:
        """Calculate pass accuracy percentage."""
        if not self.passes:
            return 0.0
        return (self.passes_completed / self.passes) * 100


@dataclass
class Team:
    name: str
    players: List[Player] = field(default_factory=list)
    points: int = 0
    goals_for: int = 0
    goals_against: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    clean_sheets: int = 0
    total_shots: int = 0
    shots_on_target: int = 0
    total_passes: int = 0
    passes_completed: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    fouls: int = 0
    possession_total: float = 0.0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def matches_played(self) -> int:
        return self.wins + self.draws + self.losses

    @property
    def team_rating(self) -> float:
        if not self.players:
            return 70.0
        return sum(p.rating * p.form for p in self.players) / len(self.players)

    @property
    def average_possession(self) -> float:
        """Calculate average possession percentage."""
        if not self.matches_played:
            return 0.0
        return self.possession_total / self.matches_played

    @property
    def shot_accuracy(self) -> float:
        """Calculate shot accuracy percentage."""
        if not self.total_shots:
            return 0.0
        return (self.shots_on_target / self.total_shots) * 100

    @property
    def pass_accuracy(self) -> float:
        """Calculate pass accuracy percentage."""
        if not self.total_passes:
            return 0.0
        return (self.passes_completed / self.total_passes) * 100

    def __str__(self) -> str:
        return f"{self.name} ({self.points} pts)"


@dataclass
class Match:
    home_team: Team
    away_team: Team
    home_goals: int = 0
    away_goals: int = 0
    scorers: List[Player] = field(default_factory=list)
    assisters: List[Player] = field(default_factory=list)
    home_stats: MatchStats = field(default_factory=MatchStats)
    away_stats: MatchStats = field(default_factory=MatchStats)
    completed: bool = False

    def simulate(self) -> None:
        """Simulate the match result based on team ratings and form."""
        if self.completed:
            return

        # Calculate expected goals based on team ratings
        home_xg = self.home_team.team_rating / 20
        away_xg = self.away_team.team_rating / 25  # Away teams score less

        # Simulate possession
        base_possession = 50
        rating_diff = self.home_team.team_rating - self.away_team.team_rating
        possession_modifier = rating_diff / 2
        self.home_stats.possession = min(70, max(30, base_possession + possession_modifier))
        self.away_stats.possession = 100 - self.home_stats.possession

        # Update team possession totals
        self.home_team.possession_total += self.home_stats.possession
        self.away_team.possession_total += self.away_stats.possession

        # Simulate shots and shots on target
        self.home_stats.shots = max(0, int(random.gauss(12 * (self.home_stats.possession/50), 3)))
        self.away_stats.shots = max(0, int(random.gauss(10 * (self.away_stats.possession/50), 3)))
        
        self.home_stats.shots_on_target = max(0, int(self.home_stats.shots * random.uniform(0.3, 0.6)))
        self.away_stats.shots_on_target = max(0, int(self.away_stats.shots * random.uniform(0.25, 0.55)))

        # Update team shot totals
        self.home_team.total_shots += self.home_stats.shots
        self.home_team.shots_on_target += self.home_stats.shots_on_target
        self.away_team.total_shots += self.away_stats.shots
        self.away_team.shots_on_target += self.away_stats.shots_on_target

        # Simulate goals based on shots on target
        self.home_goals = max(0, int(random.gauss(self.home_stats.shots_on_target * 0.3, 1)))
        self.away_goals = max(0, int(random.gauss(self.away_stats.shots_on_target * 0.25, 1)))

        # Simulate other match events
        self._simulate_match_events()

        # Update team stats
        self.home_team.goals_for += self.home_goals
        self.home_team.goals_against += self.away_goals
        self.away_team.goals_for += self.away_goals
        self.away_team.goals_against += self.home_goals

        if self.home_goals > self.away_goals:
            self.home_team.points += 3
            self.home_team.wins += 1
            self.away_team.losses += 1
        elif self.away_goals > self.home_goals:
            self.away_team.points += 3
            self.away_team.wins += 1
            self.home_team.losses += 1
        else:
            self.home_team.points += 1
            self.away_team.points += 1
            self.home_team.draws += 1
            self.away_team.draws += 1

        # Simulate goal scorers and assists
        self._simulate_goals()
        self.completed = True

    def _simulate_match_events(self) -> None:
        """Simulate various match events like cards, corners, etc."""
        # Simulate corners
        self.home_stats.corners = max(0, int(random.gauss(6, 2)))
        self.away_stats.corners = max(0, int(random.gauss(5, 2)))

        # Simulate fouls and cards
        self.home_stats.fouls = max(0, int(random.gauss(10, 3)))
        self.away_stats.fouls = max(0, int(random.gauss(11, 3)))  # Away teams slightly more fouls

        self.home_stats.yellow_cards = min(5, max(0, int(self.home_stats.fouls * 0.3)))
        self.away_stats.yellow_cards = min(5, max(0, int(self.away_stats.fouls * 0.35)))

        self.home_stats.red_cards = 1 if random.random() < 0.05 else 0  # 5% chance
        self.away_stats.red_cards = 1 if random.random() < 0.06 else 0  # 6% chance for away team

        # Update team stats
        self.home_team.yellow_cards += self.home_stats.yellow_cards
        self.home_team.red_cards += self.home_stats.red_cards
        self.home_team.fouls += self.home_stats.fouls
        self.away_team.yellow_cards += self.away_stats.yellow_cards
        self.away_team.red_cards += self.away_stats.red_cards
        self.away_team.fouls += self.away_stats.fouls

        # Simulate passes
        self.home_stats.passes = int(self.home_stats.possession * 5)  # Rough estimate
        self.away_stats.passes = int(self.away_stats.possession * 5)

        self.home_stats.passes_completed = int(self.home_stats.passes * random.uniform(0.75, 0.9))
        self.away_stats.passes_completed = int(self.away_stats.passes * random.uniform(0.7, 0.85))

        # Update team pass totals
        self.home_team.total_passes += self.home_stats.passes
        self.home_team.passes_completed += self.home_stats.passes_completed
        self.away_team.total_passes += self.away_stats.passes
        self.away_team.passes_completed += self.away_stats.passes_completed

    def _simulate_goals(self) -> None:
        """Simulate who scored the goals and made the assists."""
        for _ in range(self.home_goals):
            scorer = random.choice([p for p in self.home_team.players if p.position != "GK"])
            scorer.goals += 1
            scorer.shots += 1
            scorer.shots_on_target += 1
            self.scorers.append(scorer)
            if random.random() < 0.8:  # 80% chance of assist
                assister = random.choice([p for p in self.home_team.players if p != scorer])
                assister.assists += 1
                self.assisters.append(assister)

        for _ in range(self.away_goals):
            scorer = random.choice([p for p in self.away_team.players if p.position != "GK"])
            scorer.goals += 1
            scorer.shots += 1
            scorer.shots_on_target += 1
            self.scorers.append(scorer)
            if random.random() < 0.8:  # 80% chance of assist
                assister = random.choice([p for p in self.away_team.players if p != scorer])
                assister.assists += 1
                self.assisters.append(assister)

        # Update clean sheets
        if self.away_goals == 0:
            self.home_team.clean_sheets += 1
            for p in self.home_team.players:
                if p.position == "GK":
                    p.clean_sheets += 1
        if self.home_goals == 0:
            self.away_team.clean_sheets += 1
            for p in self.away_team.players:
                if p.position == "GK":
                    p.clean_sheets += 1

    def __str__(self) -> str:
        status = "✓" if self.completed else "⏳"
        return f"{status} {self.home_team.name} {self.home_goals} - {self.away_goals} {self.away_team.name}"


@dataclass
class League:
    name: str
    teams: List[Team]
    matches: List[Match] = field(default_factory=list)
    current_matchday: int = 0

    def generate_fixtures(self) -> None:
        """Generate a full season of fixtures with home and away matches."""
        # Clear any existing matches
        self.matches = []
        
        # Generate all possible combinations of teams
        fixtures = []
        for home, away in itertools.combinations(self.teams, 2):
            fixtures.append(Match(home, away))
            fixtures.append(Match(away, home))  # Return fixture
        
        # Shuffle the fixtures
        random.shuffle(fixtures)
        self.matches = fixtures

    def get_matchday_fixtures(self, matchday: int) -> List[Match]:
        """Get all matches for a specific matchday."""
        matches_per_day = len(self.teams) // 2
        start_idx = (matchday - 1) * matches_per_day
        end_idx = start_idx + matches_per_day
        return self.matches[start_idx:end_idx]

    def simulate_matchday(self) -> List[Match]:
        """Simulate the next matchday's matches."""
        if self.current_matchday >= len(self.matches) // (len(self.teams) // 2):
            return []

        self.current_matchday += 1
        fixtures = self.get_matchday_fixtures(self.current_matchday)
        for match in fixtures:
            match.simulate()
        return fixtures

    def get_league_table(self) -> List[Team]:
        """Get the current league table sorted by points and goal difference."""
        return sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference, t.goals_for),
            reverse=True
        )

    def get_top_scorers(self, limit: int = 5) -> List[Player]:
        """Get the top goal scorers."""
        all_players = [p for team in self.teams for p in team.players]
        return sorted(all_players, key=lambda p: p.goals, reverse=True)[:limit]

    def get_top_assisters(self, limit: int = 5) -> List[Player]:
        """Get the top assisters."""
        all_players = [p for team in self.teams for p in team.players]
        return sorted(all_players, key=lambda p: p.assists, reverse=True)[:limit]

    def get_top_clean_sheets(self, limit: int = 5) -> List[Player]:
        """Get the goalkeepers with most clean sheets."""
        goalkeepers = [p for team in self.teams for p in team.players if p.position == "GK"]
        return sorted(goalkeepers, key=lambda p: p.clean_sheets, reverse=True)[:limit]

    def get_disciplinary_table(self, limit: int = 5) -> List[Player]:
        """Get players with most cards (yellow cards count as 1, red cards as 2)."""
        all_players = [p for team in self.teams for p in team.players]
        return sorted(all_players, key=lambda p: p.yellow_cards + p.red_cards * 2, reverse=True)[:limit]

    def get_pass_masters(self, limit: int = 5) -> List[Player]:
        """Get players with best pass accuracy (minimum 100 passes)."""
        all_players = [p for team in self.teams for p in team.players if p.passes >= 100]
        return sorted(all_players, key=lambda p: p.pass_accuracy, reverse=True)[:limit] 