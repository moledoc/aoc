
def ex1(filename):
	with open(filename, "r") as f:
		disk_map = [int(line) for line in f.read().strip("\n")]

	# print(len(disk_map))
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
	# print(file_blocks)
	# print(free_spaces)

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
		# MAYBE: TODO: currently consuming file blocks one at a time, but maybe should do it smarter
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

	# print("".join([str(x) for x in new_disk_mapping]))
	checksum = 0
	for i in range(len(new_disk_mapping)):
		checksum += i * new_disk_mapping[i]
	return checksum

print(f"ex1: {ex1("./input.txt")}")
# print(f"ex2: {ex2("./sample.txt")}")

