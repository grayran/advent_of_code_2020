import operator
from functools import reduce

def parse(filename):
	text = open(filename).read().strip().split()
	return int(text[0]), [int(x) for x in text[1].split(",") if x != "x"]

def solution1(earliest, buses):
	return operator.mul(*min(map(lambda x: (x - earliest % x, x), buses)))

def parse2(text):
	return [int(x) if x != "x" else x for x in text.split(",")]

def gcd(a, b):
	bigger = max(a,b)
	smaller = min(a, b)
	remainder = bigger % smaller
	while remainder != 0:
		bigger = max(smaller, remainder)
		smaller = min(smaller, remainder)
		remainder = bigger % smaller
	return smaller

def inv(a, m) : 
	m0 = m 
	x0 = 0
	x1 = 1
	if (m == 1) : 
		return 0
	while (a > 1) : 
		q = a // m 
		t = m 
		m = a % m 
		a = t 
		t = x0 
		x0 = x1 - q * x0 
		x1 = t 
	if (x1 < 0) : 
		x1 = x1 + m0 
	return x1

def solution2(buses):
	constraints = [(buses[i] - i, buses[i]) for i in range(len(buses)) if buses[i] != "x"]
	prod = reduce(operator.mul, [x for x in buses if x != "x"])
	result = 0
	for remainder, divisor in constraints:
		pp = prod // divisor
		# print(f"remainder: {remainder}, divisor: {divisor}, pp: {pp}, inv: {inv(pp, divisor)}")
		result = result + remainder * inv(pp, divisor) * pp 
	return result % prod

# print(solution1(*parse("sample.txt")))
# print(solution1(*parse("input.txt")))

print(solution2(parse2("17,x,13,19")))
assert solution2(parse2("17,x,13,19")) == 3417
assert solution2(parse2("67,7,59,61")) == 754018.
assert solution2(parse2("67,x,7,59,61")) == 779210.
assert solution2(parse2("67,7,x,59,61")) == 1261476.
assert solution2(parse2("1789,37,47,1889")) == 1202161486.

print(solution2(parse2(open("sample.txt").read().split("\n")[1])))
print(solution2(parse2(open("input.txt").read().split("\n")[1])))