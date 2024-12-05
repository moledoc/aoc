
def intify(str_list):
	return [int(elem) for elem in str_list]

def pos_mapping(rules):
	mapping = ({}, {})
	for r1,r2 in rules:
		if r1 not in mapping[0]:
			mapping[0][r1] = [r2]
		else:
			mapping[0][r1].append(r2)
		if r2 not in mapping[1]:
			mapping[1][r2] = [r1]
		else:
			mapping[1][r2].append(r1)
	return mapping

def ex1(filename):
	with open(filename, "r") as f:
		rules, pages = f.read().split("\n\n")
		rules = rules.split("\n")
		pages = pages.split("\n")

	rules = [intify(line.split("|")) for line in rules]
	pages = [intify(line.split(",")) for line in pages]

	sum = 0
	mapping = pos_mapping(rules)
	for page in pages:
		correct = True
		for i in range(1, len(page)):
			if page[i] not in (mapping[0].get(page[i-1]) or []):
				correct = False
				break
		if correct:
			sum += page[len(page)//2]

	return sum

def order_with(page, mapping):
	while True:
		changes = 0
		for i in range(0, len(page)-1):
			for j in range(i+1, len(page)):
				if page[i+1] not in (mapping[0].get(page[i]) or []):
					if page[i] not in (mapping[0].get(page[i+1]) or []):
						raise "anomaly"
					a = page[i]
					b = page[i+1]
					page[i+1] = a
					page[i] = b
					changes += 1
		if changes == 0:
			break
	return page

def ex2(filename):
	with open(filename, "r") as f:
		rules, pages = f.read().split("\n\n")
		rules = rules.split("\n")
		pages = pages.split("\n")

	rules = [intify(line.split("|")) for line in rules]
	pages = [intify(line.split(",")) for line in pages]

	sum = 0
	mapping = pos_mapping(rules)
	for page in pages:
		incorrect = False
		for i in range(1, len(page)):
			if page[i] not in (mapping[0].get(page[i-1]) or []):
				incorrect = True
				break
		if incorrect:
			page = order_with(page, mapping)
			sum += page[len(page)//2]

	return sum


print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")
