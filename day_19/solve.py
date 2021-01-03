class Rule(object):
	def check(self, text):
		raise Exception("Not implemented")
	def generate(self):
		raise Exception("Not implemented")

class ConstRule(Rule):
	def __init__(self, rule_id, char):
		self.rule_id = rule_id
		self.char = char
	def check(self, text):
		#print(f"ConstRule({self.rule_id}) check: {self.char} == {text[0]} is {self.char == text[0]}")
		if len(text) == 0:
			return False, 0
		return self.char == text[0], 1
	def generate(self):
		return [self.char]

class SeqRule(Rule):
	def __init__(self, rule_id, db, rule_ids):
		self.rule_id = rule_id
		self.db = db
		self.rule_ids = rule_ids
	def check(self, text):
		index = 0
		#print(f"SeqRule({self.rule_id}) check: {self.rule_ids}, {text}")
		for rule_id in self.rule_ids:
			rule = self.db[rule_id]
			if index >= len(text):
				#print(f"SeqRule({self.rule_id}) result: (False, 0)")
				return False, 0
			is_match, consumed = rule.check(text[index:])
			if not is_match:
				#print(f"SeqRule({self.rule_id}) result: (False, 0)")
				return False, 0
			index += consumed
		#print(f"SeqRule({self.rule_id}) result: {(True, index)}")
		return True, index
	def generate(self):
		gens = [self.db[rule].generate() for rule in self.rule_ids]
		result = gens.pop()
		while len(gens) > 0:
			gen = gens.pop()
			new_res = []
			for result in result:
				for x in gen:
					new_res.append(x + result)
			result = new_res
		return result

class PipeRule(Rule):
	def __init__(self, rule_id, left, right):
		self.rule_id = rule_id
		self.left = left
		self.right = right
	def check(self, text):
		#print(f"PipeRule({self.rule_id}) check: ({self.left.rule_ids},{self.right.rule_ids}) {text}")
		is_match, consumed = self.left.check(text)
		if not is_match:
			is_match, consumed = self.right.check(text)
		#print(f"PipeRule({self.rule_id}) result: {(is_match, consumed)}")
		return is_match, consumed
	def generate(self):
		return self.left.generate() + self.right.generate()
		
def parse(filename):
	rule_defs, messages = tuple(map(lambda x: x.split("\n"), open(filename).read().strip().split("\n\n")))
	rules = {}
	for line in rule_defs:
		rule_number, rule_def = line.split(": ")
		#print(f"{rule_number}: {rule_def}")
		if "\"" in rule_def:
			rules[rule_number] = ConstRule(rule_number, rule_def.strip("\""))
			t = rule_def.strip("\"")
			#print(f"ConstRule({t})")
		elif "|" in rule_def:
			left, right = tuple(map(lambda x: tuple(x.split(" ")), rule_def.split(" | ")))
			#print(f"PipeRule(SeqRule({left}), SeqRule({right}))")
			rules[rule_number] = PipeRule(rule_number, SeqRule(f"{rule_number}_1", rules, left), SeqRule(f"{rule_number}_2", rules, right))
		else:
			#print(f"SeqRule({rule_def.split(' ')})")
			rules[rule_number] = SeqRule(rule_number, rules, tuple(rule_def.split(" ")))
	return rules, messages

def solution1(rules, messages):
	count = 0
	for message in messages:
		print(f"Beginning check for: {message}")
		is_match, consumed = rules["0"].check(message)
		print(f"Check result for {message}: {is_match}, {consumed}")
		if is_match and consumed == len(message):
			count += 1
	return count

def _chunk(text, size):
	return [text[i:i+size] for i in range(0, len(text), size)]

def match8(rules, text):
	size = len(rules["42"].generate()[0])
	if len(text) % size != 0:
		return False
	units = rules["42"].generate()
	return all([chunk in units for chunk in _chunk(text, size)])
		
def match11(rules, text):
	size = len(rules["42"].generate()[0])
	if len(text) % size != 0:
		return False
	chunks = _chunk(text, size)
	if len(chunks) % 2 != 0:
		return False
	unitsX = rules["42"].generate()
	unitsY = rules["31"].generate()
	return all([x in unitsX for x in chunks[:len(chunks)//2]]) and all([x in unitsY for x in chunks[len(chunks)//2:]])
		

def match0(rules, text):
	size = len(rules["42"].generate()[0])
	if len(text) % size != 0:
		return False
	for i in range(size, len(text), size):
		left, right = match8(rules, text[:i]), match11(rules, text[i:])
		if left and right:
			return True
	return False


def solution2(rules, messages):
	count = 0
	for message in messages:
		if match0(rules, message):
			count += 1
	return count

"""
print(solution1(*parse("sample.txt")))
print(solution1(*parse("input.txt")))
print(solution2(*parse("input2.txt")))
"""
print("ANSWER:", solution2(*parse("sample2.txt")))
print("ANSWER:", solution2(*parse("input2.txt")))

rules, messages = parse("sample2.txt")
print(set([len(x) for x in rules["42"].generate()]))
print(set([len(x) for x in rules["31"].generate()]))