import time
import pandas as pd
import logging
from pynput.mouse import Listener


log = logging.getLogger(__name__)


click_times = []
reaction_times = []
mouse_pos = []


def on_move(x: float, y: float) -> None:
    mouse_pos.append((x, y, time.time()))


def on_click(x: float, y: float, pressed: bool) -> None:
    if pressed:
        click_times.append(time.time())
    if len(click_times) > 1:
        react_time = click_times[-1] - click_times[-2]
        reaction_times.append(react_time)
        log.debug(f"Reaction time {react_time:.3f} seconds") 

