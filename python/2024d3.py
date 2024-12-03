

def ex1(filename):
	with open(filename, "r") as f:
		lines = f.read().strip("\n").split("\n")
	sum = 0
	for line in lines:
		line_len = len(line)
		for i in range(4, len(line)):
			if line[i-4:i] != "mul(":
				continue
			closing = -1
			for j in range(1, 8): # 1 to 3 digits + , + 1 to 3 digits
				if i+j >= line_len:
					break
				if line[i+j] == ")":
					closing = i+j
					break
				if not (line[i+j].isdigit() or line[i+j] == ","):
					break
			if closing == -1:
				continue
			numbers = line[i:closing].split(",")
			if len(numbers) != 2:
				continue
			sum += int(numbers[0]) * int(numbers[1])
	return sum

def ex2(filename):
	with open(filename, "r") as f:
		lines = f.read().strip("\n").split("\n")
	sum = 0
	enabled = True
	for line in lines:
		line_len = len(line)
		for i in range(4, len(line)):
			if i>=7 and line[i-7:i] == "don't()":
				enabled = False
			elif i>=4 and line[i-4:i] == "do()":
				enabled = True
			if line[i-4:i] != "mul(":
				continue
			if not enabled:
				continue
			closing = -1
			for j in range(1, 8): # 1 to 3 digits + , + 1 to 3 digits
				if i+j >= line_len:
					break
				if line[i+j] == ")":
					closing = i+j
					break
				if not (line[i+j].isdigit() or line[i+j] == ","):
					break
				
			if closing == -1:
				continue
			numbers = line[i:closing].split(",")
			if len(numbers) != 2:
				continue
			sum += int(numbers[0]) * int(numbers[1])
	return sum


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")
