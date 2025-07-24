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

    s = find_student_by_name(students, "Ruby")
    if s == None:
        s = make_a_new_student("Ruby", "CAPCOM", 10)
        students.append(s)
        print("added a new student", s["name"], "the", s["title"])

    print("")
    print("The students are:")
    for s in students:
        total=0
        for hours in s["hours"]:
            total=total+hours
        print("  ", s["name"], "the", s["title"],"has", total, "hours")

    save_students(students)

    print()
    print("ROUND 2 - CODE")



main()


