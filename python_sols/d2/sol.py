# p1
# invalid ids st:
# only made up of repeated sequences
# calc all invalid ids
def inv_id_p1(id: int) -> bool:
    # get every digit split check if d+d = id
    id = str(id)
    id_len = len(id)
    base = id_len // 2
    left, right = id[base:], id[:base]
    if left == right:
        return True

    return False


def p1():
    data = open("data.txt", "r")
    inv = 0
    for l in data.readline().split(","):
        left, right = l.split("-")
        left = int(left)
        right = int(right)
        for i in range(left, right + 1):
            if inv_id_p1(i):
                inv += i
    return inv


def inv_id_p2(id: int) -> bool:
    """
    invalid ids have repeated strings of atleast 2
    """
    id = str(id)
    id_len = len(id)

    for index in range(1, id_len):
        parts = [id[i : i + index] for i in range(0, len(id), index)]
        if len(parts) > 1 and len(set(parts)) == 1:
            return True
    return False


def p2():
    data = open("data.txt", "r")
    inv = 0
    for l in data.readline().split(","):
        left, right = l.split("-")
        left = int(left)
        right = int(right)
        for i in range(left, right + 1):
            if inv_id_p2(i):
                inv += i
    return inv


print(p2())
