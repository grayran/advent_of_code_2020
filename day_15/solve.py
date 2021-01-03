def solution(seed, limit):
	count = len(seed)
	numbers = seed.copy()
	db = {}
	for i in range(len(numbers)-1):
		db[numbers[i]] = i

	while count < limit:
		if numbers[-1] not in db:
			numbers.append(0)
		else:
			next = count - db[numbers[-1]] - 1
			numbers.append(next)
		db[numbers[-2]] = count - 1
		count += 1
		# print(f"number: {numbers[-1]}")
	return numbers[-1]


print(solution([0,3,6], 2020))
print(solution([5,1,9,18,13,8,0], 2020))
print(solution([5,1,9,18,13,8,0], 30000000))

"""
assert solution([0,3,6], 30000000) == 175594
assert solution([1,3,2], 30000000) ==  2578
assert solution([2,1,3], 30000000) ==  3544142
assert solution([1,2,3], 30000000) ==  261214
assert solution([2,3,1], 30000000) ==  6895259
assert solution([3,2,1], 30000000) ==  18
assert solution([3,1,2], 30000000) ==  362
"""