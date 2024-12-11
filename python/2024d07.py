
def intify(str_list):
	return [int(elem) for elem in str_list]

def plus(a, b, rest):
	return max(a + b, b)

def mult(a, b, rest):
	return max(a * b, b)

def ex_recur(target, acc, op_funcs, rest):
	if len(rest) == 0:
		return acc if acc == target else 0
	for op_func in op_funcs:
		rest1 = rest[:]
		acc1 = op_func(acc, rest[0], rest1)
		if acc1 > target:
			continue
		r = ex_recur(target, acc1, op_funcs, rest1[1::])
		if r != 0:
			return r
	return 0

def ex1(filename):
	with open(filename, "r") as f:
		lines = [intify(line.replace(":", "").split(" ")) for line in f.read().strip("\n").split("\n")]
	return sum([ex_recur(line[0], line[1], [mult, plus], line[2::]) for line in lines])

def concat(a, b, rest):
	if len(rest) > 0:
		a = int(str(a) + str(rest[0]))
		rest = rest[1:]
	return a

# NOTE: a bit slow, but beareble
def ex2(filename):
	with open(filename, "r") as f:
		lines = [intify(line.replace(":", "").split(" ")) for line in f.read().strip("\n").split("\n")]
	return sum([ex_recur(line[0], line[1], [mult, plus, concat], line[2::]) for line in lines])

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")

