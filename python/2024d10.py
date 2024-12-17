
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def walk(grid, r, c, seen):
	paths = 0
	if grid[r][c] == 9:
		seen.add((r, c))
		return 1
	for dr, dc in dirs:
		if r+dr < 0 or c+dc < 0 or r+dr >= len(grid) or c+dc >= len(grid[r]):
			continue
		if grid[r+dr][c+dc] == grid[r][c] + 1:
			paths += walk(grid, r+dr, c+dc, seen)
	return paths

def ex1(filename):
	with open(filename, "r") as f:
		grid = [[int(elem) for elem in list(line) ] for line in f.read().strip().split("\n")]
	trailheads_score = 0
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] != 0:
				continue
			seen = set()
			walk(grid, r, c, seen)
			trailheads_score += len(seen)
	return trailheads_score

def ex2(filename):
	with open(filename, "r") as f:
		grid = [[int(elem) for elem in list(line) ] for line in f.read().strip().split("\n")]
	paths = 0
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] != 0:
				continue
			seen = set()
			w = walk(grid, r, c, seen)
			paths += walk(grid, r, c, seen)
	return paths

print(f"ex1: {ex1("./input.txt")}")
print(f"ex1: {ex2("./input.txt")}")