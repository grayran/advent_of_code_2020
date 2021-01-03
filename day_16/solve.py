def parse(filename):
	text = open(filename).read().strip().split("\n\n")
	rules = []
	for line in text[0].split("\n"):
		field = line.split(":")[0]
		bounds_text = line.split(":")[1].strip().split(" or ")
		bounds = [tuple(map(int, x.split("-"))) for x in bounds_text]
		rules.append((field, *bounds))
	my_ticket = tuple(map(int, text[1].split("\n")[1].split(",")))
	nearby_tickets = list(map(lambda x: tuple(map(int, x.split(","))), text[2].split("\n")[1:]))
	return rules, my_ticket, nearby_tickets

def is_valid(rules, number):
	for field, bound1, bound2 in rules:
		if bound1[0] <= number <= bound1[1] or bound2[0] <= number <= bound2[1]:
			return True
	return False

def solution1(rules, tickets):
	invalids = []
	for ticket in tickets:
		for field in ticket:
			if not is_valid(rules, field):
				invalids.append(field)
	print(f"invalids: {invalids}")
	return sum(invalids)

def field_matches(rule, values):
	name, bound1, bound2 = rule
	return all([bound1[0] <= x <= bound1[1] or bound2[0] <= x <= bound2[1] for x in values])

def solution2(rules, my_ticket, tickets):
	valid_tickets = []
	for ticket in tickets:
		if all([is_valid(rules, x) for x in ticket]):
			valid_tickets.append(ticket)

	field_values = []
	for i in range(len(my_ticket)):
		field_values.append([])
		for ticket in valid_tickets:
			field_values[-1].append(ticket[i])

	db = []
	for rule in rules:
		valids = []
		for i in range(len(field_values)):
			if field_matches(rule, field_values[i]):
				valids.append(i)
		db.append((len(valids), rule[0], valids))

	slots = {}
	reserved = set()
	for _, field_name, cands in sorted(db):
		slot = list(set(cands) - set(reserved))[0]
		slots[field_name] = slot
		reserved.add(slot)
	result = 1
	for name in slots:
		print(f"{name}: {slots[name]}")
		if name[:9] == "departure":
			result *= my_ticket[slots[name]]
	return result

rules, my_ticket, nearby_tickets = parse("sample.txt")
# print(solution1(rules, nearby_tickets))
print(solution2(rules, my_ticket, nearby_tickets))
rules, my_ticket, nearby_tickets = parse("input.txt")
# print(solution1(rules, nearby_tickets))
print(solution2(rules, my_ticket, nearby_tickets))