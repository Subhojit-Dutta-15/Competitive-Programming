s = "anagram"
t = "nagaram"
seen = {}
if len(s) != len(t):
    print(False)
else:
    for char in s:
        seen[char] = seen.get(char, 0) + 1
    for char in t:
        if seen.get(char, 0) == 0:
            print(False)
            break
        seen[char] -= 1
    else:
        print(True)
