# hangman.py
import random

# Small curated lists for predictable behaviour
WORDS = [
    "apple", "banana", "grape", "orange", "mango",
    "peach", "cherry", "papaya", "lemon", "melon", "guava", "kiwi"
]

PHRASES = [
    "hello world",
    "unit testing",
    "python programming",
    "clean code",
]


class Hangman:
    """
    Minimal, UI-agnostic Hangman model.

    - Letters are masked with underscores; spaces/punctuation are preserved.
    - A wrong *first-time* guess deducts one life.
    - Repeated guesses (right or wrong) do not deduct again.
    """

    def __init__(self, word=None, mode="word", lives=6):
        if word is not None:
            answer = str(word).lower()
        elif mode == "phrase":
            answer = random.choice(PHRASES)
        else:
            answer = random.choice(WORDS)

        self.word = answer.lower()
        self.lives = int(lives)
        self.max_lives = int(lives)
        self.guessed = set()
        # underscores for letters; keep non-letters as-is (e.g., spaces)
        self._display = ["_" if ch.isalpha() else ch for ch in self.word]

    @property
    def hidden_word(self):
        return "".join(self._display)

    def guess(self, letter):
        """
        Try a letter. Returns True if at least one position was revealed, else False.
        A wrong *first-time* guess deducts 1 life. Repeats are ignored.
        """
        if not letter or len(letter) != 1 or not letter.isalpha():
            return False

        letter = letter.lower()
        if letter in self.guessed:
            return False

        self.guessed.add(letter)

        if letter in self.word:
            revealed = False
            for i, ch in enumerate(self.word):
                if ch == letter and self._display[i] == "_":
                    self._display[i] = letter
                    revealed = True
            return revealed

        # wrong first-time guess
        if self.lives > 0:
            self.lives -= 1
        return False

    def is_won(self):
        return self.hidden_word == self.word

    def is_over(self):
        return self.is_won() or self.lives <= 0

    def reveal(self):
        return self.word


def play():
    print("\n🎮 Simple Hangman")
    mode_in = input("Choose mode: word / phrase (default: word): ").strip().lower()
    mode = "phrase" if mode_in == "phrase" else "word"
    game = Hangman(mode=mode, lives=6)

    print(f"\nYou have {game.lives} lives.")
    print(f"Word: {game.hidden_word}")

    while not game.is_over():
        print(f"\nLives: {game.lives} | Guessed: {', '.join(sorted(game.guessed)) or '-'}")
        raw = input("Enter a single letter (or 'quit'): ").strip().lower()
        if raw == "quit":
            print("Bye!")
            return

        if len(raw) != 1 or not raw.isalpha():
            print("⚠️  Please enter exactly one alphabetic character.")
            continue

        before = game.lives
        revealed = game.guess(raw)

        if raw in game.guessed and not revealed and raw not in game.word:
            if game.lives < before:
                print("❌ Wrong!")
            else:
                print("ℹ️  Already tried.")
        elif revealed:
            print("✅ Nice!")
        else:
            print("❌ Wrong!")

        print(f"Word: {game.hidden_word}")

    if game.is_won():
        print("\n🎉 You guessed it!")
    else:
        print(f"\n💀 Game over. The answer was: {game.reveal()}")


if __name__ == "__main__":
    play()
