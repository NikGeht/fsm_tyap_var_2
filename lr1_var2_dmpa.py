import numpy as np

alpha = [("abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ", None), ("0123456789", None), (" ", None),
         ("=", None), ("(", None), (")", "+"), ("+*", None), (".", None), ("eE", None), ("+-", None), ("\1", None)]


states = [*range(0, 12, 1)]

actions = [
    [(1, None), (-1, None), (-1, None), (-1, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(1, None), (1, None), (2, None), (3, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(-1, None), (-1, None), (2, None), (3, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(5, None), (7, None), (4, None), (-1, None), (6, '+'), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(5, None), (-1, None), (4, None), (-1, None), (6, '+'), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(5, None), (5, None), (-1, None), (-1, None), (-1, None), (12, None),
     (3, None), (-1, None), (-1, None), (-1, None), (50, "HALT")],
    [(5, None), (7, None), (-1, None), (-1, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(-1, None), (7, None), (-1, None), (-1, None), (-1, None), (12, None),
     (3, None), (8, None), (9, None), (-1, None), (50, "HALT")],
    [(-1, None), (8, None), (-1, None), (-1, None), (-1, None), (12, None),
     (-1, None), (-1, None), (9, None), (-1, None), (50, "HALT")],
    [(-1, None), (8, None), (-1, None), (-1, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (10, None), (-1, None)],
    [(-1, None), (11, None), (-1, None), (-1, None), (-1, None), (-1, None),
     (-1, None), (-1, None), (-1, None), (-1, None), (-1, None)],
    [(-1, None), (11, None), (-1, None), (-1, None), (-1, None), (12, None),
     (3, None), (-1, None), (-1, None), (-1, None), (50, "HALT")],
    [(-1, None), (11, None), (-1, None), (-1, None), (-1, None), (-1, None), (3, None), (-1, None), (-1, None), (-1, None), (50, "HALT")]]

state = 0
stack = []
name = ""
leksem = []


def get_action(curr_state, character):
    global name
    global stack
    global state
    global leksem
    key = 0
    i = 0
    while True:
        if curr_state == 8 or curr_state == 7 or curr_state == 9:
            if str(alpha[curr_state][0]).find(character) != -1:
                key = curr_state
                break
            elif str(alpha[curr_state + 1][0]).find(character) != -1:
                key = curr_state + 1
                break
        if character in alpha[i][0]:
            key = i
            break
        i = i + 1
        if i > len(alpha):
            break

    if key == -1:
        print("Character not found in the alphabet")
        return -1

    if actions[curr_state][key][0] != -1:
        stack_ch = actions[curr_state][key][1]
        if stack_ch != None and stack_ch != "HALT":
            stack.append(stack_ch)
        if key == 0 or key == 1 or key == 7 or key == 8 or key == 9:
            name += character
        elif key == 3 or key == 4 or key == 6:
            if name != "":
                leksem.append(name)
                name = ""
            leksem.append(character)
        elif key == 2:
            pass
        elif key == 5:
            if len(stack) > 0:
                stack.pop()
                if name != "":
                    leksem.append(name)
                name = ""
                leksem.append(character)
            else:
                print("Actions not allowed for this state and character:{} {}", curr_state, character)
                return -1
        state = actions[curr_state][key][0]

        if key == 10:
            if len(stack) == 0 and state == 50:
                if name != "":
                    leksem.append(name)
                name = ""
            else:
                print("Warning: stack is not empty or state is not HALT")
                return -1


input_file = open("input.txt", "r")
output_file = open("output.txt", "w")

text = input_file.read()
text += "\1"

for char in text:
    print(char)
    if (get_action(state, char) == -1):
        print("ERROR")
        break
output_file.write("TABLE OF NAMES:\n")
for elem in leksem:
    if str(elem)[0].isdigit():
        if str(elem).find(".") == -1:
            output_file.write(str(elem) + " - integer constant\n")
        else:
            output_file.write(str(elem) + " - float constant\n")
    if str(elem)[0].isalpha():
        output_file.write(str(elem) + "- variable\n")
output_file.write("LEKSEMS: \n" + str(leksem) + "\n")


def get_code():
    var_mass = []
    opr_mass = []
    all_operators = ["=", "+", "*", "(", ")"]
    level = 1
    code = ""
    while len(leksem) != 0:
        if leksem[0] in all_operators:
            if len(opr_mass) != 0:
                if opr_mass[-1] == "*" and leksem[0] == "+":
                    while opr_mass[-1] == "*":
                        code = var_mass[-1] + "\nSTORE $" + \
                            str(level) + "\nLOAD " + \
                            var_mass[-2] + "\nMPY $" + str(level)
                        level = level + 1
                        var_mass.pop()
                        var_mass.pop()
                        var_mass.append(code)
                        opr_mass.pop()
                if leksem[0] == ")":
                    while opr_mass[-1] != "(":
                        if opr_mass[-1] == "*":
                            code = var_mass[-1] + "\nSTORE $" + str(
                                level) + "\nLOAD " + var_mass[-2] + "\nMPY $" + str(level)
                            level = level + 1
                        else:
                            code = var_mass[-1] + "\nSTORE $" + str(
                                level) + "\nLOAD " + var_mass[-2] + "\nADD $" + str(level)
                            level = level + 1
                        var_mass.pop()
                        var_mass.pop()
                        var_mass.append(code)
                        opr_mass.pop()
                    opr_mass.pop()
            if leksem[0] != ")":
                opr_mass.append(leksem[0])
            leksem.remove(leksem[0])
        else:
            var_mass.append(leksem[0])
            leksem.remove(leksem[0])
    while len(opr_mass) != 0:
        if opr_mass[-1] == "*":
            code = var_mass[-1] + "\nSTORE $" + \
                str(level) + "\nLOAD " + var_mass[-2] + "\nMPY $" + str(level)
            level = level + 1
        if opr_mass[-1] == "+":
            code = var_mass[-1] + "\nSTORE $" + \
                str(level) + "\nLOAD " + var_mass[-2] + "\nADD $" + str(level)
            level = level + 1
        if opr_mass[-1] == "=":
            code = "LOAD " + var_mass[-1] + "\nSTORE " + var_mass[0]
        var_mass.pop()
        var_mass.pop()
        var_mass.append(code)
        opr_mass.pop()

    return var_mass


def oprimize_code(code):
    opt_code = str(code).split("\n")
    optimized = True

    while optimized:
        optimized = False
        i = 0
        while len(opt_code) > i + 2:

            op1 = opt_code[i].split(" ")
            op2 = opt_code[i + 1].split(" ")
            op3 = opt_code[i + 2].split(" ")
            if op1[0] == "STORE" and op2[0] == "LOAD" and (op3[0] == "ADD" or op3[0] == "MPY"):
                if op1[1] == op3[1]:
                    opt_code[i + 2] = op3[0] + " " + op2[1]
                    opt_code = opt_code[:i] + opt_code[i + 2:]
                    optimized = True
            elif op1[0] == "LOAD" and op2[0] == "STORE" and op3[0] == "LOAD":
                j = i + 3

                while not opt_code[j].endswith(op2[1]):
                    j = j + 1

                X = opt_code[j][:4]
                opt_code[j] = X + " " + str(op1[1])

                opt_code = opt_code[:i] + opt_code[i + 2:]
                optimized = True
            i = i + 1

    return opt_code


raw_code = get_code()
raw_code = str(raw_code[0])
output_file.write("RAW CODE:\n" + str(raw_code))
optimized_code = oprimize_code(raw_code)
output_file.write("\nOPTIMIZED CODE:\n")
for count in optimized_code:
    output_file.write(str(count) + "\n")
