
def example_if():

    x = 10
    if x == 10: # notice the double equals
        print("x = 10")

    if x < 10: # notice the double equals
        print("x != 10")
    if x > 10: # notice the double equals
        print("x != 10")
    if x <= 10: # notice the double equals
        print("x >= 10")
    if x >= 10: # notice the double equals
        print("x <= 10")

    # these tests are equivalent
    if not (x == 10): 
        print("not (x == 10)")
    if x != 10:
        print("x != 10")

    if x < 10:
        print(" x < 10")
    elif x > 10:
        print(" x > 10")
    else:
        print(" x = 10")

def example_loops():

    # print 0 to 4
    for i in range(5):
        print(i)

    # print 0 to 4 (same as above)
    i = 0
    while i < 5:
        print(i)
        i = i + 1

    # print 0 to 4 (same as above)
    i = 0
    while True:
        print(i)
        i = i + 1
        if i >= 5: break

    # print in reverse
    for i in range(10, 0, -2):
        print(i)

    # print in reverse (same as above)
    i = 10
    while True:
        print(i)
        i = i - 2
        if i <= 0: break

    # only print 5
    for i in range(0, 10):
        if i != 5: continue # skip to the top of the loop
        print(i)


def main():
    example_if()
    example_loops()

main()