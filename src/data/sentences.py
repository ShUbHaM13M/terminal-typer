from dataclasses import dataclass
from enum import Enum
from random import randint


class WordState(Enum):
    NORMAL = 0
    CURRENT = 1
    INCORRECT = 2
    CORRECT = 3


@dataclass
class Word:
    value: str
    state: WordState


data = [
    "He enjoys practicing his ballet in the bathroom.",
    "The delicious aroma from the kitchen was ruined by cigarette smoke.",
    "Her daily goal was to improve on yesterday.",
    "The sunblock was handed to the girl before practice, but the burned skin was proof she did not apply it.",
    "The river stole the gods.",
    "Cats are good pets, for they are clean and are not noisy.",
    "In that instant, everything changed.",
    "Tuesdays are free if you bring a gnome costume.",
    "There have been days when I wished to be separated from my body, but today wasn’t one of those days.",
    "She saw the brake lights, but not in time.",
]


# TODO: Accept attributes for tweaking the lenght or words of the sentence
def get_random_sentence() -> str:
    sentence = data[randint(0, len(data) - 1)]
    return "\n".join(data)  # sentence
