
def pprint(grid):
	print("-------------------------")
	print("\n".join(["".join(row) for row in grid]))

def start(grid):
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] in ['^', '>', 'v', '<']:
				return (r, c), grid[r][c]

dirs = ['^', '>', 'v', '<']
steps = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	grid[r][c] = 'X'
	while True:
		s = steps[dir]
		r, c = r+s[0], c+s[1]
		if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
			break
		if grid[r][c] == '#':
			r,c = r-s[0], c-s[1] # step back
			dir = dirs[(dirs.index(dir)+1)%4] # change dir
			s = steps[dir]
			r, c = r+s[0], c+s[1] # step again
		grid[r][c] = 'X'
		# pprint(grid)
	# pprint(grid)
	return sum([1 if x == 'X' else 0 for xs in grid for x in xs])

def is_loop(grid, coord, dir):
	orig_dir = dir
	r, c = coord
	dir = dirs[(dirs.index(dir)+1)%4]
	# print(coord, orig_dir, dir)
	while True:
		s = steps[dir]
		r, c = r+s[0], c+s[1]
		if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
			return False
		if grid[r][c] == '#':
			r,c = r-s[0], c-s[1] # step back
			dir = dirs[(dirs.index(dir)+1)%4] # change dir
			s = steps[dir]
			r, c = r+s[0], c+s[1] # step again
		if (r, c) == coord:
			# print(r, c, orig_dir)
			return True
	return False

def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	grid[r][c] = 'X'
	loops = 0
	while True:
		s = steps[dir]
		r, c = r+s[0], c+s[1]
		if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
			break
		if grid[r][c] == '#':
			r,c = r-s[0], c-s[1] # step back
			dir = dirs[(dirs.index(dir)+1)%4] # change dir
			s = steps[dir]
			r, c = r+s[0], c+s[1] # step again
		grid[r][c] = 'X'
		loops += 1 if is_loop(grid, (r, c), dir) else 0
		# pprint(grid)
	# pprint(grid)
	return loops

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./sample.txt")}")