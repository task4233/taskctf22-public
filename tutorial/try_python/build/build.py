numbers = [idx for idx in range(1, 1000, 2)]

with open('numbers.txt', 'w') as f:
    for number in numbers:
        f.write(str(number)+' ')

