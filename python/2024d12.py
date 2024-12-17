
def pprint(grid):
	print("-------------------------")
	cln = lambda x: str(x).replace("-1", ".")
	print("\n".join(["".join(map(cln, row)) for row in grid]))

# idea:
# flood fill each region: 
# * have 1 main seen that keeps track what is already seen overall
# * have 1 local seen that keeps track of region:
# ** non-zero for cell in region (non-zero reason below)
# ** when finding area, count cells >= 0
# ** each cell contains nr of perimeter
# ** perimeter can be found by checking neighbours and if same val, that side is not perimeter

# inspirations: flood-fill and minesweeper 

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def floodfill(grid, r, c, val, overall_seen, local_seen):
	# pprint(local_seen)
	# print(r, c, val)
	if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
		return
	if grid[r][c] != val:
		return
	if local_seen[r][c] >= 0:
		return

	# mark cell seen in overall
	overall_seen[r][c] = 1

	# check perimeter
	# has perimeter if neighbour is out of bounds or val is different
	local_seen[r][c] = 0
	for dr, dc in dirs:
		if r+dr < 0 or c+dc < 0 or r+dr >= len(grid) or c+dc >= len(grid[0]) or grid[r+dr][c+dc] != val:
			local_seen[r][c] += 1

	# continue floodfill
	for dr, dc in dirs:
		floodfill(grid, r+dr, c+dc, val, overall_seen, local_seen)

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip().split('\n')]

	# pprint(grid)
	overall_seen = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
	local_seens = []
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if overall_seen[r][c] == 1:
				continue
			local_seen = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
			floodfill(grid, r, c, grid[r][c], overall_seen, local_seen)
			local_seens.append(local_seen)

	price = 0
	for lseen in local_seens:
		area = 0
		perimeter = 0
		for r in range(len(lseen)):
			for c in range(len(lseen[0])):
				if lseen[r][c] >= 0:
					perimeter += lseen[r][c]
					area += 1
		price += area*perimeter
		# pprint(lseen)
		# print(area, perimeter, area*perimeter)
	return price

print(f"ex1: {ex1("./input.txt")}")
# print(f"ex2: {ex2("./sample.txt")}")