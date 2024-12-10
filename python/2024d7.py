
def intify(str_list):
	return [int(elem) for elem in str_list]

def plus(a, b):
	return a + b

def mult(a, b):
	return a * b

# debug = []

def ex1_recur(target, acc, op_funcs, rest):
	# global debug
	if len(rest) == 0:
		return 0
	for op_func in op_funcs:
		# debug.append({rest[0], op_func})
		# print(debug)
		acc1 = op_func(acc, rest[0])
		if target == acc1:
			return target
		if target < acc1:
			# debug = debug[0:-1]
			continue
		r = ex1_recur(target, acc1, op_funcs, rest[1::])
		if r != 0:
			return r
		# debug = debug[0:-1]
	# debug = debug[0:-1]
	return 0

def ex1(filename):
	with open(filename, "r") as f:
		lines = [intify(line.replace(":", "").split(" ")) for line in f.read().strip("\n").split("\n")]
	return sum([ex1_recur(line[0], line[1], [mult, plus], line[2::]) for line in lines])

print(f"ex1: {ex1("./input.txt")}")
# print(f"ex2: {ex2("./sample.txt")}")
