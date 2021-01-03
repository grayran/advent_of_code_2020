from itertools import combinations
import functools

def parse(filename):
	numbers = sorted(list(map(int, open(filename).read().strip().split())))
	return [0] + numbers + [numbers[-1] + 3]

def solution1(numbers):
	diffs = {1: 0, 3:0}
	for i in range(len(numbers)-1):
		diff = numbers[i+1] - numbers[i]
		if diff == 1 or diff == 3:
			diffs[diff] += 1
		else:
			print(f"Sorted numbers list is wrong: {numbers}")
			raise Exception(f"Invalid diff {diff}")
	return diffs

def get_candidates(numbers, i):
	candidates = {1:[], 2:[], 3:[]}
	for j in range(i+1, len(numbers)):
		diff = numbers[j] - numbers[i]
		if diff > 3:
			return candidates
		candidates[diff].append(j)
		

@functools.lru_cache(maxsize=None)
def solution2(num_tuple):
	numbers = list(num_tuple)
	if len(numbers) == 0:
		return 0
	if len(numbers) == 1:
		return 1

	candidates = [numbers[x] for x in range(1, len(numbers)) if numbers[x] - numbers[0] <= 3]
	# print(f"candidates: {candidates}")

	trees = []
	for i in range(len(candidates)):
		trees.append(tuple(numbers[i+1:]))
		
	# print(f"Trees: {trees}")
	result = sum(map(solution2, trees))
	return result

print(solution1(parse("sample.txt")))
print(solution1(parse("sample2.txt")))
print(solution1(parse("input.txt")))

print(solution2(tuple(parse("sample.txt"))))
print(solution2(tuple(parse("sample2.txt"))))
print(solution2(tuple(parse("input.txt"))))