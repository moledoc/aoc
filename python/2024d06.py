
dirChars = ['^', '>', 'v', '<']
dirs = [0, 1, 2, 3]
steps = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

def pprint(grid):
	print("-------------------------")
	print("\n".join(["".join(row) for row in grid]))

def start(grid):
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] in dirChars:
				return (r, c), dirChars.index(grid[r][c])

def take_step(grid, r, c, dir):
	while True:
		s = steps[dir]
		r1, c1 = r+s[0], c+s[1]
		if r1 < 0 or c1 < 0 or r1 >= len(grid) or c1 >= len(grid[0]):
			return False, r, c, dir
		if grid[r1][c1] == '#':
			dir = dirs[(dir+1)%4] # change dir
			s = steps[dir]
			r1, c1 = r+s[0], c+s[1] # step again
			continue
		break
	return True, r1, c1, dir

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	grid[r][c] = 'X'
	while True:
		cont, r, c, dir = take_step(grid, r, c, dir)
		if not cont:
			break
		grid[r][c] = 'X'
	return sum([1 if x == 'X' else 0 for xs in grid for x in xs])

def is_loop(grid, coord, dir):
	orig_dir = dir
	r, c = coord

	# add tmp obs
	cont, r1, c1, dir1 = take_step(grid, r, c, dir)
	if not cont or dir1 != dir: # next step is out of bounds, don't add tmp obs or next step changed dir, meaning there already is a obs
		return 0

	before_obs = grid[r1][c1]
	grid[r1][c1] = '#'

	seen = {}

	looped = 0
	while True:
		if r in seen and c in seen[r] and dir in seen[r][c]:
			looped = 1
			break
		if r not in seen:
			seen[r] = {}
		if c not in seen[r]:
			seen[r][c] = []
		if dir not in seen[r][c]:
			seen[r][c].append(dir)

		cont, r, c, dir = take_step(grid, r, c, dir)
		if not cont:
			break

	# rm tmp obs
	grid[r1][c1] = before_obs
	return looped

def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	loops = 0
	while True:
		cont, r, c, dir = take_step(grid, r, c, dir)
		if not cont:
			break
		loops += is_loop(grid, (r, c), dir)
	return loops

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")