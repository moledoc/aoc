
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
		if grid[r1][c1] in ['#', 'O']:
			dir = dirs[(dir+1)%4] # change dir
			s = steps[dir]
			r1, c1 = r+s[0], c+s[1] # step again
			continue
		break
	return True, r1, c1, dir

def walk(grid, r, c, dir):
	seen = {}
	while True:
		if (seen.get((r, c)) or -1) == dir:
			return True
		grid[r][c] = 'X'
		seen |= {((r, c), dir)}
		cont, r, c, dir = take_step(grid, r, c, dir)
		if not cont:
			break
	return False

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	walk(grid, r, c, dir)
	return sum([c == 'X' for r in grid for c in r])


# walk the path and mark all X's
# for each X, check if that leads to a loop, by replacing the X with # and walking the path from start again
def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip("\n").split("\n")]

	coord, dir = start(grid)
	r, c = coord
	walk(grid, r, c, dir)

	obs = []
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			if grid[row][col] == 'X':
				grid[row][col] = '#' # put tmp obs
				obs.append(walk(grid, r, c, dir))
				grid[row][col] = 'X' # rm tmp obs
	return sum(obs)

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")