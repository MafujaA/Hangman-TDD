"""
Unit tests for the simple Hangman project.
"""

import unittest
from hangman import Hangman, WORDS, PHRASES

class TestHangmanBasicRequirements(unittest.TestCase):
    """Tests aligned to the core project requirements (no GUI/timer here)."""

    def test_basic_level_selects_word_from_dictionary(self):
        """Req. 1a + 2: Basic level must choose a word from WORDS."""
        game = Hangman(mode="word")
        self.assertIsInstance(game.word, str)
        self.assertIn(game.word, WORDS, "Basic level must draw from WORDS")

    def test_intermediate_level_selects_phrase_from_dictionary(self):
        """Req. 1b + 2: Intermediate level must choose a phrase from PHRASES."""
        game = Hangman(mode="phrase")
        self.assertIsInstance(game.word, str)
        self.assertIn(game.word, PHRASES, "Intermediate level must draw from PHRASES")
        self.assertIn(" ", game.word, "Phrases should contain a space")

    def test_initial_masking_uses_underscores_and_preserves_spaces(self):
        """Req. 3: Letters are underscores; spaces are preserved."""
        game = Hangman(word="hello world")
        self.assertEqual(game.hidden_word, "_____ _____")

    def test_correct_guess_reveals_all_matching_positions(self):
        """Req. 5: A correct guess reveals every occurrence of the letter."""
        game = Hangman(word="apple")
        self.assertEqual(game.hidden_word, "_____")
        revealed = game.guess("p")
        self.assertTrue(revealed, "Expected at least one letter to be revealed")
        self.assertEqual(game.hidden_word, "_pp__")

    def test_wrong_guess_deducts_one_life(self):
        """Req. 6: A wrong first-time guess deducts exactly one life."""
        game = Hangman(word="apple", lives=6)
        start = game.lives
        result = game.guess("z")
        self.assertFalse(result, "Wrong guess should return False")
        self.assertEqual(game.lives, start - 1, "Life should be deducted once for a wrong guess")

    def test_win_condition_when_all_letters_revealed(self):
        """Req. 7/8b: Game is won when the word is fully revealed."""
        game = Hangman(word="a", lives=6)
        game.guess("a")
        self.assertTrue(game.is_won())
        self.assertTrue(game.is_over())

    def test_lose_condition_when_lives_reach_zero(self):
        """Req. 7/8a: Game is over (lost) when lives hit zero."""
        game = Hangman(word="a", lives=1)
        game.guess("z")  # wrong
        self.assertFalse(game.is_won())
        self.assertTrue(game.is_over())


if __name__ == "__main__":
    unittest.main(verbosity=2)
