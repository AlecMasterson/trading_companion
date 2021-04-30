from argparse import ArgumentParser
from model.Interval import Interval
from model.Source import Source
from typing import List
import enum


class Argument(enum.Enum):
    ACTUAL = {
        "compact": "-a",
        "expanded": "--actual",
        "options": {"action": "store_true", "dest": "ACTUAL"},
    }
    INTERVAL = {
        "compact": "-i",
        "expanded": "--interval",
        "options": {"choices": list(Interval), "dest": "INTERVAL", "required": True, "type": Interval},
    }
    SOURCE = {
        "compact": "-s",
        "expanded": "--source",
        "options": {"choices": list(Source), "dest": "SOURCE", "required": True, "type": Source},
    }
    TICKER = {
        "compact": "-t",
        "expanded": "--ticker",
        "options": {"dest": "TICKER", "required": True, "type": str},
    }


def get_args(requiredArgs: List[Argument]) -> dict:
    parser = ArgumentParser()

    def add_arg(arg: Argument) -> None:
        parser.add_argument(arg.value["compact"], arg.value["expanded"], **arg.value["options"])

    [add_arg(arg) for arg in requiredArgs]

    return parser.parse_args()
