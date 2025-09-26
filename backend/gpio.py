from gpiozero import Button


button = Button(17, pull_up=True, bounce_time=0.10)


def setup_button_callback(callback):
    button.when_pressed = callback


button.wait_for_active()
