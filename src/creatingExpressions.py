from itertools import product
from os import mkdir


def create_cpp_file(s1, s2, s3):
    line0 = "#define ex GPR:$r\n"
    line1 = "#define gamma (SHYADD ex, ex)\n"
    line2 = "#define beta (SHXADD "
    line3 = "#define alpha (SHZADD "
    if s3[10:12] == s2[7:9]:
        line3 = line3 + "beta, "
        if s3[13:15] == s2[7:9]:
            line3 = line3 + "beta)\n"
        elif s3[13:15] == s1[7:9]:
            line3 = line3 + "gamma)\n"
        else:
            line3 = line3 + "ex)\n"
    elif s3[10:12] == s1[7:9]:
        line3 = line3 + "gamma, "
        if s3[13:15] == s2[7:9]:
            line3 = line3 + "beta)\n"
        elif s3[13:15] == s1[7:9]:
            line3 = line3 + "gamma)\n"
        else:
            line3 = line3 + "ex)\n"
    else:
        line3 = line3 + "ex, "
        if s3[13:15] == s2[7:9]:
            line3 = line3 + "beta)\n"
        elif s3[13:15] == s1[7:9]:
            line3 = line3 + "gamma)\n"
        else:
            line3 = line3 + "ex)\n"
    if s2[10:12] == s1[7:9]:
        line2 = line2 + "gamma, "
        if s2[13:15] == s1[7:9]:
            line2 = line2 + "gamma)\n"
        else:
            line2 = line2 + "ex)\n"
    else:
        line2 = line2 + "ex, "
        if s2[13:15] == s1[7:9]:
            line2 = line2 + "gamma)\n"
        else:
            line2 = line2 + "ex)\n"
    return line0 + line1 + line2 + line3 + "alpha"


class result:
    def __init__(self, line_one, line_two, line_three, expr):
        self.shxadd_1 = line_one
        self.shxadd_2 = line_two
        self.shxadd_3 = line_three
        self.expression = expr

    shxadd_1: str
    shxadd_2: str
    shxadd_3: str
    expression: str


variables = ["a0", "a1"]
res_strings: list[result] = []

"""
Each qmN can be a0 or a1 register
shXadd qm1 a0 a0
shYadd qm2 qm3 qm4
shZadd a0 qm5 qm6
"""
for qm1, qm2, qm3, qm4, qm5, qm6 in product(variables, repeat=6):
    a0 = "(2**x + 1)" if (qm1 == "a0") else "t"
    a1 = "(2**x + 1)" if (qm1 == "a1") else ""
    s1 = "shXadd " + qm1 + " a0 a0\n"
    isThereA1 = qm1 == "a1"
    if not (isThereA1 == False and (qm3 == "a1" or qm4 == "a1")):
        if qm3 == qm4:
            if qm3 == "a1":
                if qm2 == "a0":
                    a0 = a1 + "(2**y + 1)"
                else:
                    a1 = a1 + "(2**y + 1)"
            else:
                if qm2 == "a0":
                    a0 = a0 + "(2**y + 1)"
                else:
                    a1 = a0 + "(2**y + 1)"
        else:
            if qm3 == "a0":
                if qm2 == "a0":
                    a0 = "(" + a0 + "(2**y)" + " + " + a1 + ")"
                else:
                    a1 = "(" + a0 + "(2**y)" + " + " + a1 + ")"
            else:
                if qm2 == "a0":
                    a0 = "(" + a1 + "(2**y)" + " + " + a0 + ")"
                else:
                    a1 = "(" + a1 + "(2**y)" + " + " + a0 + ")"
        s2 = "shYadd " + qm2 + " " + qm3 + " " + qm4 + "\n"
        isThereA2 = isThereA1 == False and qm2 == "a1"
        isThereA1 = isThereA1 or (qm2 == "a1")
        if not (
            (isThereA1 == False and (qm5 == "a1" or qm6 == "a1"))
            or (isThereA2 and (qm5 == "a0" and qm6 == "a0"))
        ):
            s3 = "shZadd " + "a0 " + qm5 + " " + qm6 + "\n"
            if qm5 == qm6:
                if qm5 == "a0":
                    a0 = a0 + "(2**z + 1)"
                else:
                    a0 = a1 + "(2**z + 1)"
            else:
                if qm5 == "a0":
                    a0 = a0 + "(2**z)" + " + " + a1
                else:
                    a0 = a1 + "(2**z)" + " + " + a0
            res1 = result(s1, s2, s3, a0)
            res_strings.append(res1)

# Print all possible pattern
counter = 0
for x in res_strings:
    print(x.shxadd_1)
    print(x.shxadd_2)
    print(x.shxadd_3)
    print(x.expression)
    print("counter - " + str(counter) + "n")
    counter += 1

""" Pattern useless if it consist only of 2 bitmanips
Example: qm1 = am5 = am6 = a0, qm2 = am3 = qm4 = a1 """
useless_patterns = [5, 8, 12, 16, 20, 21, 22, 23, 24, 25, 29, 33]
counter = 0

""" Create directory for each unique pattern 
and file with python code to create tests for this pattern """
expr: list[str] = []
for x in res_strings:
    if x.expression not in expr:
        counter += 1
    if x.expression not in expr and counter not in useless_patterns:
        patternName = f"pattern{counter}"
        mkdir(patternName)
        wow = create_cpp_file(x.shxadd_1, x.shxadd_2, x.shxadd_3)
        f = open(f"{patternName}/forCpp.cpp", "w")
        f.write(wow)
        f.close()
        f = open(f"{patternName}/pattern", "w")
        f.write(x.shxadd_1 + x.shxadd_2 + x.shxadd_3)
        f.close()
        f = open(f"{patternName}/pythonCode", "w")
        code = (
            """from os import mkdir
tests_creating = []
print(\"shZ,shY,shM,res\")
for x in range(1,4):
    for y in range(1,4):
        for z in range(1,4):
            t = 1
            const = """
            + x.expression.replace(")(", ")*(").replace("t(", "t*(")
            + """
            if const not in tests_creating:
                print(x,y,z,const)
                tests_creating.append(const)
print(sorted(tests_creating))

mkdir(\"mulw\")
for x in tests_creating:
    fName = \"mulw/test\" + str(x) + \".c\"
    f = open(fName,\"w\")
    s = \"int test1(int x) { int z = \" + str(x) + \" * x; return z; }\"
    f.write(s)
    f.close()"""
        )
        f.write(code)
        f.close()
        expr.append(x.expression)
