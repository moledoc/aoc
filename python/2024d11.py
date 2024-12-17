def intify(str_list):
	return [int(elem) for elem in str_list]

def ex(filename, iters):
	with open(filename, "r") as f:
		numbers = [intify(line.split(" ")) for line in f.read().strip("\n").split("\n")][0]

	mapping = {}
	for n in numbers:
		mapping[n] = 1

	for _ in range(iters):
		n_mapping = {}
		for k, v in mapping.items():
			kstr = str(k)
			len_k = len(kstr)
			if k == 0:
				n_mapping[1] = (n_mapping.get(1) or 0) + v
			elif len_k % 2 == 0:
				n1, n2 = int(kstr[:len_k//2]), int(kstr[len_k//2:])
				n_mapping[n1] = (n_mapping.get(n1) or 0) + v
				n_mapping[n2] = (n_mapping.get(n2) or 0) + v
			else:
				n_mapping[2024*k] = (n_mapping.get(2024*k) or 0) + v
		mapping = n_mapping

	sum = 0
	for k, v in mapping.items():
		sum += v

	return sum

print(f"ex1: {ex("./input.txt", 25)}")
print(f"ex2: {ex("./input.txt", 75)}")