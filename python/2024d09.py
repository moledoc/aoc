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

	# pprint(new_disk_mapping)
	checksum = 0
	for i in range(len(new_disk_mapping)):
		checksum += i * new_disk_mapping[i]
	return checksum

# 6787922826883 too high
def ex2(filename):
	with open(filename, "r") as f:
		disk_map = [int(line) for line in f.read().strip("\n")]

	disk_map_tuples = [(-1, -1) for _ in range(len(disk_map))]

	id = 0
	for i in range(len(disk_map)):
		if i % 2 == 0:
			disk_map_tuples[i] = (id, disk_map[i])
			id += 1
		else:
			disk_map_tuples[i] = (-1, disk_map[i])

	r_offset = len(disk_map_tuples)

	seen = {}
	while True:
		r_offset -= 1
		if r_offset < 0:
			break

		r_id, r_count = disk_map_tuples[r_offset]

		if r_id == -1:
			continue

		for l in range(len(disk_map_tuples)):
			l_id, l_count = disk_map_tuples[l]
			if l_id != -1:
				continue
			if l > r_offset: # don't move stuff we already touched
				break
			if r_count == l_count: # swap places
				disk_map_tuples[l] = (r_id, r_count)
				disk_map_tuples[r_offset] = (-1, r_count)
				r_offset -= 1
				break
			elif r_count < l_count:
				# swap empty with file block
				disk_map_tuples[l] = (l_id, l_count - r_count)
				disk_map_tuples[r_offset] = (-1, r_count)
				# add new file block tuple
				disk_map_tuples.insert(l, (r_id, r_count))
				r_offset -= 1
				break

	# print(disk_map_tuples)
	new_disk_map = []
	for id, count in disk_map_tuples:
		new_disk_map.extend([id for _ in range(count)])
	# pprint(new_disk_map)

	checksum = 0
	for i in range(len(new_disk_map)):
		if new_disk_map[i] == -1:
			continue
		checksum += i * new_disk_map[i]

	return checksum


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")

