from gpiozero import Button


button = Button(17, pull_up=True, bounce_time=0.10)


def setup_button_callback(callback):
    button.when_pressed = callback


def is_button_pressed() -> bool:
    if button.is_active:
        return True
    else:
        return False


# button.wait_for_active()
