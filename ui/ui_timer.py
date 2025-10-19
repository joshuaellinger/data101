#
# Timer support recording how long it takes perform different actions
#
# Importing this file creates a global timer instance that records
# up to 10K actions and prints them when the program exits.  It uses
# numpy arrays for efficiency.
# 
# Call ui_timer.TIMER.record("text") to record when of interest something happens 
#
import pandas as pd
import numpy as np
import atexit
import time

class Timer():
    def __init__(self):
        self.cnt = 0
        self.timings = np.zeros(10_000)
        self.labels = np.zeros(10_000, dtype=np.object_)

        self.record("START")

    def record(self, msg: str):
        "record a message with a timestamp"
        if self.cnt >= 10_000-1 and msg != "END":
            raise Exception("Timer full") 
        self.timings[self.cnt] = time.time()
        self.labels[self.cnt] = msg
        self.cnt += 1

    def to_frame(self):
        "convert messages/timing to dataframe"
        df = pd.DataFrame({
            "Labels": self.labels[0: self.cnt],
            "DeltaMS": 0.0
        })
        df.DeltaMS.values[1:] = (1e3 * (self.timings[1: self.cnt] - self.timings[0: self.cnt-1])).round(3)
        df["At"] = (1e-3*df.DeltaMS.cumsum()).round(3)
        return df
    
TIMER = Timer()

def show_timing():
    TIMER.record("END")

    df = TIMER.to_frame()
    print("TIMING:")
    with pd.option_context("display.max_rows", None):
        print(df)

atexit.register(show_timing)