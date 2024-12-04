
lxmas = list("XMAS")
blxmas = lxmas[::-1]

def transpose(lines):
	new = [None for _ in range(len(lines[0]))]
	for col in range(0, len(lines[0])):
		nrow = [None for _ in range(len(lines))]
		for row in range(0, len(lines)):
			nrow[row] = lines[row][col]
		new[col] = nrow
	return new

def diagonalize(lines):
	new = [None for _ in range(len(lines)*2-1)]

	main_diag = ['' for _ in range(len(lines))]
	for i in range(len(lines)):
		main_diag[i] = lines[i][i]
	new[0] = main_diag

	new_offset = 1

	for row in range(1, len(lines)):
		lower_diag = ['' for _ in range(len(lines[row]))]
		for col in range(0, len(lines[i])):
			if len(lines) <= row+col:
				break
			lower_diag[col] = lines[row+col][col]
		new[new_offset] = lower_diag
		new_offset += 1

	for col in range(1, len(lines)):
		upper_diag = ['' for _ in range(len(lines[row]))]
		for row in range(0, len(lines[row])):
			if len(lines) <= row+col:
				break
			upper_diag[row] = lines[row][row+col]
		new[new_offset] = upper_diag
		new_offset += 1

	return new		

def flip(lines):
	new = [None for _ in range(len(lines))]
	for i in range(len(lines)):
		new[i] = lines[i][::-1]
	return new

def count_xmas(lines):
	xmas_count = 0
	for line in lines:
		if len(lines) < 4:
			continue
		for i in range(4, len(line)+1):
			fwd = line[i-4:i]
			if '' in fwd:
				break
			xmas_count += int((fwd == lxmas) or (fwd == blxmas))
	return xmas_count

def ex1(filename):
	with open(filename, "r") as f:
		content = f.read().strip("\n")

	lines = [list(line) for line in content.split("\n")]

	xmas_count = 0
	# rows
	xmas_count += count_xmas(lines)
	# cols
	xmas_count += count_xmas(transpose(lines))

	# left to right diag
	xmas_count += count_xmas(diagonalize(lines))
	# right to left diag
	xmas_count += count_xmas(diagonalize(flip(lines)))

	return xmas_count

def ex2(filename):
	with open(filename, "r") as f:
		content = f.read().strip("\n")

	lines = [list(line) for line in content.split("\n")]

	xmas_count = 0
	for row in range(0,len(lines)):
		for col in range(0, len(lines[row])):
			if lines[row][col] != 'A':
				continue

			top_row = row-1
			bot_row = row+1
			left_col = col-1
			right_col = col+1

			# bounds
			# NW
			if top_row < 0 or left_col < 0:
				continue
			# NE
			if top_row < 0 or len(lines[top_row]) <= right_col:
				continue
			# SW

			if len(lines) <= bot_row or left_col < 0:
				continue
			# SE
			if len(lines) <= bot_row or len(lines[top_row]) <= right_col:
				continue

			# left to right diag
			if lines[top_row][left_col] not in ['M', 'S']:
				continue
			if lines[bot_row][right_col] not in ['M', 'S']:
				continue
			if lines[top_row][left_col] == lines[bot_row][right_col]:
				continue

			# right to left diag
			if lines[bot_row][left_col] not in ['M', 'S']:
				continue
			if lines[top_row][right_col] not in ['M', 'S']:
				continue
			if lines[bot_row][left_col] == lines[top_row][right_col]:
				continue
							
			xmas_count += 1

	return xmas_count


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")
