from typing import List, Tuple

# ----------------------------------------------------------------------------------------
# when declaring functions
#                v -- this is the argument list
#                      v -- this is the turn
def func_no_args( ) -> None:
    print("no args, not return")

# WARNING: return types in python are on the right side of the declaration
# In C-family languages (C/C++/Java/C#) the returns types are left size of the declartion
# This same function in C would be:
#    void func_no_args() {}


# ----------------------------------------------------------------------------------------
#                        v -- this is an 'argument'
#                             it creates a new variable and assigns the value passed into the function
def func_scalar_no_types(x):
    print(f"passed in {x}")
    x += 10
    print(f"local copy of x is now {x}")
    return x # return x

# This same function in C would be:
#    int func_scalar_no_types() { return x; }

# ----------------------------------------------------------------------------------------
#                v -- this is an optional type-hint.  it tells VS studio that you expect an int
#                         v -- this is the option return type-hint that you expect to return an int       
def func_scalar(x:int) -> int:
    print(f"passed in {x}")
    x += 10
    print(f"local copy of x is now {x}")
    return x 

# ----------------------------------------------------------------------------------------
#                v -- this is an argument list with two variables
#                                  v -- this is the type hint that you are returning two values
def func_scalar2(x:int, y: int) -> Tuple[int, int]:
    print(f"passed in {x, y}")
    x, y = x+10, y+11
    # same as:
    #    x += 10 or x = x + 10
    #    y += 11 or y = y + 11

    # x,y += (10,11) probably doesn't work

    print(f"local copy of x is now {x}")
    print(f"local copy of y is now {y}")
    return x,y
    # same as
    #   return (x,y)

# ----------------------------------------------------------------------------------------
# this is an example that takes a list as input ( an 'argument') and returns it as output
def func_list(items:List[int]) -> List[int]:
    print(f"passed in {items}")
    items[0] = 10
    print(f"items is now {items}")
    return items

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
def example_simple_functions():
    
    # returns none
    print(func_no_args())

    # passes a copy of x into the function. 
    # returns an int and assigns it to a new variable called z
    x = 1
    z = func_scalar(x)
    print(f"x is still {x} but z = {z}")

    # passes a copy of the constant 1 into the function
    z = func_scalar(1)

    # this doesn't work because the function returns a value (1)
    # and you can't assign the value of z to a constant
    #
    try:
        func_scalar(1) = z
    except Exception as ex:
        print("bad assignment")
        

    a = func_scalar2(1,2)
    print(a) # returns a tuple so this works
    print(a[0], a[1]) # this works

    # assigns the returned tuple to two new variables 
    x,y = func_scalar2(1,2)

def example_shallow_copy():

    # make a list and make a copy of it
    items = [3,4,5,6]
    items2 = items.copy()

    # Everything gets passed using a 'shallow' copy.  This is called call-by-value
    # 
    # This means that, unlike primitives, you can modify a container object
    # and the changes are retained after the function returns.
    print("before ", items)
    items3 = func_list(items)
    print("after (items)", items)
    print("after (items2)", items2)

    # but item3 is still considered the same object because it points to the same
    # container.
    print("Same List (items vs items2)?", items == items2)
    print("Same List (items vs items3)?", items == items3)


def main():
    example_simple_functions()
    example_shallow_copy()
    