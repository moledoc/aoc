#include <stdio.h>
#include <string.h>
#include <limits.h>

typedef unsigned short int UINT2; // 16-bit
typedef unsigned long int UINT4; // 32-bit

/*
unsigned int T[64];
for (double i=0; i<64; ++i) {
	unsigned int tmp = 4294967296 * sin(i+1);
	T[(int)i] = tmp < 0 ? -tmp : tmp;
}
*/
static unsigned int T[64] = {0xd76aa478,0xe8c7b756,0x242070db,0x3e423112,0xa83f051,0xb87839d6,0xa8304613,0xfd469501,0x698098d8,0x74bb0851,0xa44f,0x76a32842,0x6b901122,0xfd987193,0xa679438e,0xb64bf7df,0x9e1da9e,0x3fbf4cc0,0x265e5a51,0xe9b6c7aa,0xd62f105d,0xfdbbebad,0x275e197f,0x182c0438,0xde1e321a,0xc33707d6,0xf4d50d87,0x455a14ed,0x561c16fb,0x3105c08,0x9890fd27,0x8d2a4c8a,0xfffa3942,0x8771f681,0x92629ede,0x21ac7f4,0x5b4115bc,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,0xd764813a,0x155ed806,0x2b10cf7b,0x4881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0x3b53a99b,0xbd6ddbc,0xbcd50069,0xab9423a7,0xfc93a039,0x655b59c3,0x70f3336e,0x100b83,0x7a7ba22f,0x6fa87e4f,0xfe2ce6e0,0xa3014314,0xb1f7ee5f,0x8ac817e,0x42c50dcb,0x2ad7d2bb,0xeb86d391};

// static unsigned int b2e32 = 0x77359400;


unsigned F(UINT4 x, UINT4 y, UINT4 z) {
	return (x & y) | ((~x) & z);
}
unsigned G(UINT4 x, UINT4 y, UINT4 z) {
	return (x & y) | (y & (~z));
}
unsigned H(UINT4 x, UINT4 y, UINT4 z) {
	return x ^ y ^ z;
}
unsigned I(UINT4 x, UINT4 y, UINT4 z) {
	return y ^ (x | (~z));
}
unsigned rot_left(UINT4 x, unsigned s) {
	return (x<<s) | (x >> (32-s));
}

unsigned round1(UINT4 a, UINT4 b, UINT4 c, UINT4 d, UINT4 x, unsigned s, UINT4 t) {
	a += F(b,c,d) + x + (UINT4)t;
	a = rot_left(a, s);
	a += b;
	return a;	
}

unsigned round2(UINT4 a, UINT4 b, UINT4 c, UINT4 d, UINT4 x, unsigned s, UINT4 t) {
	a += G(b,c,d) + x + (UINT4)t;
	a = rot_left(a, s);
	a += b;
	return a;	
}

unsigned round3(UINT4 a, UINT4 b, UINT4 c, UINT4 d, UINT4 x, unsigned s, UINT4 t) {
	a += H(b,c,d) + x + (UINT4)t;
	a = rot_left(a, s);
	a += b;
	return a;	
}

unsigned round4(UINT4 a, UINT4 b, UINT4 c, UINT4 d, UINT4 x, unsigned s, UINT4 t) {
	a += I(b,c,d) + x + (UINT4)t;
	a = rot_left(a, s);
	a += b;
	return a;	
}

void md5_memset(unsigned char *dest, char *src, size_t size) {
	for (int i=0; i<size; ++i) {
		dest[i] = src[i];
	}
}

static void encode (unsigned char *output, UINT4 *input, unsigned int len) {
	for (unsigned int i = 0, j = 0; j < len; i++, j += 4) {
		output[j] = (unsigned char)(input[i] & 0xff);
		output[j+1] = (unsigned char)((input[i] >> 8) & 0xff);
		output[j+2] = (unsigned char)((input[i] >> 16) & 0xff);
		output[j+3] = (unsigned char)((input[i] >> 24) & 0xff);
	}
}

static void printer(unsigned char *digest, size_t len) {
	for (int i=0; i<16; ++i) {
		printf("%02x", digest[i]);
	}
	putchar('\n');
}

// https://www.rfc-editor.org/rfc/rfc1321
void md5(char *in) {

	size_t in_len = strlen(in);
	size_t padding_len = (in_len<<3)%512==512-64 ? 512>>3 : (512-64-(in_len<<3)%512)>>3;
	size_t bits_len = 8;

	size_t buffer_len = in_len + padding_len + bits_len;
	unsigned char buffer[buffer_len];

	md5_memset(buffer, in, in_len);

	memset(buffer+in_len, 0x00 + '0', padding_len);
	buffer[in_len] = '1'; // 0x80;

	unsigned char bits[bits_len];
	UINT4 count[2];
	count[0] = in_len<<3; count[1] = 0;
	encode(bits, count, 8);
	md5_memset(buffer+in_len+padding_len, (char *)bits, bits_len);

	// printf("%s %lu\n", buffer, buffer_len);
	

	UINT4 a0 = 0x67452301;
	UINT4 b0 = 0xefcdab89;
	UINT4 c0 = 0x98bacdfe;
	UINT4 d0 = 0x10325476;

	printf("%s %ld\n", buffer, buffer_len);

	if ((buffer_len<<3)%16!=0) {
		fprintf(stderr, "buffer_len<<3 is not mod16: %lu\n", buffer_len<<3);
		return; // TODO: error better
	}

	// processing each 16 (32-bit) word block, i.e.
	// 16-word block is 16x32=512 bits;
	// 8 bits make a byte
	// 512/8=64
	for (int i=0; i<buffer_len/64; ++i) { 

		UINT4 a = a0;
		UINT4 b = b0;
		UINT4 c = c0;
		UINT4 d = d0;
		UINT4 x[16];
		memset(x, 0, sizeof(x));

		// i*64 because we want to decode each 16-word block (i.e. 64 bytes) to x on each iteration.
		// this loop has 16 iterations: j=0,4,8,...,64
		int block = 64;
		for (int k=0, j=0; j<64; k+=1, j+=4) {
			x[k] = ((UINT4)buffer[i*block+j] << 0) | (((UINT4)buffer[i*block+j+1]) << 8) |
   (((UINT4)buffer[i*block+j+2]) << 16) | (((UINT4)buffer[i*block+j+3]) << 24);
			// printf("%d %d %d -- %lu\n", i,k, i*block+j+3, x[k]);
		}

		a = round1(a, b, c, d, x[ 0],  7, T[ 1]);
		d = round1(d, a, b, c, x[ 1], 12, T[ 2]);
		c = round1(c, d, a, b, x[ 2], 17, T[ 3]);
		b = round1(b, c, d, a, x[ 3], 22, T[ 4]);
		a = round1(a, b, c, d, x[ 4],  7, T[ 5]);
		d = round1(d, a, b, c, x[ 5], 12, T[ 6]);
		c = round1(c, d, a, b, x[ 6], 17, T[ 7]);
		b = round1(b, c, d, a, x[ 7], 22, T[ 8]);
		a = round1(a, b, c, d, x[ 8],  7, T[ 9]);
		d = round1(d, a, b, c, x[ 9], 12, T[10]);
		c = round1(c, d, a, b, x[10], 17, T[11]);
		b = round1(b, c, d, a, x[11], 22, T[12]);
		a = round1(a, b, c, d, x[12],  7, T[13]);
		d = round1(d, a, b, c, x[13], 12, T[14]);
		c = round1(c, d, a, b, x[14], 17, T[15]);
		b = round1(b, c, d, a, x[15], 22, T[16]);

		a = round2(a, b, c, d, x[ 1],  5, T[17]);
		d = round2(d, a, b, c, x[ 6],  9, T[18]);
		c = round2(c, d, a, b, x[11], 14, T[19]);
		b = round2(b, c, d, a, x[ 0], 20, T[20]);
		a = round2(a, b, c, d, x[ 5],  5, T[21]);
		d = round2(d, a, b, c, x[10],  9, T[22]);
		c = round2(c, d, a, b, x[15], 14, T[23]);
		b = round2(b, c, d, a, x[ 4], 20, T[24]);
		a = round2(a, b, c, d, x[ 9],  5, T[25]);
		d = round2(d, a, b, c, x[14],  9, T[26]);
		c = round2(c, d, a, b, x[ 3], 14, T[27]);
		b = round2(b, c, d, a, x[ 8], 20, T[28]);
		a = round2(a, b, c, d, x[13],  5, T[29]);
		d = round2(d, a, b, c, x[ 2],  9, T[30]);
		c = round2(c, d, a, b, x[ 7], 14, T[31]);
		b = round2(b, c, d, a, x[12], 20, T[32]);

		a = round3(a, b, c, d, x[ 5],  4, T[33]);
		d = round3(d, a, b, c, x[ 8], 11, T[34]);
		c = round3(c, d, a, b, x[11], 16, T[35]);
		b = round3(b, c, d, a, x[14], 23, T[36]);
		a = round3(a, b, c, d, x[ 1],  4, T[37]);
		d = round3(d, a, b, c, x[ 4], 11, T[38]);
		c = round3(c, d, a, b, x[ 7], 16, T[39]);
		b = round3(b, c, d, a, x[10], 23, T[40]);
		a = round3(a, b, c, d, x[13],  4, T[41]);
		d = round3(d, a, b, c, x[ 0], 11, T[42]);
		c = round3(c, d, a, b, x[ 3], 16, T[43]);
		b = round3(b, c, d, a, x[ 6], 23, T[44]);
		a = round3(a, b, c, d, x[ 9],  4, T[45]);
		d = round3(d, a, b, c, x[12], 11, T[46]);
		c = round3(c, d, a, b, x[15], 16, T[47]);
		b = round3(b, c, d, a, x[ 2], 23, T[48]);

		a = round4(a, b, c, d, x[ 0],  6, T[49]);
		d = round4(d, a, b, c, x[ 7], 10, T[50]);
		c = round4(c, d, a, b, x[14], 15, T[51]);
		b = round4(b, c, d, a, x[ 5], 21, T[52]);
		a = round4(a, b, c, d, x[12],  6, T[53]);
		d = round4(d, a, b, c, x[ 3], 10, T[54]);
		c = round4(c, d, a, b, x[10], 15, T[55]);
		b = round4(b, c, d, a, x[ 1], 21, T[56]);
		a = round4(a, b, c, d, x[ 8],  6, T[57]);
		d = round4(d, a, b, c, x[15], 10, T[58]);
		c = round4(c, d, a, b, x[ 6], 15, T[59]);
		b = round4(b, c, d, a, x[13], 21, T[60]);
		a = round4(a, b, c, d, x[ 4],  6, T[61]);
		d = round4(d, a, b, c, x[11], 10, T[62]);
		c = round4(c, d, a, b, x[ 2], 15, T[63]);
		b = round4(b, c, d, a, x[ 9], 21, T[64]);


		a0 += a;
		b0 += b;
		c0 += c;
		d0 += d;
		memset(x, 0, sizeof(x));
	}

	unsigned char digest[16];
	UINT4 state[4];
	state[0] = a0; state[1] = b0; state[2] = c0; state[3] = d0;
	encode(digest, state, 16);
	printer(digest, 16);
}

int main(void) {
	md5("abcdef609043_111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111");
}