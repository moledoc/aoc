def intify(str_list):
	return [int(elem) for elem in str_list]

def pprint(grid):
	print("-------------------------")
	print("\n".join(["".join(map(str, row)) for row in grid]))

def check_antinode1(grid, row, col, antinodes):
	antenna = grid[row][col]
	for r in range(row, len(grid)):
		for c in range(len(grid[0])):
			if c == col:
				continue
			if grid[r][c] != antenna:
				continue
			r_dist = r - row
			c_dist = c - col
			if row - r_dist >= 0 and row - r_dist < len(grid) and col - c_dist >= 0 and col - c_dist < len(grid[0]):
				antinodes[row-r_dist][col-c_dist] = 1
			if r + r_dist < len(grid) and r + r_dist >= 0 and c + c_dist < len(grid[0]) and c + c_dist >= 0:
				antinodes[r+r_dist][c+c_dist] = 1

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	antinodes = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

	for r in range(len(grid)):
		for c in range(len(grid[r])):
			if grid[r][c] == '.':
				continue
			check_antinode1(grid, r, c, antinodes)

	return sum([node for anodes in antinodes for node in anodes])

def check_antinode2(grid, row, col, antinodes):
	antenna = grid[row][col]
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if r == row and c == col: # NOTE: handle only one its kind
				continue
			if grid[r][c] != antenna:
				continue
			r_dist = r - row
			c_dist = c - col

			fact = 1
			while True:
				if not (row - fact*r_dist >= 0 and \
					row - fact*r_dist < len(grid) and \
					col - fact*c_dist >= 0 and \
					col - fact*c_dist < len(grid[0])):
					break
				antinodes[row-fact*r_dist][col-fact*c_dist] = 1
				if r_dist == 0 or c_dist == 0:
					break
				fact += 1

			fact = 1
			while True:
				if not (r + fact*r_dist < len(grid) \
					and r + fact*r_dist >= 0 and \
					c + fact*c_dist < len(grid[0]) and \
					c + fact*c_dist >= 0):
					break
				antinodes[r+fact*r_dist][c+fact*c_dist] = 1
				if r_dist == 0 or c_dist == 0:
					break
				fact += 1

			antinodes[row][col] = 1 # NOTE: handle only one its kind

def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	antinodes = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

	for r in range(len(grid)):
		for c in range(len(grid[r])):
			if grid[r][c] == '.':
				continue
			check_antinode2(grid, r, c, antinodes)

	return sum([node for anodes in antinodes for node in anodes])


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")