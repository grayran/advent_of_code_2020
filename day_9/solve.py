def parse(filename):
	return list(map(int, open(filename).read().strip().split()))

def get_pair_sums(numbers):
	for i in range(len(numbers)):
		for j in range(i+1, len(numbers)):
			yield numbers[i] + numbers[j]

def solution1(numbers, trail):
	for i in range(trail, len(numbers)):
		candidates = set(get_pair_sums(numbers[i-trail:i]))
		# print(f"past {trail}: {numbers[i-trail:i]}")
		# print(f"candidates: {candidates}")
		if numbers[i] not in candidates:
			return numbers[i]

def solution2(numbers, trail):
	target = solution1(numbers, trail)
	for i in range(len(numbers)):
		for j in range(i+2, len(numbers)):
			series = numbers[i:j]
			if sum(series) == target:
				return min(series), max(series)


print(solution1(parse("sample.txt"), 5))
print(solution1(parse("input.txt"), 25))

print(sum(solution2(parse("sample.txt"), 5)))
print(sum(solution2(parse("input.txt"), 25)))