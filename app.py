from pynput import mouse, keyboard
import time
import threading

mouse_control = mouse.Controller()

positions = {}
i = 0
automation = False
pause = False
duration = 3


def add_position(value):
    global i
    positions[i] = value
    i += 1


def set_automation():
    global automation, pause
    if not automation:
        automation = True
        print("Automation has been started")
        thread = threading.Thread(target=run_automation)
        thread.start()
    else:
        pause = not pause
        if pause:
            print("Automation has been paused")
        else:
            print("Automation is continuing")


def run_automation():
    global automation, pause
    while automation:
        if pause:
            time.sleep(0.1)
            continue
        for position in positions.values():
            if pause:
                break
            x, y = position
            mouse_control.position = (x, y)
            time.sleep(0.1)
            mouse_control.click(mouse.Button.left, 1)
            time.sleep(duration)
            if not automation:
                break


def on_press(key):
    if key == keyboard.Key.shift:
        set_automation()


def on_release(key):
    if key == keyboard.Key.esc:
        print("Automation has been killed")
        global automation
        automation = False
        mouse_listener.stop()
        keyboard_listener.stop()


def on_click(x, y, button, pressed):
    if pressed and not automation:
        add_position([x, y])
        print(f"Position {len(positions)} has been added: {x}, {y}")


mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

keyboard_listener.join()
mouse_listener.join()
