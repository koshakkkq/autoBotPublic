def is_float(element):
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def buatify_int(n):
    s = str(n)
    s = s[::-1]
    res = ''
    for i in range(0,len(s)):
        if i % 3 != 0 or i == 0:
            res += s[i]
        else:
            res += ' ' + s[i]
    return res[::-1]

