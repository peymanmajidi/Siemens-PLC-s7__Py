import keyboard #Using module keyboard
while True:  #making a loop
    if keyboard.is_pressed('up'): #if key 'up' is pressed.You can use right,left,up,down and others
        print('PRESSED ',end='')
    else:
        pass

