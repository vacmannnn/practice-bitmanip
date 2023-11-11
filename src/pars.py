import pathlib
from os import getcwd, mkdir

set_of_passed_tests: set[int] = set()
set_of_failed_tests: set[int] = set()
'''
c1 - default Clang
c2 - patched Clang
c3 - defaule GCC for RISC-V
'''
c1 = "clang++-17"
c2 = "clang"
c3 = "riscv64-unknown-linux-gnu-gcc"
nameOfCompiler = c3
desktop = pathlib.Path(getcwd())
for dirpath in desktop.iterdir():
    if dirpath.is_dir() and dirpath.name != "mulw":
        f = open(f"{dirpath}/{nameOfCompiler}.csv", "r")
        for x in f:
            if "test" in x and "passed" in x:
                for z in x.split(","):
                    if z.startswith("test"):
                        set_of_passed_tests.add(int(z[4 : len(z)]))
            if "test" in x and "failed" in x:
                for z in x.split(","):
                    if z.startswith("test"):
                        set_of_failed_tests.add(int(z[4 : len(z)]))
        f.close()
print("compiler -", nameOfCompiler, "\n")
print(
    f"passed - {sorted(set_of_passed_tests)}\ncan't optimize - {len(set_of_passed_tests)}\n"
)
print(f"failed - {sorted(set_of_failed_tests)}\ncan optimize - {len(set_of_failed_tests)}")

# mkdir("mulw")
# for testNumber in set_of_passed_tests:
#     f = open("mulw/testZ.c".replace("Z",str(testNumber)),"w")
#     f.write("#include <stdint.h>\nint test1(int x) { int z = " + str(testNumber) + " * x; return z; }")
#     f.close()
