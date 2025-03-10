# Football Match Simulator

This Python program simulates a football league where each team plays every other team twice (home & away). It generates random match results, updates a points table with goal difference (GD), and ranks teams based on performance.

---

## Features

1. **User Input for Teams**:
   - Users can input the names of the teams (minimum 2, maximum 20).
   - Teams are validated to ensure the correct number is entered.

2. **Random Fixture Generation**:
   - Teams are shuffled and paired into fixtures randomly.
   - If the number of teams is odd, one team gets a **bye** (no match for that round).

3. **Match Simulation**:
   - For each match, random scores are generated for both teams.
   - The winner is determined based on the scores, or it is declared a draw if the scores are equal.

4. **Points Table with Goal Difference (GD)**:
   - The league standings are sorted by:
     - **Points** (higher is better)
     - **Goal Difference** (GD) if points are tied

     

5. **Clear Output**:
   - The program displays:
     - Fixtures (list of matches).
     - Simulated match results (teams, scores, and winners)
     - Final points table (sorted by points & GD)
---

## How It Works

1. **Input Teams**:
   - The user is prompted to enter the names of the teams, separated by commas.
   - The program ensures the user enters **between 2 and 20 teams**.

2. **Generate Fixtures**:
   - Fixtures are randomized but follow a balanced schedule (no immediate rematches).
   - Each team plays every other twice (once home, once away).


3. **Simulate Matches**:
   - Random scores (0-5 goals) are assigned for each match.
   - The winner, draw, and goal difference are calculated.

4. **Display Results**:
   - The program prints:
     - Fixtures
     - Match results (teams, scores, and winners)
     - The updated points table.

---


---

## Requirements

- Python 3.x
- No external libraries are required.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/AseefBandey/football-match-simulator.git

2. Run the Program
   ```bash
   python league_simulator.py

 ## Future Improvements

- Add top scorers tracking
- Include Knockout Rounds (Champions League Format)
- Implement customized league settings (number of games per team, point rules, etc.)


Author

GitHub: AseefBandey

Email: aseefahmad46@gmail.com
