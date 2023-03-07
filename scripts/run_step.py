import os
import sys

import logging

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, ".."))

sys.path.append(PACKAGE_PATH)


from prv_candidates_step import PrvCandidatesStep


def step_creator():
    from settings import settings_creator

    settings = settings_creator()
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if "LOGGING_DEBUG" in locals():
        if settings["LOGGING_DEBUG"]:
            level = logging.DEBUG
    return PrvCandidatesStep(config=settings, level=level)


if __name__ == "__main__":
    step_creator().start()
