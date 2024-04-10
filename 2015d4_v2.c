#include <stdio.h>

// https://www.rfc-editor.org/rfc/rfc1321

typedef unsigned long int WORD; // 32-bits, little-endianess, uint4 (i.e. 4xBYTE=WORD)
typedef unsigned char BYTE; // 8-bits, big-endianess

WORD B2E32 = 0x100000000; // 2^32 or 16^8

BYTE PADDING[64] = {
	0x80, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 
	0, 0, 0, 0, 
	0, 0, 0, 0, 
	0, 0, 0, 0, 
	0, 0, 0, 0, 
	0, 0, 0, 0
};

WORD table[64] = {
	0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
	0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
	0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
	0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,

	0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
	0xd62f105d,	0x02441453,	0xd8a1e681,	0xe7d3fbc8,
	0x21e1cde6,	0xc33707d6,	0xf4d50d87,	0x455a14ed,
	0xa9e3e905,	0xfcefa3f8,	0x676f02d9,	0x8d2a4c8a,

	0xfffa3942,	0x8771f681,	0x6d9d6122,	0xfde5380c,
	0xa4beea44,	0x4bdecfa9,	0xf6bb4b60,	0xbebfbc70,
	0x289b7ec6,	0xeaa127fa,	0xd4ef3085,	0x04881d05,
	0xd9d4d039,	0xe6db99e5,	0x1fa27cf8,	0xc4ac5665,

	0xf4292244,	0x432aff97,	0xab9423a7,	0xfc93a039,
	0x655b59c3,	0x8f0ccc92,	0xffeff47d,	0x85845dd1,
	0x6fa87e4f,	0xfe2ce6e0,	0xa3014314,	0x4e0811a1,
	0xf7537e82,	0xbd3af235,	0x2ad7d2bb,	0xeb86d391
};

#define S11 7
#define S12 12
#define S13 17
#define S14 22
#define S21 5
#define S22 9
#define S23 14
#define S24 20
#define S31 4
#define S32 11
#define S33 16
#define S34 23
#define S41 6
#define S42 10
#define S43 15
#define S44 21

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

size_t my_strlen(const unsigned char *s) {
	char *s_cpy = (char *)s;
	size_t n = 0;
	for (; (*s++) != '\0'; ++n) {
		;
	}
	return n;
}

void my_memcpy(unsigned char *dest, unsigned char *src, size_t len) {
	for (int i=0; i<len; ++i) {
		dest[i] = src[i];
	}
}

void my_memset(unsigned char *dest, unsigned char c, size_t len) {
	for (int i=0; i<len; ++i) {
		dest[i] = c;
	}
}

// only use it for preparing message len in bits for constructing message_pp
void strbits(unsigned char *b, size_t len) {
	unsigned long long int lenb = len << 3;
	for (int i=0; i<2; ++i) {
		b[4*i+0] = (unsigned char)((lenb >> ( 0+(32*i))) & 0xff);
		b[4*i+1] = (unsigned char)((lenb >> ( 8+(32*i))) & 0xff);
		b[4*i+2] = (unsigned char)((lenb >> (16+(32*i))) & 0xff);
		b[4*i+3] = (unsigned char)((lenb >> (24+(32*i))) & 0xff);
	}
}

// only use it for constructing digest
void encode(unsigned char *digest, WORD state[4]) {
	for (int i=0; i<16/4; ++i) {
		digest[4*i+0] = (unsigned char)((state[i] >> ( 0+(32*i))) & 0xff);
		digest[4*i+1] = (unsigned char)((state[i] >> ( 8+(32*i))) & 0xff);
		digest[4*i+2] = (unsigned char)((state[i] >> (16+(32*i))) & 0xff);
		digest[4*i+3] = (unsigned char)((state[i] >> (24+(32*i))) & 0xff);
	}
}

WORD plus(WORD a, WORD b) {
	return (a+b)%B2E32;
}

WORD rot_left(WORD a, int s) {
	return (a << s) | (a >> (32-s));
}

WORD aux_f(WORD x, WORD y, WORD z) {
	return ((x) & (y)) | ((!x) & (z));
}

WORD aux_g(WORD x, WORD y, WORD z) {
	return ((x) & (z)) | ((y) & (!z));
}

WORD aux_h(WORD x, WORD y, WORD z) {
	return (x) ^ (y) ^ (z);
}

WORD aux_i(WORD x, WORD y, WORD z) {
	return (y) ^ ((x) | (!z));
}

WORD round_1(WORD a, WORD b, WORD c, WORD d, WORD x_k, WORD t_i, int s) {
	WORD result;
	result = a + aux_f(b, c, d) + x_k + t_i;
	result = rot_left(result, s);
	result += b;
	return result;
}

WORD round_2(WORD a, WORD b, WORD c, WORD d, WORD x_k, WORD t_i, int s) {
	WORD result;
	result = a + aux_g(b, c, d) + x_k + t_i;
	result = rot_left(result, s);
	result += b;
	return result;
}

WORD round_3(WORD a, WORD b, WORD c, WORD d, WORD x_k, WORD t_i, int s) {
	WORD result;
	result = a + aux_h(b, c, d) + x_k + t_i;
	result = rot_left(result, s);
	result += b;
	return result;
}

WORD round_4(WORD a, WORD b, WORD c, WORD d, WORD x_k, WORD t_i, int s) {
	WORD result;
	result = a + aux_i(b, c, d) + x_k + t_i;
	result = rot_left(result, s);
	result += b;
	return result;
}

void printer(unsigned char *digest, size_t len) {
	for (int i=0; i<len; ++i) {
		printf("%02x", digest[i]);
	}
	putchar('\n');
}

void md5(char *m) {
	unsigned char *message = m;
	size_t message_len = my_strlen((const unsigned char *)message);
	size_t padding_len = message_len%56 == 0 ? 64 : 56-message_len%56;
	unsigned char bits[8];
	my_memset(bits, 0, 8);
	strbits(bits, message_len);

	size_t message_pp_len = message_len+padding_len+8;
	unsigned char message_pp[message_pp_len];

	my_memcpy(message_pp, message, message_len);
	my_memcpy(message_pp+message_len, PADDING, padding_len);
	my_memcpy(message_pp+message_len+padding_len, bits, 8);

	WORD state[4] = {
		0x67452301,
		0xefcdab89,
		0x98badcfe,
		0x10325476
	};

	for (int i=0; i<message_pp_len/16; ++i) {

		WORD x[16];
		my_memset((unsigned char *)x, 0, 16);
		for (int j=0; j<16; ++j) {
			x[j] = message_pp[i*16+j];
		}

		WORD a = state[0];
		WORD b = state[1];
		WORD c = state[2];
		WORD d = state[3];

		a = round_1(a, b, c, d, x[ 0], S11, 0xd76aa478);
		d = round_1(d, a, b, c, x[ 1], S12, 0xe8c7b756);
		c = round_1(c, d, a, b, x[ 2], S13, 0x242070db);
		b = round_1(b, c, d, a, x[ 3], S14, 0xc1bdceee);
		a = round_1(a, b, c, d, x[ 4], S11, 0xf57c0faf);
		d = round_1(d, a, b, c, x[ 5], S12, 0x4787c62a);
		c = round_1(c, d, a, b, x[ 6], S13, 0xa8304613);
		b = round_1(b, c, d, a, x[ 7], S14, 0xfd469501);
		a = round_1(a, b, c, d, x[ 8], S11, 0x698098d8);
		d = round_1(d, a, b, c, x[ 9], S12, 0x8b44f7af);
		c = round_1(c, d, a, b, x[10], S13, 0xffff5bb1);
		b = round_1(b, c, d, a, x[11], S14, 0x895cd7be);
		a = round_1(a, b, c, d, x[12], S11, 0x6b901122);
		d = round_1(d, a, b, c, x[13], S12, 0xfd987193);
		c = round_1(c, d, a, b, x[14], S13, 0xa679438e);
		b = round_1(b, c, d, a, x[15], S14, 0x49b40821);

		a = round_2(a, b, c, d, x[ 1], S21, 0xf61e2562);
		d = round_2(d, a, b, c, x[ 6], S22, 0xc040b340);
		c = round_2(c, d, a, b, x[11], S23, 0x265e5a51);
		b = round_2(b, c, d, a, x[ 0], S24, 0xe9b6c7aa);
		a = round_2(a, b, c, d, x[ 5], S21, 0xd62f105d);
		d = round_2(d, a, b, c, x[10], S22, 0x02441453);
		c = round_2(c, d, a, b, x[15], S23, 0xd8a1e681);
		b = round_2(b, c, d, a, x[ 4], S24, 0xe7d3fbc8);
		a = round_2(a, b, c, d, x[ 9], S21, 0x21e1cde6);
		d = round_2(d, a, b, c, x[14], S22, 0xc33707d6);
		c = round_2(c, d, a, b, x[ 3], S23, 0xf4d50d87);
		b = round_2(b, c, d, a, x[ 8], S24, 0x455a14ed);
		a = round_2(a, b, c, d, x[13], S21, 0xa9e3e905);
		d = round_2(d, a, b, c, x[ 2], S22, 0xfcefa3f8);
		c = round_2(c, d, a, b, x[ 7], S23, 0x676f02d9);
		b = round_2(b, c, d, a, x[12], S24, 0x8d2a4c8a);

		a = round_3(a, b, c, d, x[ 5], S31, 0xfffa3942);
		d = round_3(d, a, b, c, x[ 8], S32, 0x8771f681);
		c = round_3(c, d, a, b, x[11], S33, 0x6d9d6122);
		b = round_3(b, c, d, a, x[14], S34, 0xfde5380c);
		a = round_3(a, b, c, d, x[ 1], S31, 0xa4beea44);
		d = round_3(d, a, b, c, x[ 4], S32, 0x4bdecfa9);
		c = round_3(c, d, a, b, x[ 7], S33, 0xf6bb4b60);
		b = round_3(b, c, d, a, x[10], S34, 0xbebfbc70);
		a = round_3(a, b, c, d, x[13], S31, 0x289b7ec6);
		d = round_3(d, a, b, c, x[ 0], S32, 0xeaa127fa);
		c = round_3(c, d, a, b, x[ 3], S33, 0xd4ef3085);
		b = round_3(b, c, d, a, x[ 6], S34, 0x04881d05);
		a = round_3(a, b, c, d, x[ 9], S31, 0xd9d4d039);
		d = round_3(d, a, b, c, x[12], S32, 0xe6db99e5);
		c = round_3(c, d, a, b, x[15], S33, 0x1fa27cf8);
		b = round_3(b, c, d, a, x[ 2], S34, 0xc4ac5665);

		a = round_4(a, b, c, d, x[ 0], S41, 0xf4292244);
		d = round_4(d, a, b, c, x[ 7], S42, 0x432aff97);
		c = round_4(c, d, a, b, x[14], S43, 0xab9423a7);
		b = round_4(b, c, d, a, x[ 5], S44, 0xfc93a039);
		a = round_4(a, b, c, d, x[12], S41, 0x655b59c3);
		d = round_4(d, a, b, c, x[ 3], S42, 0x8f0ccc92);
		c = round_4(c, d, a, b, x[10], S43, 0xffeff47d);
		b = round_4(b, c, d, a, x[ 1], S44, 0x85845dd1);
		a = round_4(a, b, c, d, x[ 8], S41, 0x6fa87e4f);
		d = round_4(d, a, b, c, x[15], S42, 0xfe2ce6e0);
		c = round_4(c, d, a, b, x[ 6], S43, 0xa3014314);
		b = round_4(b, c, d, a, x[13], S44, 0x4e0811a1);
		a = round_4(a, b, c, d, x[ 4], S41, 0xf7537e82);
		d = round_4(d, a, b, c, x[11], S42, 0xbd3af235);
		c = round_4(c, d, a, b, x[ 2], S43, 0x2ad7d2bb);
		b = round_4(b, c, d, a, x[ 9], S44, 0xeb86d391);

		state[0] += a;
		state[1] += b;
		state[2] += c;
		state[3] += d;
	}
	unsigned char digest[16];
	encode(digest, state);
	printer(digest, 16);
}

int main() {
	md5("abcdef609043");
	md5("1234567890");
}