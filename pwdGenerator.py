import random

print('welcome to password generator!')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ! @£$%^&*().,:'

number = input('how much amount do you want?: ')
number = int(number)

length = input('length your password?:  ')
length = int(length)

print('\nhere are your passwords:   ')

for pwd in range(number):
    password = ''
for c in range(length):
    password += random.choice(chars)
    print(password)    