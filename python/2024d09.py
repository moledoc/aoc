
def pprint(int_list):
	print("".join([str(x) for x in int_list if x != -1]))


def ex1(filename):
	with open(filename, "r") as f:
		disk_map = [int(line) for line in f.read().strip("\n")]

	disk_map_len = len(disk_map)

	free_spaces = [0 for _ in range(disk_map_len//2)]
	file_blocks = [(0, 0) for _ in range(disk_map_len - disk_map_len//2)]
	b_idx = 0
	s_idx = 0
	id = 0
	for i in range(0, disk_map_len):
		if i % 2 == 0:
			file_blocks[b_idx] = (id, disk_map[i])
			b_idx += 1
			id += 1
		else:
			free_spaces[s_idx] = disk_map[i]
			s_idx += 1

	new_disk_mapping = []

	while True:
		if len(file_blocks) == 0:
			break
		# handle file block by consuming from beginning
		id, count = file_blocks[0]
		for _ in range(count):
			new_disk_mapping.append(id)
		file_blocks = file_blocks[1::]

		# handle free space by consuming free space from beginning
		# and file blocks at the end
		# NOTE: fit block-by-block
		for fre in range(free_spaces[0]):
			if len(file_blocks) == 0 or len(free_spaces) == 0:
				break
			id, count = file_blocks[-1]
			new_disk_mapping.append(id)
			if count-1 > 0:
				file_blocks[-1] = (id, count - 1)
			else:
				file_blocks = file_blocks[:len(file_blocks)-1]
		free_spaces = free_spaces[1::]

	checksum = 0
	for i in range(len(new_disk_mapping)):
		checksum += i * new_disk_mapping[i]
	return checksum

def ex2(filename):
	with open(filename, "r") as f:
		disk_map = [int(line) for line in f.read().strip("\n")]

	dmap = [(-1, -1) for _ in range(len(disk_map))]

	id = 0
	for i in range(0, len(dmap), 2):
		dmap[i] = (id, disk_map[i])
		id += 1
	for i in range(1, len(dmap), 2):
		dmap[i] = (-1, disk_map[i])

	r = len(dmap)
	while True:
		r -= 1
		if r < 0:
			break
		r_id, r_count = dmap[r]
		if r_id == -1: # skip empty blocks
			continue
		for l in range(r):
			if l >= r:
				break
			l_id, l_count = dmap[l]
			if l_id != -1: # skip file blocks
				continue
			if l_count < r_count: # skip empty blocks that are smaller
				continue

			dmap[l] = (r_id, r_count) # move right to left with right_count
			
			# move empty to left with right count
			# and concat surrounding empty blocks
			extra = 0
			if r + 1 < len(dmap):
				if dmap[r+1][0] == -1:
					extra += dmap[r+1][1]
					dmap[r+1] = (-1, 0)
			if dmap[r-1][0] == -1:
				extra += dmap[r-1][1]
				dmap[r-1] = (-1, 0)
			dmap[r] = (l_id, r_count+extra) # move left id to right with right_count
			# add left-over empty block
			if l_count > r_count:
				dmap.insert(l+1, (-1, l_count - r_count))
				r += 1
			break
			
	new_disk_map = []
	for id, count in dmap:
		if id == -1 and count == 0:
			continue
		new_disk_map.extend([id for _ in range(count)])

	checksum = 0
	for i in range(len(new_disk_map)):
		if new_disk_map[i] == -1:
			continue
		checksum += i * new_disk_map[i]

	return checksum


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")

