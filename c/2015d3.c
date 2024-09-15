#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void freeme(int **grid, size_t rows) {
	for (int i=0; i<rows; ++i) {
		free(grid[i]);
	}
	free(grid);
}

int e1(char *buf, size_t size) {
	// find grid size
	int dirs[4] = {0,0,0,0};
	for (int i=0; i<size; ++i) {
		switch (buf[i]) {
		case '^':
			++dirs[0]; break;
		case '>':
			++dirs[1]; break;
		case 'v':
			++dirs[2]; break;
		case '<':
			++dirs[3]; break;
		}
	}
	int rows = 2*(dirs[0] > dirs[2] ? dirs[0] : dirs[2]);
	int cols = 2*(dirs[1] > dirs[3] ? dirs[1] : dirs[3]);

	// set coordinates as middle for santa
	int row_cur = rows/2;
	int col_cur = cols/2;

	int **grid = malloc(rows * sizeof(int *));
	for (int i=0; i<rows; ++i) {
		grid[i] = calloc(cols, sizeof(int));
	}

	// follow directions	
	++grid[row_cur][col_cur];
	for (int i=0; i<size; ++i) {
		switch (buf[i]) {
		case '^':
			--row_cur; break;		
		case '>':
			++col_cur; break;
		case 'v':
			++row_cur; break;
		case '<':
			--col_cur; break;
		}
		++grid[row_cur][col_cur];
	}

	// find houses with >= presents
	int at_least_one = 0;
	for (int i=0; i<rows; ++i) {
		for (int j=0; j<cols; ++j) {
			at_least_one += grid[i][j] > 0 ? 1 : 0;
		}
	}
	freeme(grid, rows);
	return at_least_one;
}

int e2(char *buf, size_t size) {
	// find grid size
	int dirs[4] = {0,0,0,0};
	for (int i=0; i<size; ++i) {
		switch (buf[i]) {
		case '^':
			++dirs[0]; break;
		case '>':
			++dirs[1]; break;
		case 'v':
			++dirs[2]; break;
		case '<':
			++dirs[3]; break;
		}
	}
	int rows = 2*(dirs[0] > dirs[2] ? dirs[0] : dirs[2]);
	int cols = 2*(dirs[1] > dirs[3] ? dirs[1] : dirs[3]);

	// set coordinates as middle for santas
	int row_cur_santa = rows/2;
	int col_cur_santa = cols/2;
	int row_cur_robot = rows/2;
	int col_cur_robot = cols/2;

	int **grid = malloc(rows * sizeof(int *));
	for (int i=0; i<rows; ++i) {
		grid[i] = calloc(cols, sizeof(int));
	}

	// follow directions	
	++grid[row_cur_santa][col_cur_santa];
	++grid[row_cur_robot][col_cur_robot];
	for (int i=0; i<size; i+=2) {
		switch (buf[i]) {
		case '^':
			--row_cur_santa; break;		
		case '>':
			++col_cur_santa; break;
		case 'v':
			++row_cur_santa; break;
		case '<':
			--col_cur_santa; break;
		}
		switch (buf[i+1]) {
		case '^':
			--row_cur_robot; break;		
		case '>':
			++col_cur_robot; break;
		case 'v':
			++row_cur_robot; break;
		case '<':
			--col_cur_robot; break;
		}
		++grid[row_cur_santa][col_cur_santa];
		++grid[row_cur_robot][col_cur_robot];
	}

	// find houses with >= presents
	int at_least_one = 0;
	for (int i=0; i<rows; ++i) {
		for (int j=0; j<cols; ++j) {
			at_least_one += grid[i][j] > 0 ? 1 : 0;
		}
	}
	freeme(grid, rows);
	return at_least_one;

}

int main(void) {\
	FILE *fptr = fopen("./2015d3.in", "r");
	fseek(fptr, 0, SEEK_END);
	long size = ftell(fptr);
	rewind(fptr);
	char buf[size+1];
	buf[size]='\0';
	fread(buf, sizeof(char), size, fptr);
	fclose(fptr);


	printf("e1: %d\n", e1(buf, size));
	printf("e2: %d\n", e2(buf, size));
}