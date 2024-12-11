
def intify(str_list):
	return [int(elem) for elem in str_list]

def is_safe1(int_list):
	inc, dec = 0, 0
	for i in range(1, len(int_list)):
		dist = abs(int_list[i-1]-int_list[i])
		if not (1 <= dist and dist <= 3):
			return 0
		inc += int(int_list[i-1] < int_list[i])
		dec += int(int_list[i-1] > int_list[i])

	return not dec or not inc
			
def is_safe2_recur(int_list, attempt):
	if attempt > 1:
		return 0
	inc, dec, differ = 0, 0, 0, 0
	for i in range(1, len(int_list)):
		dist = abs(int_list[i-1]-int_list[i])
		differ += int(not (1 <= dist and dist <= 3))
		inc += int(int_list[i-1] < int_list[i])
		dec += int(int_list[i-1] > int_list[i])

	# safe with no fixes
	if differ == 0 and (inc == 0 or dec == 0):
		return 1

	# hulk smash
	for i in range(0,len(int_list)):
		cpy = int_list.copy()
		del cpy[i]
		if is_safe2_recur(cpy, attempt+1) == 1:
			return 1
	return 0

def is_safe2(int_list):
	return is_safe2_recur(int_list, 0)

def ex1(filename):
	with open(filename, "r") as f:
		return sum([is_safe1(intify(line.split(" "))) for line in f.read().strip("\n").split("\n")])

def ex2(filename):
	with open(filename, "r") as f:
		return sum([is_safe2(intify(line.split(" "))) for line in f.read().strip("\n").split("\n")])

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")
	