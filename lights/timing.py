from datetime import datetime, timedelta
from random import randint
from typing import ClassVar


def is_after(last_run: datetime, delta: timedelta):
    return datetime.now() > (last_run + delta)

def is_before(last_run: datetime, delta: timedelta):
    return not is_after(last_run, delta)

class Interval:
    interval: timedelta
    last_run: datetime
    def __init__(self, interval: timedelta, immediate=True) -> None:
        self.last_run = datetime.now() - interval if immediate else datetime.now()
        self.interval = interval

    def is_ready(self):
        if (self.last_run + self.interval) < datetime.now():
            self.last_run = datetime.now()
            return True
        
        return False


class FuzzyInterval(Interval):
    min_seconds: int
    max_seconds: int

    def __init__(self, min_seconds: int, max_seconds: int) -> None:
        super().__init__(interval=timedelta(seconds=0))

        self.min_seconds = min_seconds
        self.max_seconds = max_seconds
        self.interval = self._get_next_interval()

    def _get_next_interval(self):
        return timedelta(seconds=randint(self.min_seconds, self.max_seconds))
    
    def is_ready(self):
        ready = super().is_ready()
        if ready:
            self.interval = self._get_next_interval()

        return ready



class AnimationTiming:
    last_run: datetime = None
    delta: ClassVar[timedelta]

    def should_run(self):
        if self.last_run is None:
            self.last_run = datetime.now() - self.delta
            
        if is_after(self.last_run, self.delta):
            self.last_run = datetime.now()
            return True
        
        return False