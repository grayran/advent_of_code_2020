def solution1(groups):
	for group in groups:
		answers = "".join(group.split())
		yield len(set(answers))

def solution2(groups):
	for group in groups:
		group_answers = [set(answers) for answers in group.split()]
		common_answers = group_answers[0].intersection(*group_answers[1:]) if len(group_answers) > 1 else group_answers[0]
		print(f"all answers: {group.split()}")
		print(f"common answers: {common_answers}")
		yield len(common_answers)

print(sum(solution1(open("sample.txt").read().strip().split("\n\n"))))
print(sum(solution1(open("input.txt").read().strip().split("\n\n"))))

print(sum(solution2(open("input.txt").read().strip().split("\n\n"))))
print(sum(solution2(open("sample.txt").read().strip().split("\n\n"))))