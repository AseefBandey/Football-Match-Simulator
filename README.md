# Football-Match-Simulator
This Python program simulates football matches between teams, generates random scores, determines winners, and maintains a points table. It is designed to mimic a football league or tournament, allowing users to input their own list of teams and see the results of simulated matches.
Features

    User Input for Teams:

        Users can input the names of the teams (minimum 2, maximum 20).

        Teams are validated to ensure the correct number is entered.

    Random Fixture Generation:

        Teams are shuffled and paired into fixtures randomly.

        If the number of teams is odd, one team gets a bye (no match for that round).

    Match Simulation:

        For each match, random scores are generated for both teams.

        The winner is determined based on the scores, or it is declared a draw if the scores are equal.

    Points Table:

        A points table is maintained and updated after each match:

            Win: 3 points.

            Draw: 1 point for each team.

            Loss: 0 points.

    Clear Output:

        The program displays:

            Fixtures (list of matches).

            Match results (teams, scores, and winners).

            Updated points table (sorted by points).

How It Works

    Input Teams:

        The user is prompted to enter the names of the teams, separated by commas.

        The program ensures the user enters between 2 and 20 teams.

    Generate Fixtures:

        Teams are shuffled and paired into matches.

        If the number of teams is odd, one team gets a bye.

    Simulate Matches:

        For each match, random scores are generated for both teams.

        The winner is determined, and the points table is updated.

    Display Results:

        The program prints:

            The list of fixtures.

            The results of each match (teams, scores, and winners).

            The updated points table.
