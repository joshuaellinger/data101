#
# Python Primitives
# 

# integers contain 'whole' numbers
#   called 'int' or 'integer' by programmers
def example_integers():
 
    print(10)
    print(type(10))

    print(-10)
    print(1_000) # you can add an _ for readability where you would normally have a comma
    print(10 + 10) # add
    print(10 * 2) # multiple
    print(10 // 2) # integer divide (notice the two backslashs)
    print(10 / 3) # fractional divide
    print(10 % 2) # modulus / remainder
    print(8 * 2 + 2 * 2) # multiple happens before addition
    print(8 + (2 * 2) + 2) # parenthesis
    print(10 ** 2) # 10^2 -- raise 10 to the 2nd power


# 'fractional' or 'scientific' numbers
#   called 'float' or 'floating point' by programmer
def example_floats():
    print(10.0)
    print(type(10.0))
    print(10e3)
    print(10e-3)
    print(1_000.0)

    print(1 + 0.5) # int + float -> float

    print(5.5)
    print(10. * 1.5)
    print(10. / 2)
    print(10. / 3)

    print(1e-20)
    print(1e20)

    print(1.0 - 1e-15)
    print(1.0 - 1e-20)

# True/False flags
#   called 'bool' or 'boolean' by programmer
def example_bools():
    print(True)
    print(type(True))
    print(False)

    # case matters: true and false don't work

    print(not True)
    print(not False)

    print(False and False)
    print(False and True)
    print(True and True)
    print(False or False)
    print(True or False)
    print(True or True)

# A string is a list of letters (called characters)
#  called 'str' in code
def example_strs():

    print("Hi")
    print('Hi') # single quotes work too

    print(type("Hi"))

    # get the length of the string
    print(len("Hi"))
    print(len("Hello"))
    print(len("Hi "))   

    print("Hel" + "lo") # concats
    print("Hel" "lo") # you can leave out the plus sign
    print("Hello" * 3) # duplicates the string 

    # -- indexing and slicing
    # get the 1st character
    print("Hello" [0])

    # get the list character
    print("Hello" [-1])

    # get the middle characters
    print("Hello" [ 1:-1])

    # ----

    # print each char
    for ch in "Hello":
        print(ch)

    # embedded quotes
    print("Hello 'Friends'") 
    print('Hello "Friends"') 

    # use slash '\' to include special characters
    #   programs call this 'escaping' the following character
    print("Hello \"Friends\"") 

    #other special characters
    print("Hello\nGoodbye") # new line
    print("Hello\tGoodbye") # tab
    print("Hello\\Goodbye") # slash

    print("""
Hello
I
must
be
going""")

def example_conversions():

    print(str(10))
    print(str(10.0))
    print(str(True))

    print(int("10"))
    print(float("10.0"))
    print(bool("True"))

def run_all():
    example_integers()
    example_floats()
    example_bools()
    example_strs()
    example_conversions()

# run all the examples
run_all()