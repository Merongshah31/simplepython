#teka nombor comp dgn player
import random

#player
def guess(x):   
    random_number = random.randint(1, x) 
    guess = 0
    while guess != random_number:
        guess = int(input(f'guess the number between 1 and {x}:  '))
        if guess < random_number:
            print('sorry, tooo low , guess again hehehe')
        elif guess > random_number:
            print('soorry, too high , guess again huhuhu')    
    print(f'congratss , you guess the number {random_number} correct')

#comp
def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    while feedback != 'c':
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low    
        feedback = input(f'is {guess} to high (h), too low (L), or correct (C)')
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'L':
            low = guess + 1


    print(f"ahahahahahh the computer guess your number {guess}, correctly! ")        

computer_guess(10)
