# Hangman-TDD (Python)

A compact **Hangman** game implemented with a **test-first** mindset.  
The repository includes a playable **CLI**, a **Tkinter GUI** with a visible **15-second** per-guess timer, a **unittest** test suite, and a companion **report**.

## Repository layout
<img width="800" height="222" alt="image" src="https://github.com/user-attachments/assets/5b6b7c2f-3a7f-4322-9ea4-d343c5a9f7b8" />

## Requirements
- Python **3.8+** (3.10+ recommended)
- `tkinter` (bundled on Windows/macOS; on Debian/Ubuntu: `sudo apt-get install python3-tk`)

## Quick start

### 1. Run the CLI
```bash
python hangman.py
```
- Choose word or phrase mode when prompted.
- Make single-letter guesses; lives decrement on wrong first-time guesses.
- The game ends on win (all letters revealed) or lose (lives = 0).
  
### 2. Run the GUI
```bash
python hangman_gui.py
```
- Select Basic (word) or Intermediate (phrase).
- A visible 15s timer resets after each guess; when it reaches 0, 1 life is deducted.
- Use Reset to start a new round; Quit closes the app.
  
### 3. Run the tests (unittest)
``` bash
python -m unittest -v
# or
python test_hangman.py -v
```

