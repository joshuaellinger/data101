import code

class TutorialBot:
    def __init__(self):
        self.repl = code.InteractiveConsole()

    def print(self, message: str) -> None:
        lines = message.strip().split("\n")
        if len(lines) == 1:
            print(f"[Bot: {lines[0]}]")
        else:
            print("[Bot:")
            for s in lines:
                print("   " + s)
            print("")
            print("Press the '<enter>' key to continue")
            print("]")

            _ = self.repl.raw_input()

    def single_command(self, prompt: str, *, verbose=False) -> bool:
        while True:

            try:
                if prompt == "":
                    cmd = self.repl.raw_input(f">>> ")
                else:
                    cmd = self.repl.raw_input(f"[Bot: {prompt}]\n>>> ")
                while cmd.strip() == "": 
                    cmd = self.repl.raw_input(f">>> ")
            except KeyboardInterrupt as ex:
                print("[Bot. You typed ^C.  Bye.]")
                return True

            if cmd == "done":
                return True

            if cmd.replace(" ", "") == "'exit'" or cmd.replace(" ", "") == "'exit()'":
                print("[Bot: By surrounding the exit command with quotes, you turned it into a string]")
                print("[Bot: Type exit() instead of 'exit()']")
                continue

            if verbose: print(f"[Bot: You typed: '{cmd}']")

            if cmd.strip() == "exit":
                print("[Bot: exit is a built-in system function to exit a program]")
                print("[Bot: To call/evoke a function you have to give type '()' after the function name]")
                print("[Bot: So type exit() instead of exit]")
                continue

            if cmd.lower().strip() == "exit":
                print("[Bot: Python is case-sensitive, type exit() instead of Exit()]")
                continue

            if cmd.lower().strip() == "exit()":
                print("[Bot: continuing to next step]")
                return True

            try:
                result = self.repl.compile(cmd)
                if result == None: 
                    print("[Bot. You typed an incomplete command]")
                    continue
            except SyntaxError as ex:
                print("[Bot. Your code had an error.  Look at the error message below and try again]")
                print(ex.msg)
                continue
                
            if verbose: print(f"[Bot: You typed a command with valid syntax.  Now, I am going to evaluate it and print the result.]")
            try:
                exec(result)
            except SystemExit:
                print(f"[Bot: You called the exit command, which tells python to stop running.]")
                return True
            except Exception as ex:
                print("[Bot: The syntax was valid but the code had an error.  Read the message below and try again]")
                print(type(ex).__name__ + ": " + ", ".join(ex.args))
                continue

            break

        return False
    
    def multiple_commands(self, cmds: str) -> bool:
        lines = cmds.strip().splitlines()
        for cmd in lines:
            cmd = cmd.strip()
            if cmd == "": continue
            if cmd.starts("#"):
                print(f"[Bot: {cmd[1:].strip()}]")
            else:
                parts = cmd.split("#")
                done = self.single_command(parts[0])
                if done: return done
                if len(parts) > 1:
                    print(f"[Bot: {parts[1].strip()}]")


def step_1(bot: TutorialBot) -> None:

    print("==== step 1: algebra commands")

    done = bot.single_command("Type an alegbra expression, like 1+2, then press the <enter> key", verbose=True)
    if done: return 
    done = bot.single_command("Type an more complex alegbra expression, then press <enter>", verbose=True)
    if done: return 

    print("[Bot: Now keep typing commands, followed by <enter>, until you get bored.]")
    print("[Bot: When you get bored, type exit() and then <enter>]")
    cnt, prompt = 0, "Type an algebra expression, or exit()"
    while True:
        done = bot.single_command(prompt)
        if done: break
        cnt += 1
        if cnt == 3:
            print("[Bot: I'm going to be quiet now.  remember to type exit() when done]") 
            prompt = ""

def step_2(bot: TutorialBot) -> None:

    bot = TutorialBot()

    print("==== step 2: primitive types")
    smt = """
Python has four main primitive data types.

1. Whole numbers (called int) are numbers like 10, 0, -10.

2. Scientific/Fractional Numbers (called float) are numbers like 1.5 and 1e10. They
behave very differently from int. The term 'float' is short for floating point.
They use a 'floating' decimal point so they can store very large numbers 
(like 1.5e30) and very small number (1.5e-30).

3. Strings (called str) are a list of characters like 'abc'.  They are enclosed by
single quotes (') or double quotes (").

4. Boolean (called bool) are a yes/no or True/False variable.

In python, you can get the type of something, using the built-in function called type().
"""
    bot.print(smt)

    bot.print("I am going to ask you to type a series of commands to help you understand each type")
    bot.print("You can hit up-arrow to get the previous command")
    bot.print("Type exit() if you want to stop early")
    bot.print("When I say 'Enter X', just type X followed by the <enter> key")

    step_2_type(bot)
    step_2_int(bot)
    step_2_float(bot)
    step_2_str(bot)

def step_2_type(bot: TutorialBot):
    print("    [subtopic: type() function]")
    bot.print("Let's learn about the built-in type function")
    done = bot.single_command("Enter type(10) # 10 is an 'int'")
    if done: return

    bot.print("Technically, the type() function returns a 'class' object with the name 'int' ")
    done = bot.single_command("Enter type(10).name # just print the name of the type")
    if done: return

    done = bot.multiple_commands("""
type(10.0)
type('abc')
type(True)
""")
    if done: return
    
    bot.print("10.0 is a 'float', 'abc' is a 'str', True is 'bool'")

def step_2_int(bot: TutorialBot):
    print("    [subtopic: int]")
  
    bot.print("Now let's look at int a little more")
    done = bot.single_command("Enter 1_000 # you can add an _ for readability where you would normally have a comma")
    if done: return

    done = bot.single_command("Normal operations work expected. Type something like 2 * 10 + 5")
    if done: return

    bot.print("But there are a few oddities.")
    done = bot.multiple_commands("""
3/2 # Even though both inputs are int, it returns 1.5
type(3/2) # And the type is float

# Use two backslashs to do integer division
3//2 # you get 1 (rounds down)
type(3//2) # you get an int

5%2 # modulus / remainder
10**3 # exponent - raise 10 to the 3rd power
""")
    if done: return
    



def step_2_float(bot: TutorialBot):
    print("    [subtopic: float]")

    done = bot.multiple_commands_command("""
1.5
1.5e1 # this is the same as 15.0 or 1.5 * (10**1)
1.5e-1 # this is the same as 0.15 or 1.5 * (10**-1)
1 + 0.5 # adding an int to a float works
""")

    done = bot.single_command(f"Enter 1.5e0 to start")
    for i in range(0, -7, -1):
        done = bot.single_command(f"Hit up-arrow then change the {i-1} to {i}")
        if done: return
    bot.print("Each step makes the result smaller by a factor of 10")
    bot.print("After a while, it starts printing in 'scientific format'")

def step_2_str(bot: TutorialBot):
    print("    [subtopic: str]")

    bot.print("Strings are a big topic.  This is just start.")

    done = bot.multiple_commands("""
'Hi'
"Hi" # double quotes work too
len('Hi') # built-in len function, len = 2
len('Hello') # len = 5
len('Hi ') # it counts the spaces so len = 3
'Hel' + 'lo' # concats
'Hel' 'lo' # you can leave out the plus sign
Enter 'Hello ' * 3 # duplicates the string

# Here is how getting parts of a string work
# It's called indexing and slicing
# get the 1st character
"Hello" [0]

# get the list character
"Hello" [-1]

# get the middle characters
"Hello" [ 1:-1]

# Here are some random string functions
"abc".upper()
"ABC".lower()
"abc".capitalize()
" abc ".strip()
""")
    


def main():

    bot = TutorialBot()
    bot.print("""
Hello.  I am CodingBot here to help you learn how to code.
                           
I am going to ask you to type a series of commands.
You can do as I ask or type something different check your understanding.
Whatever you type will be evaluated as Python code.
I will try to give you helpful hints as we go.
"""
    )

    #step_1(bot)
    step_2(bot)
    


main()