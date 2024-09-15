#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *disallowed[4] = {"ab", "cd", "pq", "xy"};

void freeme(char **elems, size_t elems_size) {
	for (int i=0; i<elems_size; ++i) {
		free(elems[i]);
	}
	free(elems);
}


char **split(const char *s, const char delim, size_t *elems_count) {
	int s_len = strlen((char *) s);
	int delim_count=0;
	for (int i=0; i<s_len; ++i) {
		if (s[i] == delim) {
			++delim_count;
		}
	}
	char **elems = calloc(delim_count+1, sizeof(char *));
	if (!delim_count) {
		*elems_count = 1;
		char *s1 = malloc((s_len+1)*sizeof(char));
		strncpy(s1, s, s_len);
		s1[s_len+1] = '\0';
		elems[0] = s1;
		return elems;
	}
	*elems_count = 0;
	int start = 0;
	for (int end=0; end<s_len+1; ++end) {
		if (s[end] == delim || end == s_len) {
			int s1_len = end-start;
			char *s1 = malloc((s1_len+1)*sizeof(char));
			s1[s1_len] = '\0';
			strncpy(s1, s+start, s1_len);
			elems[*elems_count] = s1;
			*elems_count += 1;
			
			start = end+1;
		}
	}
	return elems;
}

int e1(char *buf, size_t buf_size) {
	int nice_words = 0;
	size_t elems_count;
	char **elems = split(buf, '\n', &elems_count);

	int is_disallowed(char cc[2]) {
		for (int k=0; k<4; ++k) {
			if (strcmp(disallowed[k], cc) == 0) {
				return 1;
			}
		}
		return 0;
	} 
	
	int is_vowel(char c) {
		return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
	}

	for (int i=0; i<elems_count; ++i) {
		char c = *(elems[i]);
		int vowel_count = is_vowel(c);
		char prev = *(elems[i]);
		int is_nice = 1;
		int twice = 0;
		size_t elem_i_len = strlen(elems[i]);
		for (int j=1; j<elem_i_len && is_nice; ++j) {
			c = *(elems[i]+j);

			char pair[3];
			pair[0] = prev;
			pair[1] = c;
			pair[2] = '\0';

			// check disallowed pairs
			if (is_disallowed(pair)) {
				is_nice = 0;
				break;
			}

			// check twice in a row
			if (prev == c) {
				twice = 1;
			}

			// count vowels
			if (is_vowel(c)) {
				++vowel_count;
			}
			prev = c;
		}
		if (vowel_count < 3 || !twice) {
			is_nice = 0;
		}
		nice_words += is_nice;
	}
	
	freeme(elems, elems_count);
	return nice_words;
}

int e2(char *buf, size_t buf_size) {
	int nice_words = 0;
	size_t elems_count;
	char **elems = split(buf, '\n', &elems_count);

	int x_x(char ccc[3]) {
		return ccc[0]==ccc[2];
	} 
	
	int seen_pair(char *elems, size_t elems_len, char cc[2]) {
		for (int i=1; i<elems_len; ++i) {
			char tmp[3] = {elems[i-1], elems[i], '\0'};
			if (strcmp(cc, tmp) == 0) {
				return 1;
			}
		}
		return 0;
	}

	for (int i=0; i<elems_count; ++i) {
		char pprev = '\0';
		char prev = *(elems[i]);

		size_t elem_i_len = strlen(elems[i]);

		int twice = 0;
		int a_a = 0;

		for (int j=1; j<elem_i_len; ++j) {
			char c = *(elems[i]+j);

			char triplet[4];
			triplet[0] = pprev;
			triplet[1] = prev;
			triplet[2] = c;
			triplet[3] = '\0';

			// check pair
			if (!twice && seen_pair(elems[i]+j+1,elem_i_len-1-j, triplet+1)) {
				twice = 1;
			}

			// check x_x
			if (!a_a && x_x(triplet)) {
				a_a = 1;
			}
			pprev = prev;
			prev = c;
		}
		nice_words += a_a && twice;
	}
	
	freeme(elems, elems_count);
	return nice_words;
}

int main(void) {
	FILE *fptr = fopen("2015d5.in", "r");
	fseek(fptr, 0, SEEK_END);
	long size = ftell(fptr);
	rewind(fptr);
	char buf[size+1];
	buf[size] = '\0';
	fread(buf, sizeof(char), size, fptr);
	fclose(fptr);

	printf("e1: %d\n", e1(buf, size));
	printf("e2: %d\n", e2(buf, size));
}