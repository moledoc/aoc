
# inspirations for part 1: flood fill and minesweeper 
# inspirations for part 2: tracing shape outline + identifying nested regions, combining them and tracing combined region to get inner sides. So basically how I'd do it myself manually.

def pprint(grid):
	print("-------------------------")
	cln = lambda x: str(x).replace("-100", ",").replace("-1", ".")
	print("\n".join(["".join(map(cln, row)) for row in grid]))

dirChars = ['^', '>', 'v', '<']
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dirs_ext = dirs + [(1, 1), (-1, -1), (1, -1), (-1, 1)]

def flood_fill(grid, r, c, val, overall_seen, local_seen):
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
	# continue flood fill
	for dr, dc in dirs:
		flood_fill(grid, r+dr, c+dc, val, overall_seen, local_seen)

# carve relevant region out of the sparse grid
def carve(grid):
	max_r, min_r, max_c, min_c = -1, len(grid), -1, len(grid)
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] < 0:
				continue
			max_r = r if max_r < r else max_r
			max_c = c if max_c < c else max_c
			min_r = r if min_r > r else min_r
			min_c = c if min_c > c else min_c
	# we want to read until max_<r,c>
	# since range has [s,e), so we add +1
	max_r += 1
	max_c += 1
	return [[grid[r][c] for c in range(min_c, max_c)] for r in range(min_r, max_r)]

def ex1(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip().split('\n')]

	overall_seen = [[0 for _ in range(len(line))] for line in grid]
	local_seens = []
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if overall_seen[r][c] == 1:
				continue
			local_seen = [[-1 for _ in range(len(line))] for line in grid]
			flood_fill(grid, r, c, grid[r][c], overall_seen, local_seen)
			local_seens.append(carve(local_seen))

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
		# pprint(lseen) # debug
		# print(area, perimeter, area*perimeter) # debug
	return price

# fill region between given border
def fill_region(grid, r, c, border):
	if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] < 0:
		return
	if sum([r==br and c==bc for br, bc, _ in border]) > 0: # NOTE: cond means 'touching border'
		return
	grid[r][c] = -1
	# check diagonals, since some inner regions might be connected by a corner,
	# but they'd be counted as sep nested regions if not handled
	for dr, dc in dirs_ext:
		fill_region(grid, r+dr, c+dc, border)

def find_topleft(grid):
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] >= 0:
				return (r, c)
	return (-1, -1)

def mark_outside_of_region(grid, r, c, seen):
	if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
		return
	if grid[r][c] >= 0:
		return
	if seen[r][c] == 1:
		return
	if grid[r][c] < 0:
		grid[r][c] = -100
	seen[r][c] = 1
	for dr, dc in dirs:
		mark_outside_of_region(grid, r+dr, c+dc, seen)

def prepare_nested_region_handling(grid):
	# add padding to prepped, for easier flood fill outside area
	prepped = [[-100 for c in range(len(grid[0])+2)] for r in range(len(grid)+2)]
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			prepped[r+1][c+1] = grid[r][c]
	seen = [[0 for c in range(len(prepped[0]))] for r in range(len(prepped))]

	# mark outside of the region to distinguish nested region from other regions
	# by flood fill padded grid
	mark_outside_of_region(prepped, 0, 0, seen)

	# mark inner region as pos and everything else neg
	for r in range(len(prepped)):
		for c in range(len(prepped[0])):
			if prepped[r][c] == -1:
				prepped[r][c] = 0
			else:
				prepped[r][c] = -1
	return prepped

def trace_shape(grid, coord, end_coord, dir, turns, path):
	r, c = coord
	if (r, c) == end_coord and turns >= 4:
		return turns
	# while stepping into region
	dr, dc = dirs[dir]
	loc_turns_pre = 1
	loc_turns_loop = 0
	while r+dr >= 0 and c+dc >= 0 and r+dr < len(grid) and c+dc < len(grid[0]) and grid[r+dr][c+dc] >=0:
		dir = (dir-1)%4
		dr, dc = dirs[dir]
		loc_turns_loop += 1
	turn = abs(loc_turns_loop-loc_turns_pre)
	turns += turn
	path.append((r, c, turns))
	r += dr
	c += dc
	return trace_shape(grid=grid, coord=(r, c), end_coord=end_coord, dir=(dir+1)%4, turns=turns, path=path)

def count_sides(grid, fill=False):
	topleft = find_topleft(grid)
	start_coord = (topleft[0], topleft[1]-1)
	end_coord = (topleft[0]-1, topleft[1]-1) # end one step further from start to catch edge case turn
	path = []
	sides = trace_shape(grid=grid, coord=start_coord, end_coord=end_coord, dir=dirChars.index('>'), turns=0, path=path)
	if fill:
		fill_region(grid, topleft[0], topleft[1], path) # clean grid from traced region
	return sides

def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip().split('\n')]

	overall_seen = [[0 for _ in range(len(line))] for line in grid]
	local_seens = {}
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if overall_seen[r][c] == 1:
				continue
			local_seen = [[-1 for _ in range(len(line))] for line in grid]
			flood_fill(grid, r, c, grid[r][c], overall_seen, local_seen)
			local_seens[(r,c)] = carve(local_seen)

	price = 0
	for coord, lseen in local_seens.items():
		area = sum([lseen[r][c] >= 0 for r in range(len(lseen)) for c in range(len(lseen[0]))])
		side_count = count_sides(lseen)

		# handle nested regions
		lseen_inner = prepare_nested_region_handling(lseen)
		# pprint(lseen) # debug
		# pprint(lseen_inner) # debug
		# consume nested regions
		while sum([lseen_inner[r][c] >= 0 for r in range(len(lseen_inner)) for c in range(len(lseen_inner[0]))]) > 0:
			topleft_inner = find_topleft(lseen_inner)
			if topleft_inner == (-1, -1): # no nested region
				break
			side_count += count_sides(grid=lseen_inner, fill=True)
		price += area*side_count
		# print((coord[0], coord[1]), grid[coord[0]][coord[1]], area, side_count, area*side_count) # debug
	return price

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")