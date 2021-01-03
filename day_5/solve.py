def find(binary_codes, limit):
	upper = limit
	lower = 0
	for code in binary_codes:
		if code:
			lower = (upper + lower) // 2
		else:
			upper = (upper + lower) // 2
	return (upper + lower) // 2

def parse(text, key):
	result = []
	for c in text:
		result.append(key[c])
	return result

ROW_KEY = {"F": False, "B": True}
COL_KEY = {"L": False, "R": True}

def solution1(seats):
	for seat in seats:
		row = find(parse(seat[:7], ROW_KEY), 128)
		col = find(parse(seat[7:], COL_KEY), 8)
		yield row, col

def get_seat_id(seat):
	return seat[0]*8 + seat[1]

def solution2(seats):
	present_seats = set(solution1(seats))
	all_seats = set()
	for x in range(128):
		for y in range(8):
			all_seats.add((x,y))
	missing_seats = all_seats - present_seats
	present_ids = set([get_seat_id(x) for x in present_seats])
	for seat in missing_seats:
		seat_id = get_seat_id(seat)
		if seat_id-1 in present_ids and seat_id+1 in present_ids:
			return seat
	return None

print(max(map(lambda x: x[0]*8 + x[1], solution1(open("sample.txt").read().strip().split()))))
print(max(map(lambda x: x[0]*8 + x[1], solution1(open("input.txt").read().strip().split()))))
print(solution2(open("input.txt").read().strip().split()))