from collections import namedtuple

Policy = namedtuple("Policy", ["min", "max", "char"])

def solution1(records):
	counter = 0
	for policy, password in records:
		char_count = password.count(policy.char)
		if policy.min <= password.count(policy.char) <= policy.max:
			counter += 1
	return counter

def solution2(records):
	counter = 0
	for policy, password in records:
		char_count = password.count(policy.char)
		first_c = password[policy.min-1] == policy.char
		second_c = password[policy.max-1] == policy.char
		if first_c and second_c:
			continue
		if not first_c and not second_c:
			continue
		counter += 1
	return counter

def parse(raw_records):
	result = []
	for raw_record in raw_records:
		raw_policy, password = raw_record.split(": ")
		bounds, char = raw_policy.split(" ")
		mi, ma = map(int, bounds.split("-"))
		result.append((Policy(min=mi, max=ma, char=char), password))
	return result

print(solution1(parse(open("input.txt").read().strip().split("\n"))))
print(solution2(parse(open("input.txt").read().strip().split("\n"))))