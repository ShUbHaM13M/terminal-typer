from dataclasses import dataclass
from enum import Enum
from typing import List
from wonderwords import RandomWord


class WordState(Enum):
    NORMAL = 0
    CURRENT = 1
    INCORRECT = 2
    CORRECT = 3


@dataclass
class Word:
    value: str
    state: WordState


def get_random_sentence(difficulty: str = "easy") -> List[str]:
    r = RandomWord()
    match difficulty:
        case "easy":
            return r.random_words(40, word_max_length=5)
        case "medium":
            return r.random_words(50, word_max_length=8)
        case "hard":
            return r.random_words(60, word_max_length=12)
        case _:
            raise Exception("Unknown difficulty")
