
# Football Match Simulator

This Python program simulates a football league where each team plays every other team twice (home & away). It generates random match results, updates a points table with goal difference (GD), and ranks teams based on performance. It now also tracks **top scorers**, **assists**, **clean sheets**, and simulates **matchdays** interactively.

---

## Features

1. **User Input for Teams**:
   - Users can input the names of the teams (minimum 2, maximum 20).
   - Teams are validated to ensure the correct number is entered.

2. **Random Fixture Generation (Home & Away)**:
   - Each team plays every other team twice – once at home, once away.
   - Fixtures are randomized and grouped into **matchdays**.
   - No team plays twice in the same matchday.

3. **Matchday Simulation**:
   - Press `Enter` to simulate each matchday manually.
   - Each match randomly generates scores between 0 and 5 for each team.
   - Winner is determined based on scores, or declared a draw if equal.

4. **Points Table with Goal Difference (GD)**:
   - The league standings are sorted by:
     - **Points** (higher is better)
     - **Goal Difference (GD)** if points are tied

5. **Player Stats Tracking**:
   - **Top Scorers**: Tracks players with the most goals.
   - **Top Assisters**: Tracks players providing the most assists.
   - **Clean Sheets**: Tracks goalkeepers who kept clean sheets.

6. **Clear Output**:
   - The program displays:
     - Fixtures (organized matchdays).
     - Simulated match results (teams, scores, and winners).
     - Player awards (top 5 scorers, assisters, clean sheet leaders).
     - Final points table (sorted by points & GD).

---

## How It Works

1. **Input Teams**:
   - The user is prompted to enter the names of the teams, separated by commas.
   - The program ensures the user enters **between 2 and 20 teams**.

2. **Generate Fixtures**:
   - Each team plays every other **twice** (home & away).
   - Fixtures are randomized and split into **matchdays**.
   - No duplicate team matchups on the same day.

3. **Simulate Matches**:
   - Random scores (0-5 goals) are assigned for each match.
   - Random players are assigned as scorers and assisters.
   - Clean sheets awarded to goalkeepers when opponents score 0.

4. **Display Results**:
   - The program prints:
     - Matchday fixtures and results.
     - Scorers, assisters, and clean sheets.
     - The updated points table.
     - Player awards after the final matchday.

---

## Requirements

- Python 3.x
- No external libraries are required.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/AseefBandey/football-match-simulator.git
   cd football-match-simulator

2. Run the Program:
   ```bash
   python league_simulator.py
Future Improvements


Include Knockout Rounds (Champions League Format)

Save stats and results to file

Add customizable league settings (e.g., points system, number of matches)

    GUI or Web Interface using Flask/Streamlit

Author

GitHub: AseefBandey
Email: aseefahmad46@gmail.com """
