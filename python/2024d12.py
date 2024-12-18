
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

# inspirations for part 1: flood-fill and minesweeper 
# inspirations for part 2: trace outline (the way I'd solve it as a human) + add nester region trace outlines for each region

dirChars = ['^', '>', 'v', '<']
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

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

def trace_outside(grid, coord, end_coord, dir, turns, path):
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
	turns += abs(loc_turns_loop-loc_turns_pre)
	path.append((r,c))
	r += dr
	c += dc
	return trace_outside(grid=grid, coord=(r, c), end_coord=end_coord, dir=(dir+1)%4, turns=turns, path=path)

# construct new grid
# copy values from lseen and candidate for nested region to new grid
# see if any candidate value is seen when looking inward from all sides
def contains(lseen, lseen_inner):
	seen = [[lseen[r][c] for r in range(len(lseen))] for c in range(len(lseen[0]))]
	for r in range(len(lseen_inner)):
		for c in range(len(lseen_inner)):
			if lseen_inner[r][c] >= 0:
				seen[r][c] = -100

	# horizontal
	for r in range(len(seen)):
		for c in range(len(seen[0])):
			if seen[r][c] == -100 or seen[r][len(seen[0])-1-c] == -100:
				return False
			if seen[r][c] >= 0 or seen[r][len(seen[0])-1-c] >= 0:
				break
	# vertical
	for c in range(len(seen[0])):
		for r in range(len(seen)):
			if seen[r][c] == -100 or seen[len(seen)-1-r][c] == -100:
				return False
			if seen[r][c] >= 0 or seen[len(seen)-1-r][c] >= 0:
				break

	return True

# 884402 - too low
def ex2(filename):
	with open(filename, "r") as f:
		grid = [list(line) for line in f.read().strip().split('\n')]

	# pprint(grid)
	overall_seen = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
	local_seens = {}
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if overall_seen[r][c] == 1:
				continue
			local_seen = [[-1 for _ in range(len(grid[0]))] for _ in range(len(grid))]
			floodfill(grid, r, c, grid[r][c], overall_seen, local_seen)
			local_seens[(r, c)] = local_seen

	price = 0
	sides = {}
	for topleft, lseen in local_seens.items():
		area = sum([lseen[r][c] >= 0 for r in range(len(lseen)) for c in range(len(lseen[0]))])

		# pprint(lseen)

		# trace outside
		# start point is left of top-left corner of region (will also be end cond)
		# we want to 'get into the area',
		# so dir shows where we try to go,
		# but we might not be able to
		if topleft not in sides:
			start_coord = (topleft[0], topleft[1]-1)
			end_coord = (topleft[0]-1, topleft[1]-1) # end one step further from start to catch edge case turn
			path = []
			sides[topleft] = trace_outside(grid=lseen, coord=start_coord, end_coord=end_coord, dir=dirChars.index('>'), turns=0, path=path)

		side_count = sides[topleft]

		for r in range(len(lseen)):
			if r < topleft[0]:
				continue
			row_region_start = False
			for c in range(len(lseen[0])):
				if lseen[r][c] >= 0:
					row_region_start = True
					continue
				if row_region_start and lseen[r][c] < 0 and (r, c) in local_seens:
					topleft_inner = (r, c)
					lseen_inner = local_seens[topleft_inner]
					if contains(lseen, lseen_inner):
						if topleft_inner not in sides:
							start_coord = (r, c-1)
							end_coord = (r-1, c-1) # end one step further from start to catch edge case turn
							sides[topleft_inner] = trace_outside(grid=lseen_inner, coord=start_coord, end_coord=end_coord, dir=dirChars.index('>'), turns=0, path=[])
						side_count += sides[topleft_inner] 
					

		# print(area, side_count, area*side_count)
		price += area*side_count
	return price


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")