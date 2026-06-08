import mysql.connector

# ============================================
# STEP 1: CONNECT TO MYSQL
# ============================================
conn = mysql.connector.connect(host="localhost", user="root", password="1401")
cursor = conn.cursor()

# ============================================
# STEP 2: CREATE DATABASE
# ============================================
cursor.execute("CREATE DATABASE IF NOT EXISTS cricket_db")
cursor.execute("USE cricket_db")
print("Database created successfully!")

# ============================================
# STEP 3: CREATE TABLES
# ============================================

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(50),
    coach VARCHAR(50)
)"""
)
print("Teams table created!")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(50),
    team_id INT,
    role VARCHAR(30),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
)"""
)
print("Players table created!")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS matches (
    match_id INT PRIMARY KEY,
    team1_id INT,
    team2_id INT,
    winner_team_id INT,
    match_date DATE,
    venue VARCHAR(100),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
)"""
)
print("Matches table created!")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS performances (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    player_id INT,
    runs INT,
    wickets INT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
)"""
)
print("Performances table created!")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS umpires (
    umpire_id INT PRIMARY KEY,
    umpire_name VARCHAR(50)
)"""
)
print("Umpires table created!")

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS match_umpires (
    match_id INT,
    umpire_id INT,
    PRIMARY KEY (match_id, umpire_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (umpire_id) REFERENCES umpires(umpire_id)
)"""
)
print("Match_Umpires table created!")
conn.commit()

# ============================================
# STEP 4: INSERT DATA
# ============================================
cursor.execute("SELECT COUNT(*) FROM teams")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute(
        """
    INSERT INTO teams VALUES
    (1,'MI','Coach A'),(2,'CSK','Coach B'),(3,'RCB','Coach C'),
    (4,'KKR','Coach D'),(5,'SRH','Coach E'),(6,'DC','Coach F'),
    (7,'GT','Coach G'),(8,'RR','Coach H'),(9,'PBKS','Coach I'),
    (10,'LSG','Coach J')"""
    )
    print("Teams data inserted!")

    cursor.execute(
        """
    INSERT INTO players VALUES
    (1,'Rohit',1,'Batsman'),(2,'Surya',1,'Batsman'),
    (3,'Bumrah',1,'Bowler'),(4,'Dhoni',2,'Batsman'),
    (5,'Jadeja',2,'All-Rounder'),(6,'Deepak',2,'Bowler'),
    (7,'Kohli',3,'Batsman'),(8,'Faf',3,'Batsman'),
    (9,'Siraj',3,'Bowler'),(10,'Russell',4,'All-Rounder'),
    (11,'Gill',7,'Batsman'),(12,'Buttler',8,'Batsman'),
    (13,'Warner',6,'Batsman'),(14,'Pant',6,'Batsman'),
    (15,'Samson',8,'Batsman'),(16,'Shami',7,'Bowler'),
    (17,'Arshdeep',9,'Bowler'),(18,'Rahul',10,'Batsman'),
    (19,'Stoinis',10,'All-Rounder'),(20,'Livingstone',9,'All-Rounder')"""
    )
    print("Players data inserted!")

    cursor.execute(
        """
    INSERT INTO matches VALUES
    (1,1,2,1,'2023-04-01','Mumbai'),
    (2,3,2,2,'2023-04-02','Chennai'),
    (3,1,3,3,'2023-04-03','Delhi'),
    (4,4,5,4,'2023-04-04','Kolkata'),
    (5,6,7,7,'2023-04-05','Ahmedabad'),
    (6,8,9,8,'2023-04-06','Jaipur'),
    (7,10,1,1,'2023-04-07','Lucknow'),
    (8,2,3,3,'2023-04-08','Chennai'),
    (9,4,6,6,'2023-04-09','Delhi'),
    (10,5,7,7,'2023-04-10','Hyderabad')"""
    )
    print("Matches data inserted!")

    cursor.execute(
        """
    INSERT INTO umpires VALUES
    (1,'Umpire A'),(2,'Umpire B'),(3,'Umpire C')"""
    )
    print("Umpires data inserted!")

    cursor.execute(
        """
    INSERT INTO match_umpires VALUES
    (1,1),(1,2),(2,2),(2,3),(3,1),(3,3)"""
    )
    print("Match_Umpires data inserted!")

    cursor.execute(
        """
    INSERT INTO performances (match_id, player_id, runs, wickets) VALUES
    (1,1,45,0),(1,2,30,0),(1,3,5,3),(1,4,20,0),(1,5,10,2),
    (2,7,60,0),(2,8,25,0),(2,9,5,2),(2,4,40,0),(2,6,10,3),
    (3,1,35,0),(3,7,55,0),(3,9,10,2),(3,3,5,3),
    (4,10,70,1),(4,5,30,2),(4,11,25,0),(4,12,40,0),
    (5,13,50,0),(5,16,10,3),(6,12,65,0),(6,17,5,4),
    (7,18,55,0),(7,19,30,1),(8,4,60,0),(8,7,50,0),
    (9,14,45,0),(9,15,30,1),(10,13,35,0),(10,16,50,0)"""
    )
    print("Performances data inserted!")

    conn.commit()
    print("\nAll data inserted successfully!")
else:
    print("Data already exists, skipping insert.")

# ============================================
# STEP 5: RUN QUERIES
# ============================================


def run_query(title, query):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print("=" * 55)
    cursor.execute(query)
    rows = cursor.fetchall()
    if cursor.description:
        headers = [i[0] for i in cursor.description]
        print(" | ".join(f"{h:<22}" for h in headers))
        print("-" * 55)
        for row in rows:
            print(" | ".join(f"{str(v):<22}" for v in row))
    print()


run_query("1. Total Matches", "SELECT COUNT(*) AS total_matches FROM matches")

run_query(
    "2. Wins Per Team",
    """
    SELECT t.team_name, COUNT(*) AS wins
    FROM matches m JOIN teams t
    ON m.winner_team_id = t.team_id
    GROUP BY t.team_name ORDER BY wins DESC""",
)

run_query(
    "3. Players Per Team",
    """
    SELECT t.team_name, COUNT(p.player_id) AS players_count
    FROM teams t LEFT JOIN players p
    ON t.team_id = p.team_id
    GROUP BY t.team_name""",
)

run_query(
    "4. Top Run Scorers",
    """
    SELECT p.player_name, SUM(runs) AS total_runs
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    GROUP BY p.player_name ORDER BY total_runs DESC""",
)

run_query(
    "5. Top 5 Batsmen",
    """
    SELECT p.player_name, SUM(runs) AS total_runs
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_runs DESC LIMIT 5""",
)

run_query(
    "6. Best Bowlers",
    """
    SELECT p.player_name, SUM(wickets) AS total_wickets
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    GROUP BY p.player_name ORDER BY total_wickets DESC""",
)

run_query(
    "7. Team Total Runs",
    """
    SELECT t.team_name, SUM(pf.runs) AS total_runs
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    JOIN teams t ON p.team_id = t.team_id
    GROUP BY t.team_name ORDER BY total_runs DESC""",
)

run_query(
    "8. Matches Played Per Team",
    """
    SELECT t.team_name, COUNT(*) AS matches_played
    FROM teams t JOIN matches m
    ON t.team_id = m.team1_id OR t.team_id = m.team2_id
    GROUP BY t.team_name""",
)

run_query(
    "9. Win Percentage",
    """
    SELECT t.team_name, COUNT(*) AS matches_played,
    SUM(CASE WHEN m.winner_team_id = t.team_id
        THEN 1 ELSE 0 END) AS wins,
    ROUND(SUM(CASE WHEN m.winner_team_id = t.team_id
        THEN 1 ELSE 0 END)*100/COUNT(*),2) AS win_percentage
    FROM teams t JOIN matches m
    ON t.team_id = m.team1_id OR t.team_id = m.team2_id
    GROUP BY t.team_name ORDER BY win_percentage DESC""",
)

run_query(
    "10. Best Score Per Match",
    "SELECT match_id, MAX(runs) AS best_score FROM performances GROUP BY match_id",
)

run_query(
    "11. Highest Scorer Overall",
    """
    SELECT p.player_name, SUM(runs) AS total_runs
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_runs DESC LIMIT 1""",
)

run_query(
    "12. Team Total Wickets",
    """
    SELECT t.team_name, SUM(pf.wickets) AS total_wickets
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    JOIN teams t ON p.team_id = t.team_id
    GROUP BY t.team_name ORDER BY total_wickets DESC""",
)

run_query("13. Match Venues", "SELECT match_id, venue FROM matches")

run_query(
    "14. Players With 50+ Total Runs",
    """
    SELECT p.player_name, SUM(runs) AS total_runs
    FROM performances pf
    JOIN players p ON pf.player_id = p.player_id
    GROUP BY p.player_name HAVING total_runs > 50""",
)

run_query(
    "15. All-Rounders", "SELECT player_name FROM players WHERE role = 'All-Rounder'"
)

run_query(
    "16. Players With Wickets > 2 in a Match",
    "SELECT player_id, wickets FROM performances WHERE wickets > 2",
)

run_query(
    "17. Total Runs Per Match",
    "SELECT match_id, SUM(runs) AS total_runs FROM performances GROUP BY match_id",
)

run_query(
    "18. Average Runs Per Player",
    "SELECT player_id, ROUND(AVG(runs),2) AS avg_runs FROM performances GROUP BY player_id",
)

run_query(
    "19. Matches Per Venue",
    "SELECT venue, COUNT(*) AS matches FROM matches GROUP BY venue",
)

run_query(
    "20. Full Match Info",
    """
    SELECT m.match_id, t1.team_name AS team1,
    t2.team_name AS team2, t3.team_name AS winner
    FROM matches m
    JOIN teams t1 ON m.team1_id = t1.team_id
    JOIN teams t2 ON m.team2_id = t2.team_id
    JOIN teams t3 ON m.winner_team_id = t3.team_id""",
)

# ============================================
# STEP 6: CLOSE CONNECTION
# ============================================
cursor.close()
conn.close()
print("Connection closed.")
print("Done! All 20 queries executed successfully!")
