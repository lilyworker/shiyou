s,k  = input('Input: ').split()
k = int(k)

res = ''
for i, ch in enumerate(s):
    res += '-' if ch in s[max(0, i-k): i] else ch
print(res)