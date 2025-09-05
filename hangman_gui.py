# gui_hangman.py
import tkinter as tk
from tkinter import messagebox
from hangman import Hangman  # must be in the same folder


class HangmanGUI:
    """Tkinter GUI for Hangman with 15s per-guess countdown.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Hangman Game (GUI)")
        self.root.resizable(False, False)

        # Top row: Level selection
        top = tk.Frame(root, padx=12, pady=8)
        top.pack(fill=tk.X)

        tk.Label(top, text="Level:").pack(side=tk.LEFT)
        self.level = tk.StringVar(value="basic")  # "basic" or "intermediate"
        tk.Radiobutton(top, text="Basic (word)", variable=self.level, value="basic").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Intermediate (phrase)", variable=self.level, value="intermediate").pack(side=tk.LEFT)

        # Word display
        self.word_label = tk.Label(root, text="", font=("Arial", 28))
        self.word_label.pack(pady=(8, 4))

        # Status row: time + lives
        status = tk.Frame(root, padx=12, pady=4)
        status.pack()
        self.timer_label = tk.Label(status, text="Time left: 15s", font=("Arial", 14), fg="firebrick")
        self.timer_label.grid(row=0, column=0, padx=8)
        self.lives_label = tk.Label(status, text="Lives: -", font=("Arial", 14))
        self.lives_label.grid(row=0, column=1, padx=8)

        # Input row
        input_row = tk.Frame(root, padx=12, pady=10)
        input_row.pack()
        self.entry = tk.Entry(input_row, width=5, font=("Arial", 18), justify="center", state=tk.DISABLED)
        self.entry.grid(row=0, column=0, padx=6)
        self.guess_btn = tk.Button(input_row, text="Guess", width=8, command=self.on_guess, state=tk.DISABLED)
        self.guess_btn.grid(row=0, column=1, padx=6)

        # Control row: Reset + Quit
        controls = tk.Frame(root, padx=12, pady=6)
        controls.pack()
        self.reset_btn = tk.Button(controls, text="Reset", width=8, command=self.start_game)
        self.reset_btn.grid(row=0, column=0, padx=6)
        self.quit_btn = tk.Button(controls, text="Quit", width=8, command=root.destroy)
        self.quit_btn.grid(row=0, column=1, padx=6)

        # Message label
        self.msg_label = tk.Label(root, text="", font=("Arial", 12))
        self.msg_label.pack(pady=(0, 10))

        # game state
        self.game = None           # type: ignore[assignment]
        self.time_left = 15
        self._timer_job = None     # after() handle

        # Start immediately in the default level
        self.start_game()

        # Keep focus in the entry for fast play
        self.root.bind("<Return>", lambda _e: self.on_guess())
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # Game lifecycle

    def start_game(self) -> None:
        """Start a new round with the selected level and reset timer/UI."""
        # cancel any previous timer
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

        # map UI level to Hangman modes
        mode = "word" if self.level.get() == "basic" else "phrase"
        self.game = Hangman(mode=mode, lives=6)

        self.time_left = 15
        self._render_word()
        self._render_status()
        self.msg_label.config(text="Type a letter and press Guess.")
        self.entry.configure(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.guess_btn.configure(state=tk.NORMAL)

        # start ticking
        self._tick()

    def _end_game(self, won: bool) -> None:
        """Finish the round: stop timer, freeze inputs, and show result."""
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None

        self.entry.configure(state=tk.DISABLED)
        self.guess_btn.configure(state=tk.DISABLED)

        if won:
            self.msg_label.config(text="🎉 You won!")
            messagebox.showinfo("Hangman", "Congratulations! You guessed the word/phrase.")
        else:
            answer = self.game.reveal() if self.game else "?"
            self.msg_label.config(text=f"💀 Game Over! The answer was: {answer}")
            messagebox.showinfo("Hangman", f"Game over.\nThe word/phrase was: {answer}")

    def _on_close(self) -> None:
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
        self.root.destroy()

    # Timer logic

    def _tick(self) -> None:
        """Timer callback — runs every second. On 0: deduct a life and reset to 15s."""
        if not self.game:
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")

        if self.time_left <= 0:
            # Requirement 4: time up → deduct a life and continue
            self._deduct_life()
            self.time_left = 15
            self._render_status()
            self.msg_label.config(text="⌛ Time's up! A life was deducted.")

            if self.game.is_over():
                self._end_game(False)
                return

        else:
            self.time_left -= 1

        self._timer_job = self.root.after(1000, self._tick)

    def _deduct_life(self) -> None:
        """Deduct one life safely (works with the simple Hangman)."""
        if self.game and self.game.lives > 0:
            # If your Hangman has a timeout() method, call it; else decrement here.
            if hasattr(self.game, "timeout"):
                self.game.timeout()  # type: ignore[attr-defined]
            else:
                self.game.lives -= 1

    # UI events 

    def on_guess(self) -> None:
        """Handle 'Guess' button or Enter key."""
        if not self.game:
            return

        text = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if len(text) != 1 or not text.isalpha():
            self.msg_label.config(text="⚠️ Enter one alphabetic letter.")
            self.entry.focus_set()
            return

        previously = text in self.game.guessed
        revealed = self.game.guess(text)

        if previously:
            self.msg_label.config(text="ℹ️ Already tried.")
        elif revealed:
            self.msg_label.config(text="✅ Correct!")
        else:
            self.msg_label.config(text="❌ Wrong!")

        self._render_word()
        self._render_status()

        # Requirement 4: Reset the 15s window after each guess
        self.time_left = 15

        # Requirement 7/8: End game when won or lives exhausted
        if self.game.is_over():
            self._end_game(self.game.is_won())
            return

        self.entry.focus_set()

    # Rendering helpers

    def _render_word(self) -> None:
        """Show the masked word with spacing between characters for readability."""
        if not self.game:
            self.word_label.config(text="")
            return

        # Add spaces between characters (keeps phrase spaces visible)
        masked = self.game.hidden_word
        spaced = " ".join(masked)  # e.g., "_ _ _ _ _   _ _ _ _ _"
        self.word_label.config(text=spaced)

    def _render_status(self) -> None:
        if not self.game:
            self.timer_label.config(text="Time left: 15s")
            self.lives_label.config(text="Lives: -")
            return

        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.lives_label.config(text=f"Lives: {self.game.lives}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
