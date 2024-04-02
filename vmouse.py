import keyboard, pyautogui as pg
movement = False
pressed = False
def on_press(event):
    key_name = event.name
    global movement, pressed

    # Movimientos
    if movement == True:
        if key_name == '8' or key_name == '2' or key_name == '6' or key_name == '4' or key_name == '3' or key_name == '1' or key_name == '5' or key_name == '7' or key_name == '9': pg.press('backspace')
        if key_name == '8':
            x, y = pg.position()
            pg.moveTo(x, y-15)
        elif key_name == '2':
            x, y = pg.position()
            pg.moveTo(x, y+15)
        elif key_name == '6':
            x, y = pg.position()
            pg.moveTo(x+15, y)
        elif key_name == '4':
            x, y = pg.position()
            pg.moveTo(x-15, y)
        # Clicks
        elif key_name == '7':
            pg.leftClick()
        elif key_name == '5':
            pg.middleClick()
        elif key_name == '9':
            pg.rightClick()
        elif key_name == '1':
            print("aa")
            if not pressed: pg.mouseDown(button='left'); pressed = True
            else: pg.mouseUp(button='left')
        elif key_name == '3':
            if not pressed: pg.mouseDown(button='right'); pressed = True
            else: pg.mouseUp(button='right')
    if key_name == '-':
        movement = not movement

keyboard.on_press(on_press)
