class Schema:
    def __init__(self, db):
        self.db = db
        
    def create_tables(self):
        """Erstellt alle notwendigen Tabellen"""
        try:
            with self.db:
                # Scores Tabelle
                self.db.execute("""
                    CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_name TEXT NOT NULL,
                        attempts INTEGER NOT NULL,
                        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Index für bessere Performance bei Highscores
                self.db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scores_attempts 
                    ON scores(attempts)
                """)
                
                self.db.execute("""
                    CREATE INDEX IF NOT EXISTS idx_scores_created 
                    ON scores(created DESC)
                """)
                
                print("Datenbank-Schema erfolgreich erstellt!")
                
        except Exception as e:
            print(f"Fehler beim Erstellen des Schemas: {e}")
            raise