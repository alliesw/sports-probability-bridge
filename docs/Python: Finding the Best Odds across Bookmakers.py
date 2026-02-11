Since we are using American odds, the math is surprisingly simple for a computer: the highest number is always the best price (e.g., +150 is better than +120, and −105 is better than −115 because −105>−115).

Python: Finding the Best Odds across Bookmakers

This script connects to your sports_betting.db, looks at the most recent batch of data you've downloaded, and identifies which bookmaker is offering the highest payout for every team.

Python
import sqlite3

def find_best_odds():
    conn = sqlite3.connect('sports_betting.db')
    cursor = conn.cursor()

    # SQL Logic: 
    # 1. Get only the most recent 'timestamp' (current lines).
    # 2. Group by the game and the team (selection).
    # 3. Find the MAX price for each.
    query = """
    SELECT 
        home_team, 
        away_team, 
        selection, 
        MAX(price) as best_odds, 
        bookmaker 
    FROM odds 
    WHERE timestamp = (SELECT MAX(timestamp) FROM odds)
    GROUP BY event_id, selection
    ORDER BY home_team ASC;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print(f"{'GAME':<40} | {'BET ON':<20} | {'BEST ODDS':<10} | {'BOOKMAKER'}")
    print("-" * 90)
    
    for row in rows:
        game = f"{row[0]} vs {row[1]}"
        team = row[2]
        odds = row[3]
        bookie = row[4]
        print(f"{game:<40} | {team:<20} | {odds:<10} | {bookie}")

    conn.close()

if __name__ == "__main__":
    find_best_odds()
How the Logic Works

The Subquery: (SELECT MAX(timestamp) FROM odds) ensures that even if you have a month of historical data, the script only analyzes the odds from your latest "scrape."

The MAX() Function: As mentioned, because +200 is greater than +180 and −110 is greater than −120, a simple MAX() aggregate function finds the most bettor-friendly line.

Group By: We group by event_id and selection (the team) so that we get one "Best Price" for the Home team and one "Best Price" for the Away team.

Why Line Shopping Matters

Even a small difference in odds can drastically change your long-term profitability.

Odds	Implied Probability	Payout on $100
-115	53.5%	186.96
-110	52.4%	190.91
Finding a −110 line instead of a −115 line regularly is often the difference between being a "losing" bettor and a "break-even" or "winning" bettor over hundreds of games.
