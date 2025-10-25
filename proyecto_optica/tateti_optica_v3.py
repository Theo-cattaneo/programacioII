import tkinter as tk
from tkinter import font
import random

class TatetiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tateti Moderno")
        self.root.minsize(550, 650)
        self.root.resizable(True, True)

        # --- Paleta de Colores Moderna ---
        self.BG_COLOR = '#1a1a2e'
        self.FRAME_COLOR = '#16213e'
        self.BUTTON_COLOR = '#0D02A8'
        self.BUTTON_HOVER_COLOR = '#7307A5'
        self.X_COLOR = '#3498DB'  # Azul para la X
        self.O_COLOR = '#E74C3C'  # Rojo para el Círculo
        self.TEXT_COLOR = '#ECF0F1'
        self.ACCENT_COLOR = '#16c79a'
        self.STATUS_BG_COLOR = '#0f3460'
        self.TIMER_BG_COLOR = '#2c3e50'

        self.root.configure(bg=self.BG_COLOR)

        # --- Variables del Juego ---
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.time_left = 10
        self.timer_job = None

        # --- NUEVO: Mapeo del teclado numérico a las coordenadas del tablero ---
        self.key_map = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2),
            '4': (1, 0), '5': (1, 1), '6': (1, 2),
            '1': (2, 0), '2': (2, 1), '3': (2, 2)
        }

        # --- Fuentes ---
        self.game_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.welcome_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.winner_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.timer_font = font.Font(family="Courier", size=20, weight="bold")

        # --- Elementos de la Interfaz Gráfica ---
        self.create_widgets()
        
        # --- NUEVO: Vincular el evento de presionar una tecla al método handle_keypress ---
        self.root.bind('<KeyPress>', self.handle_keypress)
        
        self.start_timer()

    # --- NUEVO: Método para manejar las pulsaciones del teclado ---
    def handle_keypress(self, event):
        """Maneja los eventos de teclado para jugar con el teclado numérico."""
        # Si el juego ha terminado, no hacer nada
        if self.game_over:
            return

        key = event.char
        # Verificar si la tecla presionada es una de las teclas mapeadas (1-9)
        if key in self.key_map:
            row, col = self.key_map[key]
            # Llamar a la misma función que se ejecuta con el clic del mouse
            self.player_move(row, col)

    def create_widgets(self):
        # 1. Contenedor principal
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 2. Texto de bienvenida
        welcome_frame = tk.Frame(main_container, bg=self.BG_COLOR)
        welcome_frame.pack(pady=15)

        welcome_text_lines = [
            "Hola te invito a jugar",
            "un tateti para agudizar",
            "tu vista"
        ]
        for line_text in welcome_text_lines:
            line_frame = tk.Frame(welcome_frame, bg=self.BG_COLOR)
            line_frame.pack(pady=2)
            for i, char in enumerate(line_text):
                color = self.O_COLOR if i % 2 != 0 else self.X_COLOR
                label = tk.Label(line_frame, text=char, font=self.welcome_font, fg=color, bg=self.BG_COLOR)
                label.pack(side=tk.LEFT)

        # 3. Marco para el juego en curso
        self.game_active_frame = tk.Frame(main_container, bg=self.FRAME_COLOR, relief=tk.RAISED, bd=2)
        self.game_active_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # 3.1. Marco superior para el temporizador y el estado
        top_frame = tk.Frame(self.game_active_frame, bg=self.FRAME_COLOR)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 3.1.1. Temporizador pequeño en la esquina superior derecha
        self.timer_frame = tk.Frame(top_frame, bg=self.TIMER_BG_COLOR, relief=tk.SOLID, bd=1)
        self.timer_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        
        self.timer_label = tk.Label(
            self.timer_frame,
            text="10s",
            font=self.timer_font,
            fg=self.TEXT_COLOR,
            bg=self.TIMER_BG_COLOR,
            padx=10,
            pady=5
        )
        self.timer_label.pack()

        # 3.1.2. Etiqueta de estado (solo muestra el turno)
        self.status_label = tk.Label(
            top_frame,
            text="",
            font=self.status_font,
            bg=self.STATUS_BG_COLOR,
            fg=self.TEXT_COLOR,
            pady=10
        )
        self.status_label.pack(fill=tk.X, expand=True)
        self.update_status()

        # 3.2. Tablero de Tateti
        board_frame = tk.Frame(self.game_active_frame, bg=self.FRAME_COLOR)
        board_frame.pack(expand=True, pady=(0, 20))

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=self.game_font,
                    width=5,
                    height=2,
                    bg=self.BUTTON_COLOR,
                    fg=self.TEXT_COLOR,
                    relief=tk.FLAT,
                    bd=0,
                    activebackground=self.BUTTON_HOVER_COLOR,
                    command=lambda r=i, c=j: self.player_move(r, c)
                )
                btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.BUTTON_HOVER_COLOR))
                btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.BUTTON_COLOR))
                btn.grid(row=i, column=j, padx=8, pady=8)
                self.buttons[i][j] = btn

        # 4. Marco para la pantalla de fin de juego
        self.game_over_frame = tk.Frame(main_container, bg=self.BG_COLOR)
        
        self.winner_label = tk.Label(
            self.game_over_frame,
            text="",
            font=self.winner_font,
            bg=self.BG_COLOR,
            fg=self.ACCENT_COLOR
        )
        self.winner_label.pack(pady=50)

        play_again_button = tk.Button(
            self.game_over_frame,
            text="Volver a Jugar",
            font=self.status_font,
            command=self.reset_game,
            bg=self.ACCENT_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            bd=0,
            activebackground='#13a383',
            padx=20,
            pady=10
        )
        play_again_button.pack()

    def update_status(self):
        """Actualiza la etiqueta de estado con el turno actual."""
        if self.game_over:
            return
        
        player_name = "Jugador X (Azul)" if self.current_player == 'X' else "Jugador O (Rojo)"
        self.status_label.config(text=f"Turno de {player_name}")

    def update_timer_display(self):
        """Actualiza solo la visualización del temporizador."""
        if self.game_over:
            self.timer_frame.pack_forget()
            return
            
        self.timer_label.config(text=f"{self.time_left}s")
        
        if self.time_left <= 3:
            self.timer_label.config(fg=self.O_COLOR)
        else:
            self.timer_label.config(fg=self.TEXT_COLOR)

    def player_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return

        self.place_mark(row, col)
        if not self.check_game_over():
            self.switch_turn()

    def place_mark(self, row, col):
        """Coloca la marca (X o O) en el tablero y le asigna su color."""
        self.board[row][col] = self.current_player
        
        if self.current_player == 'X':
            mark_text = 'X'
            color = self.X_COLOR  # Azul
        else:
            mark_text = 'O'
            color = self.O_COLOR  # Rojo
            
        # Se configura el texto y el color
        self.buttons[row][col]['text'] = mark_text
        self.buttons[row][col]['fg'] = color
        
        # --- MODIFICACIÓN CLAVE ---
        # Se establece el color 'disabledforeground'. Cuando un botón se deshabilita
        # (state='disabled'), algunos sistemas operativos ignoran el color 'fg' y lo
        # ponen gris. Esta línea asegura que el color se mantenga (azul o rojo)
        # incluso después de deshabilitar el botón.
        self.buttons[row][col]['disabledforeground'] = color
        
        # Se deshabilita el botón para que no se pueda volver a hacer clic
        self.buttons[row][col]['state'] = 'disabled'

    def switch_turn(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.time_left = 10
        self.start_timer()
        self.update_status()

    def start_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.update_timer()

    def update_timer(self):
        if self.game_over:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.make_random_move()

    def make_random_move(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']
        
        if not empty_cells:
            self.end_game("¡Es un empate! Nadie gana.")
            return

        row, col = random.choice(empty_cells)
        self.place_mark(row, col)
        
        if not self.check_game_over():
            self.switch_turn()

    def check_game_over(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                winner = 'X' if self.board[i][0] == 'X' else 'O'
                self.end_game(f"¡El jugador {winner} ha ganado!")
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                winner = 'X' if self.board[0][i] == 'X' else 'O'
                self.end_game(f"¡El jugador {winner} ha ganado!")
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            winner = 'X' if self.board[0][0] == 'X' else 'O'
            self.end_game(f"¡El jugador {winner} ha ganado!")
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            winner = 'X' if self.board[0][2] == 'X' else 'O'
            self.end_game(f"¡El jugador {winner} ha ganado!")
            return True

        if all(self.board[r][c] != '' for r in range(3) for c in range(3)):
            self.end_game("¡Es un empate! Nadie gana.")
            return True
            
        return False

    def end_game(self, message):
        self.game_over = True
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.winner_label.config(text=message)
        
        self.game_active_frame.pack_forget()
        self.game_over_frame.pack(fill=tk.BOTH, expand=True)

    def reset_game(self):
        self.game_over_frame.pack_forget()
        self.game_active_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.timer_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.timer_label.config(fg=self.TEXT_COLOR)

        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.time_left = 10
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ''
                self.buttons[i][j]['fg'] = self.TEXT_COLOR
                self.buttons[i][j]['state'] = 'normal'
        
        self.status_label.config(fg=self.TEXT_COLOR)
        self.update_status()
        self.start_timer()

# --- Ejecución del Programa ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TatetiApp(root)
    root.mainloop()