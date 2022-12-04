with open('../files/flag.txt.encrypted', 'r') as f:
    encrypted = f.read()

# ref: https://docs.python.org/3/library/functions.html#chr:~:text=The%20valid%20range%20for%20the%20argument%20is%20from%200%20through%201%2C114%2C111%20(0x10FFFF%20in%20base%2016).%20ValueError%20will%20be%20raised%20if%20i%20is%20outside%20that%20range.
true_key = 0
for key in range(0x110000):
    if chr(ord(encrypted[0]) ^ key) == 't':
        true_key = key
        break

flag = ""
for ch in encrypted:
    flag += chr(ord(ch) ^ true_key)

with open('../flag.txt') as f:
    want = f.readline()

if flag != want:
    print(f"want: {want}, got: {flag}")
else:
    print(f"OK, {flag}")
