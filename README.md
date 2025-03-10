# Football Match Simulator

This Python program simulates football matches and can be used to generate ucl group stage(Old Version) between teams, generates random scores, determines winners, and maintains a points table. It is designed to mimic a football league or tournament, allowing users to input their own list of teams and see the results of simulated matches.

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

4. **Points Table**:
   - A points table is maintained and updated after each match:
     - **Win**: 3 points.
     - **Draw**: 1 point for each team.
     - **Loss**: 0 points.

5. **Clear Output**:
   - The program displays:
     - Fixtures (list of matches).
     - Match results (teams, scores, and winners).
     - Updated points table (sorted by points).

---

## How It Works

1. **Input Teams**:
   - The user is prompted to enter the names of the teams, separated by commas.
   - The program ensures the user enters **between 2 and 20 teams**.

2. **Generate Fixtures**:
   - Teams are shuffled and paired into matches.
   - If the number of teams is odd, one team gets a bye.

3. **Simulate Matches**:
   - For each match, random scores are generated for both teams.
   - The winner is determined, and the points table is updated.

4. **Display Results**:
   - The program prints:
     - The list of fixtures.
     - The results of each match (teams, scores, and winners).
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

Author

GitHub: AseefBandey

Email: aseefahmad46@gmail.com
