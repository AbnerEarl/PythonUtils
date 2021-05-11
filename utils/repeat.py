import time
from pynput.keyboard import Controller as key_cl
from pynput.mouse import Controller, Button


def keyboard_input(string):
    keyboard = key_cl()
    keyboard.type(string)


def mouse_click():
    # mouse = Controller()
    # mouse.press(Button.left)
    # mouse.release(Button.left)
    keyboard = key_cl()
    keyboard.press("\n")
    keyboard.release("\n")


def main(number, string):
    time.sleep(5)
    for i in range(number):
        keyboard_input(string + str(i))
        mouse_click()
        time.sleep(0.2)


if __name__ == '__main__':
    main(3, "早上好～")
