from gpiozero import Button
from signal import pause


action_queue = []

b1 = Button("GPIO17")
b1.when_released = lambda: action_queue.append("b1 pressed")


while True:
    while action_queue:
        action = action_queue.pop()
        print(f"handling {action}")