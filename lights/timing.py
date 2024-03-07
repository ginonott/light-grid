from datetime import datetime, timedelta
from typing import ClassVar


def is_after(last_run: datetime, delta: timedelta):
    return datetime.now() > (last_run + delta)

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