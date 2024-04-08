#include <stdio.h>

// https://www.rfc-editor.org/rfc/rfc1321

typedef unsigned long int WORD; // 32-bits, little-endianess, uint4 (i.e. 4xBYTE=WORD)
typedef unsigned char BYTE; // 8-bits, big-endianess

static unsigned long int B2E32 = 0x100000000; // 2^32 or 16^8

static BYTE PADDING[64] = {
	0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

/*
long long int power(long long a, int n) {
	long long int res = 1;
	for (;n > 0; a*=a, n>>=1) {
		if (n & 1) {
			res *= a;
		}
	}
	return res;
}
*/

size_t my_strlen(const char *s) {
	char *s_cpy = (char *)s;
	size_t n = 0;
	for (; (*s++) != '\0'; ++n) {
		;
	}
	return n;
}

void strbits(size_t len, WORD b[2]) {
	WORD lenb = len << 3;
	for (int i=0; i<2; ++i) {
		b[i] = (lenb >> (0+(32*i))) | (lenb >> (8+(32*i))) | (lenb >> (16+(32*i))) | (lenb >> (24+(32*i)));
	}
}

WORD plus(WORD a, WORD b) {
	return (a+b)%B2E32;
}

WORD rot_left(WORD a, int s) {
	return (a << s) | (a >> (32-s));
}

void md5(char *message) {
	size_t message_len = my_strlen((const char *)message);
	size_t padding = message_len%56 == 0 ? 64 : 56-message_len%56;
	WORD message_b[2];
	strbits(message_len, message_b);

	printf("%d %d\n", message_b[0], message_b[1]);
}

int main() {
	md5("1234567890");
}