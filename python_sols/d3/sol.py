# can turn on two batteries
# find largest joltage


def max_jolt_p1(bank: str) -> int:
    max_digit = max(bank[:-1])
    max_second = max(bank[bank.find(max_digit) + 1 :])
    jolt = int(max_digit) * 10 + int(max_second)
    return jolt


def sol_p1():
    f = open("data.txt", "r")
    res = 0
    for bank in f:
        bank = bank.strip()
        res += max_jolt_p1(bank)

    return res


## Can turn on 12 batteries
# max 12 digit number not nec. in sequence
# but digits come in "index" order

## Some shenanigans like if only 12 left just add them to jolt_arr


def max_jolt_p2(bank: str, length=12) -> int:
    to_drop = len(bank) - length
    stack = []
    for digit in bank:
        while to_drop > 0 and stack and stack[-1] < digit:
            stack.pop()
            to_drop -= 1
        stack.append(digit)

    return "".join(stack[:length])


def sol_p2():
    f = open("data.txt", "r")
    res = 0
    for bank in f:
        bank = bank.strip()
        jolt = int(max_jolt_p2(bank))
        # print(jolt)
        res += jolt
    return res


print(sol_p2())
