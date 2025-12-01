# Given seq of Lx or Rx rotation
# Lx -> dec num by x
# Rx -> inc num by x
# Modulo 100 (0-99) dials


# part1 find number of times dial is at 0 after a rotation
def sol_p1():
    f = open("p1.txt", 'r')
    
    zero_count = 0
    pos = 50
    for l in f :
        rot = int(l[1:])
        if l[0] == 'L':
            rot = -rot

        pos = (pos + rot) % 100

        if (pos == 0):
            zero_count += 1



    return zero_count


# part 2 count num of times any click causes dial to point at 0.
def sol_p2():
    f = open("p1.txt", 'r')
    
    zero_count = 0
    pos = 50
    for l in f :
        x = 1
        rot = int(l[1:])
        if l[0] == 'L':
            x = -1
        for r in range(rot):
            pos = (pos + x) % 100
            if (pos == 0):
                    zero_count +=1
        



    return zero_count



def main():

    print(sol_p2())

main()

