def solution1(numbers):
	for i in range(len(numbers)):
		for j in range(i, len(numbers)):
			if numbers[i] + numbers[j] == 2020:
				return numbers[i] * numbers[j]
	raise Exception("Can't find numbers :/")

def solution2(numbers):
	numbers = sorted(numbers)
	def _find_sum(ignored_indices, total, operand_count):
		if operand_count == 1:
			for i in range(len(numbers)):
				if i not in ignored_indices and numbers[i] == total:
					return [i]
			return False
		for i in range(len(numbers)):
			result = _find_sum(ignored_indices + [i], total - numbers[i], operand_count-1)
			if result:
				return result + [i]
		return False
	
	indices = _find_sum([], 2020, 3)
	result = 1
	for index in indices:
		result *= numbers[index]
	return result
	

numbers = list(map(int, open("input.txt").read().strip().split("\n")))

print(solution2(numbers))