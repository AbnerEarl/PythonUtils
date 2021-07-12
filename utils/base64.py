import re

base_tbl = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"
alphabet = dict(zip(base_tbl, range(len(base_tbl))))
pattern = b"[A-Za-z\d+/]{2,4}={0,2}"
regex = re.compile(pattern)


def decode(src):
    ret = bytearray()
    length = len(src)
    step = 4
    if length % step:
        return
    for offset in range(0, length, step):
        end = offset + step
        block = src[offset:end]
        if end == length and not regex.fullmatch(block):
            return
        tmp = 0
        for i, c in enumerate(reversed(block)):
            # index = base_tbl.find(c)
            index = alphabet.get(c)
            if index:
                tmp += index << (i * 6)
            elif index == 0:
                pass
            else:
                if end != length:
                    return
        ret.extend(tmp.to_bytes(3, "big"))
    return bytes(ret)


print(decode(b"YWJj"))
