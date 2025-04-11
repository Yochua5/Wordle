import turtle as t
import random 

t.hideturtle()
t.tracer(0)
t.penup()
t.setposition(-150, 300)

# function that makes a square, side length and color can be changed
def square(side, color="white"):
    # loop for each side of the square
    t.fillcolor(color)
    t.begin_fill()
    for i in range(4):
        t.pendown()
        t.forward(side)
        t.right(90)
        t.penup()
    t.end_fill()

# function that makes a row of squares the side length of each square and the amount of squares in the row can be decided later
def row(side, amount, color="white"):
    # length of row with space between each square
    row_length = side + 10
    # first square
    square(side, color)
    # loop to make the rest of the squares in row
    for i in range(amount):
        t.penup()
        t.forward(side+10)
        square(side, color)
    # resets mouse and moves it down so it's ready for the next row
    t.penup()
    t.right(90)
    t.forward(side)
    t.right(90)
    t.forward(row_length*amount)
    t.left(90)
    t.forward(10)
    t.left(90)

# loop to make the 6 rows for the user to guess
for i in range(6):
    row(50, 4)

#starting position for keyboard
start_x = -240
start_y = -100

# makes the squares for the first row of a keyboard
t.goto(start_x,start_y)
row(40, 9)

# look to make the last two rows of a keyboard
for i in range(1,3):
    x = start_x + 20 
    y = start_y - 55 * i
    t.goto(x,y)
    row(40, 8)

# starting position for the letters in the keybaord
start_x = -223
start_y = -128

# starting position for the box of the keyboard
keyboard_start_x = -240
keyboard_start_y = -100

# spacing for each row and column of the keyboard including the square 
keyborad_row_spacing = 55
keyborad_col_spacing = 50

# first row of a keyboard's letters
keyboard_letters_third = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']

# last two rows of a keyboard's letters
keyboard_letters_twothirds = [
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['↵', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
    ]

def start_keyboard_third(letters_x, letters_y, col_index):
    x = letters_x + col_index * keyborad_col_spacing
    y = letters_y
    t.goto(x,y)

def start_keyboard_twothirds(letters_x, letters_y, col_index, row_index):
    x = letters_x + col_index * keyborad_col_spacing + 20
    y = letters_y - row_index * keyborad_row_spacing - keyborad_row_spacing
    t.goto(x,y)


# loop to make first row keyboard letters
for col_index, letter in enumerate(keyboard_letters_third):
    # x and y postion that will shift the positioning depending on the column index
    start_keyboard_third(start_x, start_y, col_index)
     # writes the letter
    t.write(letter, font=("Arial", 10, "normal"))

# loop to make the rows of the last two keyboard letters
for row_index, row_keyboard in enumerate(keyboard_letters_twothirds):
    # loop to make the letters and appropriate spacing
    for col_index, letter in enumerate(row_keyboard):
        # x and y postion that will shift the positioning depending on the column index
        start_keyboard_twothirds(start_x, start_y, col_index, row_index)
         # writes the letter
        t.write(letter, font=("Arial", 10, "normal"))

# Select a random 5-letter word
with open("words.txt") as f:
    words = [word.strip().upper().replace(",", "").replace('"', "") for word in f]

random_word = random.choice(words)
# the guess
guessed_word = ""
# the position of the starting letters
letters_x = -135
letters_y = 260
# position of starting row
row_x = -150
row_y = 300
# spacing for where column starts
guess_col_spacing = 60

word_count = 0

confetti = []

def answer_key():
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(2):
        t.pendown()
        t.forward(380)
        t.right(90)
        t.forward(100)
        t.right(90)
        t.penup()
    t.end_fill()

def correct_word(letters_x, letters_y, array_word):
    t.goto(row_x, row_y)
    row(50, 4, "green")
    # puts letters back in green box
    for letter in array_word:
        t.goto(letters_x, letters_y)
        t.write(letter, font=("Arial", 20, "normal"))
        letters_x += 60

def rectangle(color, x, y):
    obj = t.Turtle()
    obj.pendown()
    obj.shape("square")
    obj.shapesize(stretch_wid=0.2, stretch_len=0.5)  # Adjusts size to match 5x10
    obj.color(color)
    obj.penup()
    obj.goto(x, y)
    return obj
    
def fall():
    for rectangle in confetti:
        y = rectangle.ycor()
        if y > -320:
            rectangle.sety(y-5)
    t.update()
    t.ontimer(fall,5)
    

# function to change box color
def box_color(color, array_letter, number, side):
    # shifts position depending on which letter is correct
    square_position = row_x + guess_col_spacing * number
    letter_position = letters_x + guess_col_spacing * number
    t.goto(square_position, row_y)
    # changes box to color chosen
    square(side, color)
    # replace letter in new box
    t.goto(letter_position, letters_y)
    t.write(array_letter, font=("Arial", 20, "normal"))

# function that is called when a key is pressed
def key_pressed(key):
    # allowing all of the variables to be changed even when the function is done
    global guessed_word 
    global letters_x
    global letters_y
    global row_x
    global row_y
    global word_count
    # changing the letter to uppercase
    key = key.upper()


    # making the max letters in the guess 5
    if len(guessed_word) < 5 and word_count < 6:
        # so it doesn't write "RETURN"
        if key != "RETURN" and key != "BACKSPACE":
            # adds letter the the guess
            guessed_word += key
            t.goto(letters_x, letters_y)
            # shifts position of letter to line up with next box
            letters_x += 60
            t.write(key, font=("Arial", 20, "normal"))

    if key == "BACKSPACE" and len(guessed_word) > 0:
        guessed_word = guessed_word[:-1]
        letters_x -= 60
        box_color("white", "", len(guessed_word), 50)

    # when a guess is entered
    if key == "RETURN":
        if len(guessed_word) < 5:
            return
        # resets position
        letters_x = -135
        # turns words into array
        array_guessed = list(guessed_word)
        array_word = list(random_word)
        
        # check if word is guessed
        if guessed_word == random_word:
            correct_word(letters_x, letters_y, array_word)
                
            for i in range(400):
                t.penup()
                x = random.randint(-380,370)
                y = random.randint(200,600)
                color = random.choice(["green", "blue", "red", "yellow"])
                rect = rectangle(color, x, y)
                confetti.append(rect)

            fall()
            return
        # loop to check if a letter is in the right spot


        # dictionary with colors and thier own dictionary for the letter and position
        data = {
                "green": {},
                "yellow": {},
                "gray": {}
            }
        
        # deteremin wether letter is green, yellow, or gray
        for i in range(5):
            if array_guessed[i] == array_word[i]:
                if array_guessed[i] in data["green"]:
                    data["green"][array_guessed[i]].append(i)
                else:
                    data["green"][array_guessed[i]] = [i]
                if array_guessed[i] in data["green"] and array_guessed[i] in data["yellow"] and len(data["green"][array_guessed[i]]) + len(data["yellow"][array_guessed[i]]) > array_word.count(array_guessed[i]):
                    last_value = list(data["yellow"].values())[-1]
                    if array_guessed[i] in data["gray"]:
                        data["gray"][array_guessed[i]].append(last_value[0])
                    else:
                        data["gray"][array_guessed[i]] = [last_value[0]]
                    data["yellow"][array_guessed[i]].pop()
            elif array_guessed[i] in data["yellow"] and len(data["yellow"][array_guessed[i]]) < array_word.count(array_guessed[i]):
                data["yellow"][array_guessed[i]].append(i)
            elif array_guessed[i] not in data["yellow"] and array_guessed[i] not in data["green"] and array_guessed[i] in array_word:
                data["yellow"][array_guessed[i]] = [i]
            elif array_guessed[i] not in data["yellow"] and array_guessed[i] in data["green"] and len(data["green"][array_guessed[i]]) < array_word.count(array_guessed[i]) and array_guessed[i] in array_word:
                data["yellow"][array_guessed[i]] = [i]
            elif array_guessed[i] in data["gray"]:
                data["gray"][array_guessed[i]].append(i)
            else:
                data["gray"][array_guessed[i]] = [i]

                
        
        for val in ["green", "yellow", "gray"]:
            for char in data[val]:
                for pos in data[val][char]:
                    # color the guess depending on if it is green, yellow, or gray
                    box_color(val, array_guessed[pos], pos, 50)
                    # colors top third of keyboard
                    for col_index, letter in enumerate(keyboard_letters_third):
                        if char == letter:
                            start_keyboard_third(keyboard_start_x, keyboard_start_y, col_index)
                            square(40, val)
                            start_keyboard_third(start_x, start_y, col_index)
                            t.write(letter, font=("Arial", 10, "normal"))
                    # colors last two thirds of keyboard
                    for row_index, row_keyboard in enumerate(keyboard_letters_twothirds):
                        # loop to make the letters and appropriate spacing
                        for col_index, letter in enumerate(row_keyboard):
                            if char == letter:
                                start_keyboard_twothirds(keyboard_start_x, keyboard_start_y, col_index, row_index)
                                square(40, val)
                                start_keyboard_twothirds(start_x, start_y, col_index, row_index)
                                t.write(letter, font=("Arial", 10, "normal"))
        # shift start of row being guessed down a row
        letters_y -= 60
        row_y -= 60
        # resets column position
        letters_x = -135
        t.goto(letters_x, letters_y)
        # reset guessed word
        guessed_word = ""  
        word_count += 1
        if word_count > 5:
            row_y = 175
            letters_y = 135
            t.goto(-200,200)
            answer_key()
            correct_word(letters_x, letters_y, array_word)
            return

# go back to row start
t.goto(letters_x, letters_y)
# when a key is pressed it starts the function
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
    t.Screen().onkey(lambda c=char: key_pressed(c), char)

def return_pressed():
    key_pressed("RETURN")


# so user can enter a guess
t.Screen().onkey(return_pressed, "Return")
t.Screen().onkey(lambda: key_pressed("BACKSPACE"), "BackSpace")
t.Screen().listen()

t.update()
t.done()