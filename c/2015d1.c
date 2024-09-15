#include <stdio.h>

int e1(char *input, int size) {
	int level = 0;
	for (int i=0; i<size; ++i) {
		switch (input[i]) {
		case '(':
			++level;
			break;
		case ')':
			--level;
			break;
		}
	}
	return level;
}

int e2(char *input, int size) {
	int level = 0;
	for (int i=0; i<size; ++i) {
		switch(input[i]) {
		case '(':
			++level;
			break;
		case ')':
			--level;
			break;
		}
		if (level == -1) {
			return i+1;
		}
	}
	return -1;
}

int main(int argc, char **argv) {
	FILE *fptr = fopen("./2015d1.in", "r");
	fseek(fptr, 0L, SEEK_END);
	long size = ftell(fptr);
	rewind(fptr);

	char buf[size];
	int nread = fread(buf, sizeof(char), size, fptr);
	fclose(fptr);
	printf("e1: %d\n", e1(buf, size));
	printf("e2: %d\n", e2(buf, size));
}