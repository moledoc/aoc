
def ex1(filename):
	with open(filename, "r") as f:
		lines = f.read().split("\n")

	a = sorted([int(line.split("   ")[0]) for line in lines])
	b = sorted([int(line.split("   ")[1]) for line in lines])
	dist = [abs(a[i]-b[i]) for i in range(0, len(a))]
	return sum(dist)

def ex2(filename):
	with open(filename, "r") as f:
		lines = f.read().split("\n")

	mp = {}
	for line in lines:
		idx = int(line.split("   ")[1])
		mp[idx] = int(mp.get(idx) or 0) + 1

	a = sorted([int(line.split("   ")[0]) for line in lines])
	scores = [ai * int(mp.get(ai) or 0) for ai in a]
	return sum(scores)

print(f"ex1: {ex1("./input.txt")}")
print(f"ex2: {ex2("./input.txt")}")