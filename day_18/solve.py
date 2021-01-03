import string

class Exp(object):
	def evaluate(self):
		raise Exception("not implemented!")

class ConstExp(Exp):
	def __init__(self, val):
		self.val = int(val)
	def evaluate(self):
		return self.val

class AddExp(Exp):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs
	def evaluate(self):
		return self.lhs.evaluate() + self.rhs.evaluate()

class MulExp(Exp):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs
	def evaluate(self):
		return self.lhs.evaluate() * self.rhs.evaluate()

class ParenExp(Exp):
	def __init__(self, exp):
		self.exp = exp
	def evaluate(self):
		return self.exp.evaluate()

class Node(object):
	def __init__(self, operator, left, right):
		self.operator = operator
		self.left = left
		self.right = right

def find_nth(text, c, n):
	for i in range(len(text)):
		if x == c:
			n -= 1
		if n == 0:
			return i

def find_opening_paren(text):
	count = 0
	for i in range(len(text)-1, -1, -1):
		c = text[i]
		if c == ")":
			count += 1
		elif c == "(":
			if count == 0:
				return i
			count -= 1

def find_closing_paren(text):
	count = 0
	for i in range(len(text)):
		c = text[i]
		if c == "(":
			count += 1
		elif c == ")":
			if count == 0:
				return i
			count -= 1
			

def pre_parse(text):
	text = list(text.replace(" ", ""))
	index = 0
	while True:
		#print(f"{index}: {''.join(text)}")
		if index >= len(text):
			break
		if text[index] == "+":
			is_left_num, is_right_num = [text[x] in string.digits for x in (index-1, index+1)]
			if is_left_num and is_right_num:
				text = text[:index-1] + ["("] + text[index-1:index+2] + [")"] + text[index+2:]
				#print(f"both: {''.join(text)}")
			elif is_left_num:
				right_paren = index+2 + find_closing_paren(text[index+2:])
				text = text[:index-1] + ["("] + text[index-1:right_paren+1] + [")"] + text[right_paren+1:]
				#print(f"left: closing_paren: {right_paren} {''.join(text)}")
			elif is_right_num:
				left_paren = find_opening_paren(text[:index-1])
				text = text[:left_paren] + ["("] + text[left_paren:index+2] + [")"] + text[index+2:]
				#print(f"right: opening_paren: {left_paren} {''.join(text)}")
			else:
				right_paren = index+2 +find_closing_paren(text[index+2:])
				left_paren = find_opening_paren(text[:index-1])
				text = text[:left_paren] + ["("] + text[left_paren:right_paren+1] + [")"] + text[right_paren+1:]
				#print(f"neither: {''.join(text)}")
			index += 2
		else:
			index += 1
	return "".join(text)

def parse(text):
	text = text.replace(" ", "")	
	lookup = {"+": AddExp, "*": MulExp}
	lhs = None
	operator = ""
	parens = []
	for i in range(len(text)):
		c = text[i]
		if c in string.digits:
			exp = ConstExp(c)
			if operator in ("+", "*"):
				lhs = lookup[operator](lhs, exp)
			else:
				lhs = exp
			operator = ""
		elif c in ("+", "*"):
			operator = c
		elif c == "(":
			parens.append((lhs, operator))
			lhs = None
			operator = ""
		elif c == ")":
			exp = ParenExp(lhs)
			old_lhs, old_operator = parens.pop()
			if old_operator in ("+", "*"):
				lhs = lookup[old_operator](old_lhs, exp)
			else:
				lhs = exp
	return lhs

def follow(exp):
	res = []
	prev = exp.left
	while prev is not None:
		exp = prev
		prev = exp.left
	while exp is not None:
		if isinstance(exp, AddExp):
			res.append("AddExp")
		elif isinstance(exp, MulExp):
			res.append("MulExp")
		elif isinstance(exp, ConstExp):
			res.append(f"ConstExp({exp.val})")
		elif isinstance(exp, ParenExp):
			res.append("ParenExp")
		exp = exp.right
	return "->".join(res)
		
		
total = 0
for line in open("input.txt").read().strip().split("\n"):
	print(line)
	print(f"{pre_parse(line)}: {parse(pre_parse(line)).evaluate()}")
	total += parse(pre_parse(line)).evaluate()

print(sum([parse(pre_parse(line)).evaluate() for line in open("input.txt").read().strip().split("\n")]))
print("total", total)

"""
def test(text):
	print(f"{text}: {parse(pre_parse(text)).evaluate()}")

test("1 + (2 * 3) + (4 * (5 + 6))")
test("5 + (8 * 3 + 9 + 3 * 4 * 3)")
test("2 * 3 + (4 * 5)")
test("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
test("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
assert parse(pre_parse("1 + (2 * 3) + (4 * (5 + 6))")).evaluate() == 51
assert parse(pre_parse("2 * 3 + (4 * 5)")).evaluate() == 46
assert parse(pre_parse("5 + (8 * 3 + 9 + 3 * 4 * 3)")).evaluate() == 1445
assert parse(pre_parse("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")).evaluate() == 669060
assert parse(pre_parse("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")).evaluate() == 23340

"""