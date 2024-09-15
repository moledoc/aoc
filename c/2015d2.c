#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void freeme(char **elems, size_t elems_size) {
	for (int i=0; i<elems_size; ++i) {
		free(elems[i]);
	}
	free(elems);
}

char **split(const char *s, const char delim, size_t *elems_size) {
	int s_len = strlen((char *) s);
	int delim_count=0;
	for (int i=0; i<s_len; ++i) {
		if (s[i] == delim) {
			++delim_count;
		}
	}
	char **elems = calloc(delim_count+1, sizeof(char *));
	if (!delim_count) {
		*elems_size = 1;
		char *s1 = malloc((s_len+1)*sizeof(char));
		strncpy(s1, s, s_len);
		s1[s_len+1] = '\0';
		elems[0] = s1;
		return elems;
	}
	*elems_size = 0;
	int start = 0;
	for (int end=0; end<s_len+1; ++end) {
		if (s[end] == delim || end == s_len) {
			int s1_len = end-start;
			char *s1 = malloc((s1_len+1)*sizeof(char));
			s1[s1_len] = '\0';
			strncpy(s1, s+start, s1_len);
			elems[*elems_size] = s1;
			*elems_size += 1;
			
			start = end+1;
		}
	}
	return elems;
}

void sort(int *arr, size_t arr_size) {
	for (int i=0; i<arr_size-1; ++i) {
		if (arr[i] < arr[i+1]) {
			continue;
		}
		int a2 = arr[i];
		int a1 = arr[i+1];
		arr[i] = a1;
		arr[i+1] = a2;	
	}
}

int e1(char *buf) {
	long paper_needed = 0;

	size_t elems_size = 0;
	char **elems = split(buf, '\n', &elems_size);
	for (int i=0; i<elems_size; ++i) {
		size_t line_elems_size;
		char **line_elems = split(elems[i], 'x', &line_elems_size);
		int nr1 = atoi(line_elems[0]);
		int nr2 = atoi(line_elems[1]);
		int nr3 = atoi(line_elems[2]);
		int edges[3] = {nr1, nr2, nr3};
		sort(edges, 3);
		paper_needed += 2*(edges[0]*edges[1]+edges[1]*edges[2]+edges[2]*edges[0])+(edges[0]*edges[1]);
		freeme(line_elems, line_elems_size);		
	}
	freeme(elems, elems_size);
	return paper_needed;
}

int e2(char *buf) {

	long ribbon_needed = 0;

	size_t elems_size = 0;
	char **elems = split(buf, '\n', &elems_size);
	for (int i=0; i<elems_size; ++i) {
		size_t line_elems_size;
		char **line_elems = split(elems[i], 'x', &line_elems_size);
		int nr1 = atoi(line_elems[0]);
		int nr2 = atoi(line_elems[1]);
		int nr3 = atoi(line_elems[2]);
		int edges[3] = {nr1, nr2, nr3};
		sort(edges, 3);
		ribbon_needed += 2*(edges[0]+edges[1])+edges[0]*edges[1]*edges[2];
		freeme(line_elems, line_elems_size);		
	}
	freeme(elems, elems_size);
	return ribbon_needed;
}

int main(void) {
	FILE *fptr = fopen("./2015d2.in", "r");
	fseek(fptr, 0L, SEEK_END);
	long size = ftell(fptr);
	rewind(fptr);

	char buf[size+1];
	fread(buf, sizeof(char), size, fptr);
	fclose(fptr);
	buf[size]='\0';

	
	printf("e1: %d\n", e1(buf));
	printf("e2: %d\n", e2(buf));
}