valid_fields = {
	"byr",
	"iyr",
	"eyr",
	"hgt",
	"hcl",
	"ecl",
	"pid",
	"cid",
}

req_fields = {
	"byr",
	"iyr",
	"eyr",
	"hgt",
	"hcl",
	"ecl",
	"pid",
}

def valid_passports(passports):
	result = []
	for passport in passports:
		# print(f"passport: {passport}")
		tags = passport.split()
		db = {x.split(":")[0]: x.split(":")[1] for x in tags}
		keys = set(db.keys())
		if keys.issubset(valid_fields) and req_fields.issubset(keys):
			result.append(db)
	return result

def solution1(passports):
	return len(valid_passports(passports))

def solution2(passports):
	counter = 0
	for passport in valid_passports(passports):
		cond = len(passport["byr"]) == 4
		cond = cond and  len(passport["iyr"]) == 4
		cond = cond and len(passport["eyr"]) == 4
		cond = cond and (passport["hgt"][-2:] == "cm" or passport["hgt"][-2:] == "in")
		cond = cond and 1920 <= int(passport["byr"]) <= 2002
		cond = cond and 2010 <= int(passport["iyr"]) <= 2020
		cond = cond and 2020 <= int(passport["eyr"]) <= 2030
		if passport["hgt"][-2:] == "in":
			cond = cond and 59 <= int(passport["hgt"][:-2]) <= 76
		else:
			cond = cond and 150 <= int(passport["hgt"][:-2]) <= 193
		cond = cond and passport["hcl"][0] == "#"
		cond = cond and len(passport["hcl"][1:]) == 6
		cond = cond and all([x in "0987654321abcdef" for x in passport["hcl"][1:]])
		cond = cond and (passport["ecl"] in "amb blu brn gry grn hzl oth".split())
		cond = cond and len(passport["pid"]) == 9
		if cond:
			counter += 1
			
	return counter

print(solution1(open("sample.txt").read().strip().split("\n\n")))
print(solution1(open("input.txt").read().strip().split("\n\n")))

print(solution2(open("sample.txt").read().strip().split("\n\n")))
print(solution2(open("sample2.txt").read().strip().split("\n\n")))
print(solution2(open("input.txt").read().strip().split("\n\n")))
		