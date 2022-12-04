numbers = None

with open('numbers.txt', 'r') as f:
    numbers = f.readlines()

numbers_list = numbers[0].split()

answer = 0
for number in numbers_list:
    answer += int(number)

print(f'taskctf{{{answer}}}')
