def parse(filename):
	lines = open(filename).read().strip().split("\n")
	instructions = []
	for line in lines:
		code, arg = line.split()
		instructions.append((code, int(arg)))
	return instructions

def _execute(code, arg, acc, ic):
		if code == "jmp":
			return acc, ic+arg
		elif code == "acc":
			return acc+arg, ic+1
		return acc, ic+1

def solution1(instructions):
	db = [False for i in range(len(instructions))]
	acc, ic = 0, 0
	while True:
		if ic == len(instructions):
			return True, acc, ic, db
		elif ic > len(instructions) or ic < 0:
			return False, acc, ic, db
		instr = instructions[ic]
		if db[ic]:
			# print(f"Stopped at line number {ic}: {instr[0]} {instr[1]}")
			return False, acc, ic, db
		db[ic] = True
		acc, ic = _execute(*instr, acc, ic)

def solution2(instructions):
	_, acc, ic, db = solution1(instructions)
	for i in range(len(db)):
		if instructions[i][0] == "acc":
			continue
		if instructions[i][0] == "jmp":
			instructions[i] = ("nop", instructions[i][1])
			original = "jmp"
		else:
			instructions[i] = ("jmp", instructions[i][1])
			original = "nop"
		halts, acc, ic, db = solution1(instructions)
		instructions[i] = (original, instructions[i][1])
		if halts:
			print(f"Fixing line {ic}: {instructions[i][0]} {instructions[i][1]} halts the code.")
			return acc
			

print(solution1(parse("sample.txt"))[1])
print(solution1(parse("input.txt"))[1])

print(solution2(parse("sample.txt")))
print(solution2(parse("input.txt")))