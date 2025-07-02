# Football Match Simulator

A realistic football league simulator with detailed match statistics, player performance tracking, and an interactive CLI interface.

## Features

- 🏃‍♂️ Realistic match simulation based on team and player ratings
- 📊 Detailed statistics tracking (goals, assists, clean sheets)
- 🎮 Interactive CLI with colored output
- ⚽ Player performance and form system
- 📈 League table with automatic sorting
- 🏆 End of season awards

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Football-Match-Simulator.git
cd Football-Match-Simulator
```

2. Install the package in development mode:
```bash
pip install -e .
```

## Usage

Run the simulator:
```bash
football-sim
```

Follow the prompts to:
1. Enter team names (2-20 teams, comma-separated)
2. Choose from available actions:
   - Simulate next matchday
   - View league table
   - View statistics
   - Exit

## Features in Detail

### Team Management
- Each team has 11 players (1 GK, 4 DEF, 4 MID, 2 FWD)
- Players have individual ratings and form factors
- Team strength is calculated based on player ratings and form

### Match Simulation
- Realistic scoring based on team strengths
- Home advantage factor
- Goal scorers and assists tracking
- Clean sheet tracking for goalkeepers

### Statistics
- Full league table with points, wins, draws, losses
- Goal difference and goals scored
- Top scorers list
- Top assisters list
- Clean sheets leaderboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
