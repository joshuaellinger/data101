#
#  This short program tracks information about each student.
#

def load_students() -> list:
    "load the students from students.json"    
    # read the content of the file into a string
    f = open("students.json", "r")
    content = f.read()
    f.close()

    # if the file is empty, return an empty list
    if len(content) == 0: return []

    # parse it into a list 
    import json
    students = json.loads(content)
    return students


def save_students(students: list) -> None:
    "save the students to students.json"    
    
    # convert the list into a string 
    import json
    content = json.dumps(students, indent=4)

    # read the content of the files
    f = open("students.json", "w")
    f.write(content)
    f.close()


def find_student_by_name(students: list, name: str) -> dict:
    "lookup a student using the 'name' attribute"
    for s in students:
        if s["name"] == name: return s
    return None


def make_a_new_student(name: str, title: str, prior_experience: int) -> dict:
    "make a 'noob' student, recording how much prior experience they have"
    student = {
        "name": name,
        "title": title,
        "hours": [prior_experience,],
        "tasks":
        {
            "install dev-tools": False,
            "write and run hello-world": False,
            "check-in a change": False,
        },
        "knowledge":
        {
            "basic types: int, float, bool, str": "noob",
            "container types: list, dict": "noob",
            "variables": "noob",
            "functions": "noob",
        }
    }
    return student

# ===========================================================
def main():
    students = load_students()

    s = find_student_by_name(students, "Sam")
    if s == None:
        s = make_a_new_student("Sam", "Shady Riddler", 10)
        students.append(s)
        print("added a new student", s["name"], "the", s["title"])

    s = find_student_by_name(students, "Amelia")
    if s == None:
        s = make_a_new_student("Amelia", "Bedilia",2)
        s["hours"].append(4)
        s["hours"].append(3)        
        students.append(s)
        print("added a new student", s["name"], "the", s["title"])

    print("")
    print("The students are:")
    for s in students:

        # get the name and title into variables
        s_name, s_title = s["name"], s["title"]

        # compute the total hours from the hours list
        total_hours = 0
        for h in s["hours"]:
            total_hours += h
        
        # convert the list of hours into a list of strings
        hours_as_strs = [str(x) for x in s["hours"]]
        #print(hours_as_strs)

        # use a formated strings (f-string) to combine the name and the title
        full_name = f"{s_name} the {s_title}"

        # add extra spaces on the end so it is all the same length
        full_name_padded = full_name.ljust(25)

        if len(hours_as_strs) > 1:      
            # use a string function to join a the hours together
            # with a plus sign between them
            formated_hours_list = "+".join(hours_as_strs)

            print("  ", full_name_padded, ":",
                formated_hours_list, "=",
                total_hours, "hours.")
        else:
            print("  ", full_name_padded, ":",
                total_hours, "hours.")

    save_students(students)

    print()
    print("ROUND 3 - CODE")



main()


