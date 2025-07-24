# variables and control structures


def basic_variables():
    
    # set a variable named x to a value of 10
    x = 10
    print(x)

    # set another variable named y to a value of 15
    y = 15
    print(y)

    # replace the value with a new value of 20
    x = 20
    print(x)
    
    # add the value of x and y and store it in x
    x = x + y
    print(x)

    # do it again with shortcut notation
    x += 20
    print(x)

def dynamic_types():

    # other languages like C/C++ make you declare variables up front
    # they also make you choose one type and stick to it. 
    
    # Python doesn't care... 

    # define a variable as int
    x = 10
    print(x, type(x))

    # change it to a str
    x = "hi"
    print(x, type(x))

    # you can give python a 'hint' about the type
    x: int = 20
    print(x, type(x))

    # but it still lets you change it
    x = "hi" 
    print(x, type(x))

# pass in a value called x and a value called y.
#    give the user a 'hint' that you expect an int and a str
#    return a str
def sample_function(x: int, y: str) -> str:
    print(x, type(x))
    print(y, type(y))
    x = x + 10
    return str(y) + " there"

def basic_variable_passing():

    # you pass values into a functon in the 'argument' list
    #   that's everything between the ()
    sample_function(5, "hi")

    # the variable name in the caller doesn't have to be the same
    z = 20
    sample_function(z, "hi")
    # it's value doesn't change because it makes a copy before passing it in
    print(z)

    # you can use the 'return' value any other expresssion
    print(sample_function(z, "hi"))
    s = sample_function(z, "hi")
    print(s)
    
def basic_scope():

    # the variables in the outer function ('basic_scope')
    # are completely separate from the varaibles 
    # in the inner function (sample_function)
    x = 10
    y = "hi"
    print("x in outer function", x)
    sample_function(x, y)
    print("x in outer function is still", x)

def main():
    basic_variables()
    dynamic_types()

    sample_function(5, "hi")
    basic_variable_passing()
    basic_scope()


main()