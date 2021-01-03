def transform(sn, lsize):
	val = 1
	for z in range(lsize):
		val *= sn
		val = val % 20201227
	return val

def crack(exp):
	val = 1
	for z in range(100000000):
		val = (val * 7) % 20201227
		if exp == val:
			return z+1

def guess(pubkey):
	for size in range(1000000):
		if transform(7, size) == pubkey:
			print(f"transform(7, {size}): {transform(7, size)}")
			return size
	return None

def get_key(key1, key2):
	size1 = crack(key1)
	size2 = crack(key2)
	return transform(key1, size2)
		

def main():
	print(get_key(5764801, 17807724))
	print(get_key(14222596, 4057428))

if __name__ == "__main__":
	main()