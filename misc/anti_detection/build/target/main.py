import ssdeep

raw_file = 'main'
target_file = 'ex-main'

raw=None
with open(raw_file, 'rb') as f:
    raw = f.read()

target=None
with open(target_file, 'rb') as f:
    target = f.read()

hash1 = ssdeep.hash(raw)
hash2 = ssdeep.hash(target)
diff = ssdeep.compare(hash1, hash2)
print(diff)
print(hash1)
