import random

from Board import Board
from Player import Player

class CLIBattleships:
    def __init__(self):
        self.player1_board = None
        self.opponent_board = None
        self.player2_board = None
        self.vs_computer = False

    def start(self):
        print("Willkommen zu 'Schiffe Versenken'!")
        while True:
            print("\nOptionen:")
            print("1: Neues Spiel starten")
            print("2: Beenden")
            option = input("Wähle eine Option: ").strip()

            if option == "1":
                self.new_game()
            elif option == "2":
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Eingabe. Bitte erneut versuchen.")

    def new_game(self):
        print("\n--- Neues Spiel gestartet ---")

        # 1. Schiffe festlegen
        ships = self.get_ships_configuration()

        # 2. Spielfeldgröße basierend auf den Schiffen berechnen
        size = self.get_board_size(ships)

        # 3. Spieler 1 Spielfeld erstellen
        self.player1_board = Board()
        self.player1_board.create_board(size)
        print(f"Spielbrett Spieler 1 mit der Größe {size}x{size} wurde erstellt.")
        self.ask_for_random_ship_placement(self.player1_board, ships)


        # 4. Gegner auswählen (Computer oder Spieler 2)
        self.vs_computer = self.ask_game_mode()

        # 5. Gegnerisches Spielfeld erstellen und Schiffe platzieren
        if self.vs_computer:
            print("\nDer Computer platziert seine Schiffe...")
            self.opponent_board = Board()
            self.opponent_board.create_board(size)
            self.random_place_ships(self.opponent_board, ships, False)
        else:
            print("\nSpieler 2 platziert seine Schiffe.")
            self.player2_board = Board()
            self.player2_board.create_board(size)
            self.ask_for_random_ship_placement(self.player2_board, ships)

        # 6. Spielablauf
        self.play_game()


    def get_recommended_board_size(self, ships):
        num_ship_fields = sum(ships)  # Alle Schiffsfelder zusammenzählen
        min_size = int((num_ship_fields / 0.4) ** 0.5)  # Quadratwurzel für 40% Trefferwahrscheinlichkeit
        max_size = int((num_ship_fields / 0.2) ** 0.5)  # Quadratwurzel für 20% Trefferwahrscheinlichkeit
        return min_size, max_size


    def get_board_size(self, ships):
        # Berechnung der empfohlenen Größe
        min_size, max_size = self.get_recommended_board_size(ships)
        print(f"\nEmpfohlene Spielfeldgröße basierend auf deinen Schiffen: {min_size}x{min_size} bis {max_size}x{max_size}")

        while True:
            try:
                size = int(input(f"Gib die Größe des Spielfelds ein (Standard: {min_size}): ").strip())
                return size
            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl eingeben.")


    def ask_game_mode(self):
        while True:
            choice = input("Möchtest du gegen den Computer spielen? (j/n): ").strip().lower()
            if choice in ["j", "n"]:
                return choice == "j"
            print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")

    def place_ships(self, board, player_name, ships):
        print(f"\n{player_name} platziert seine Schiffe!")
        for ship_size in ships:
            while True:
                try:
                    start_position = input(
                        f"Startposition für ein Schiff der Größe {ship_size} (z. B. A1): ").strip().upper()
                    orientation = input("Ausrichtung (H = Horizontal, S = Senkrecht, D = Diagonal): ").strip().upper()
                    message = board.place_battleship(start_position, ship_size, orientation)
                    print(message)
                    self.print_own_board(board, "eigenes Board")
                    break  # Wenn erfolgreich, brich aus der Schleife aus
                except ValueError as e:
                    print(f"Fehler: {e}")
                except Exception as e:
                    print(f"Unvorhergesehener Fehler: {e}")


    def random_place_ships(self, board, ships, own_ships):
        orientations = ["H", "S", "D"]
        for ship_size in ships:
            while True:
                try:
                    row = random.choice(Board.alphabet[:len(board.board)])
                    col = random.randint(1, len(board.board))
                    orientation = random.choice(orientations)
                    message = board.place_battleship(f"{row}{col}", ship_size, orientation)
                    if own_ships:
                        print(message)
                    break  # Wenn erfolgreich, brich aus der Schleife aus
                except Exception as e:
                   continue


    def play_game(self):
        print("\nDas Spiel beginnt! Greife Positionen an, indem du eine Koordinate wie 'A1' eingibst.")
        turn_of_player = True  # True = Spieler, False = Gegenspieler/Computer

        while True:
            if turn_of_player:
                print("\nSpieler 1 ist an der Reihe!")
                board_to_attack = self.opponent_board
                computer_attack = False
                coordinate = input("Gib eine Koordinate ein (z. B. A1): ").strip().upper()
            else:
                if self.vs_computer:
                    print("\nDer Computer greift an...")
                    board_to_attack = self.player1_board
                    computer_attack = True
                    coordinate = self.computer_attack()
                else:
                    print("\nSpieler 2 ist an der Reihe!")
                    board_to_attack = self.player1_board
                    computer_attack = False
                    coordinate = input("Gib eine Koordinate ein (z. B. A1): ").strip().upper()

            try:
                result = board_to_attack.miss_or_hit(coordinate)
                print(result)
                self.print_board(board_to_attack, "Gegnerisches Spielfeld", computer_attack)
                if "Congratulations" in result:
                    print("\n--- Spiel beendet! ---")
                    break
            except ValueError as e:
                print(f"Fehler: {e}")

            # Wechsel der Runde
            turn_of_player = not turn_of_player

    def computer_attack(self):
        row = random.choice(Board.alphabet[:len(self.player1_board.board)])
        col = random.randint(1, len(self.player1_board.board))
        return f"{row}{col}"

    def print_board(self, board, title, computer_attack):
        print(f"\n{title}:")
        print("  " + " ".join(str(i + 1) for i in range(len(board.board))))
        for i, row in enumerate(board.board):
            print(f"{board.alphabet[i]} " + " ".join(self.render_cell(cell, False, computer_attack) for cell in row))

    def print_own_board(self, board, title):
        print(f"\n{title}:")
        print("  " + " ".join(str(i + 1) for i in range(len(board.board))))
        for i, row in enumerate(board.board):
            print(f"{board.alphabet[i]} " + " ".join(self.render_cell(cell, True, False) for cell in row))

    def render_cell(self, cell, own_board, computer_attack):
        if cell == 1 and (own_board or computer_attack):  # Schiff noch nicht getroffen
            return "O"
        elif cell == -1:  # Schuss getroffen
            return "X"
        elif cell == 0 or not (own_board and computer_attack):  # Unbekannt/unberührt
            return "~"
        return "?"

    def get_ships_configuration(self):
        print("\n---- Schiffe Konfiguration ----")
        use_default = input("Möchtest du mit der Standard-Schiffskonfiguration spielen? (j/n): ").strip().lower()
        if use_default == 'j':
            return self.get_default_ships()

        # Benutzerdefinierte Schiffskonfiguration
        ships = []
        while True:
            try:
                size = int(input("Gib die Größe des Schiffs ein (z. B. 4 für ein Schlachtschiff): ").strip())
                quantity = int(input(f"Wie viele Schiffe der Größe {size}? ").strip())
                ships.extend([size] * quantity)  # Für n Schiffe der gleichen Größe
                more_ships = input("Möchtest du weitere Schiffe hinzufügen? (j/n): ").strip().lower()
                if more_ships != 'j':
                    break
            except ValueError:
                print("Ungültige Eingabe. Bitte Zahlen verwenden.")
        print("\nSchiffskonfiguration abgeschlossen.")
        print(f"Deine Schiffe: {ships}")
        return ships

    def get_default_ships(self):
        # Standard-Schiffskonfiguration: [1x4, 2x3, 3x2]
        return [4, 3, 3, 2, 2, 2]

    def ask_for_random_ship_placement(self, board, ships):
        choice = input("Möchtest du deine Schiffe selber platzieren? (j/n): ").strip().lower()
        if choice in ["j", "n"]:
            if choice == "j":
                self.place_ships(board, "Spieler 1", ships)
            else:
                self.random_place_ships(board, ships, True)
                self.print_own_board(board, "Eigenes Board")
        print("Ungültige Eingabe. Bitte 'j' oder 'n' eingeben.")


# Start des Spiels
if __name__ == "__main__":
    cli_game = CLIBattleships()
    cli_game.start()