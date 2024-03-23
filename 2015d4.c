#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

void length_in_binary(size_t len, char *binary) {
	int len_cpy = (int)len;
	size_t blen = 0;
	while ( len_cpy >>= 1 > 0) {
		++blen;
	}
	blen += 1; // +1 for index 0;
	len_cpy = (char)len; 
	for (int i=0; i<blen;++i) {
		binary[64-i-1] = len_cpy & 1 ? '1' : '0';
		len_cpy >>= 1;
	}
}

void hex_to_binary(int hex, int *binary) {
	int hex_cpy = (int)hex;
	size_t blen = 0;
	while ( hex_cpy >>= 1 > 0) {
		++blen;
	}
	blen += 1; // +1 for index 0;
	hex_cpy = (char)hex;
	for (int i=0; i<8-blen; ++i) {
		binary[i] = 0;
	}
	for (int i=0; i<blen;++i) {
		binary[8-i-1] = hex_cpy & 1 ? 1 : 0;
		hex_cpy >>= 1;
	}

}

void F(int x[], int y[], int z[], int out[]){
	for (int i=0; i<32; ++i) {
		out[i] = (x[i] & y[i]) | ((~x[i]) & z[i]);
		// out[i] = x[i] ? y[i] : z[i];
	}
}
void G(int x[], int y[], int z[], int out[]){
	for (int i=0; i<32; ++i) {
		out[i] = (x[i] & z[i]) | (y[i] & (~z[i]));
	}
}
void H(int x[], int y[], int z[], int out[]){
	for (int i=0; i<32; ++i) {
		out[i] = x[i] ^ y[i] ^ z[i];
	}
}
void I(int x[], int y[], int z[], int out[]){
	for (int i=0; i<32; ++i) {
		out[i] = y[i] ^ (x[i] | (~z[i]));
	}
}

float absf(float x) {
	if (x < 0) {
		return -x;
	}
	return x;
}

void backup_register(int dest[], int src[]) {
	for (int i=0; i<32; ++i) {
		dest[i] = src[i];
	}
}

void add_registers(int register_target[], int register_adder[]){
	for (int i=0; i<32; ++i) {
		register_target[i] += register_adder[i];
	}
}

void add_scalar(int register_target[], unsigned int scalar) {
	unsigned int modulo = (unsigned int)pow(2, 32);
	for (int i=0; i<32; ++i) {
		register_target[i] = ((unsigned) register_target[i] + scalar)%modulo;
	}
}

void rot_left(int arr[], int s) {
	int tmp[s];
	for (int i=0; i<s; ++i) {
		tmp[i] = arr[i];
	}
	for (int i=0; i<32-s; ++i) {
		arr[i] = arr[i+s];
	}
	for (int i=0; i<s; ++i) {
		arr[32-s+i] = tmp[i];
	}
}

void print_register(int arr[]) {
	for (int i=0; i<32; ++i) {
		printf("%d", arr[i]);
	}
	putchar('\n');
}

void round1(int X[], unsigned int T[], int a[], int b[], int c[], int d[], int k, int s, int i){
	// a = ((a+F(b,c,d)+X[k]+T[i]) <<< s) + b;
	int out[32];
	F(b,c,d, out);
	add_registers(a, out);
	add_scalar(a, X[k]);
	add_scalar(a, T[i]);
	rot_left(a, s);
	add_registers(a, b);
}

void round2(int X[], unsigned int T[], int a[], int b[], int c[], int d[], int k, int s, int i){
	// a = b + ((a + G(b,c,d) + X[k] + T[i]) <<< s);
	int out[32];
	G(b,c,d, out);
	add_registers(a, out);
	add_scalar(a, X[k]);
	add_scalar(a, T[i]);
	rot_left(a, s);
	add_registers(a, b);
}

void round3(int X[], unsigned int T[], int a[], int b[], int c[], int d[], int k, int s, int i){
	// a = b + ((a + H(b,c,d) + X[k] + T[i]) <<< s);
	int out[32];
	H(b,c,d, out);
	add_registers(a, out);
	add_scalar(a, X[k]);
	add_scalar(a, T[i]);
	rot_left(a, s);
	add_registers(a, b);
}

void round4(int X[], unsigned int T[], int a[], int b[], int c[], int d[], int k, int s, int i){
	// a = b + ((a + I(b,c,d) + X[k] + T[i]) <<< s);
	int out[32];
	I(b,c,d, out);
	add_registers(a, out);
	add_scalar(a, X[k]);
	add_scalar(a, T[i]);
	rot_left(a, s);
	add_registers(a, b);
}

// https://www.rfc-editor.org/rfc/rfc1321
char *md5(char *in) {
	size_t in_len = strlen(in);
	int padding = 512-in_len%(512)-64;
	int length = 64;
	size_t digest_len = in_len+padding+length;
	char *digest = malloc(digest_len*sizeof(char));
	memset(digest, '0', in_len+padding+length);
	strncpy(digest, in, in_len);
	digest[in_len]='1'; 
	length_in_binary(in_len, digest+in_len+padding);

	int a_hex[4] = {0x01, 0x23, 0x45, 0x67};
	int b_hex[4] = {0x89, 0xab, 0xcd, 0xef};
	int c_hex[4] = {0xfe, 0xdc, 0xba, 0x98};
	int d_hex[4] = {0x76, 0x54, 0x32, 0x10};

	int a[32], b[32], c[32], d[32];
	for (int i=0; i<32; i+=8) {
		hex_to_binary(a_hex[i/8], a+i);
		hex_to_binary(b_hex[i/8], b+i);
		hex_to_binary(c_hex[i/8], c+i);
		hex_to_binary(d_hex[i/8], d+i);
	}

	unsigned int T[64];
	for (float i=0; i<64; ++i) {
		T[(int)i] = (unsigned int)(4294967296 * absf(sinf((float)i+1)));
	}

	for (int i=0; i<digest_len/16-1; ++i) {
		int X[16];
		for (int j=0; j<16; ++j) {
			X[j] = digest[i*16+j];
		}

		int aa[32], bb[32], cc[32], dd[32];
		backup_register(aa, a);
		backup_register(bb, b);
		backup_register(cc, c);
		backup_register(dd, d);

		// round 1
		round1(X,T,a,b,c,d,0,7,1);
		round1(X,T,d,a,b,c,1,12,2);
		round1(X,T,c,d,a,b,2,17,3);
		round1(X,T,b,c,d,a,3,22,4);
		round1(X,T,a,b,c,d,4,7,5);
		round1(X,T,d,a,b,c,5,12,6);
		round1(X,T,c,d,a,b,6,17,7);
		round1(X,T,b,c,d,a,7,22,8);
		round1(X,T,a,b,c,d,8,7,9);
		round1(X,T,d,a,b,c,9,12,10);
		round1(X,T,c,d,a,b,10,17,11);
		round1(X,T,b,c,d,a,11,22,12);
		round1(X,T,a,b,c,d,12,7,13);
		round1(X,T,d,a,b,c,13,12,14);
		round1(X,T,c,d,a,b,14,17,15);
		round1(X,T,b,c,d,a,15,22,16);

		// round 2
		round2(X,T,a,b,c,d,1,5,17);
		round2(X,T,d,a,b,c,6,9,18);
		round2(X,T,c,d,a,b,11,14,19);
		round2(X,T,b,c,d,a,0,20,20);
		round2(X,T,a,b,c,d,5,5,21);
		round2(X,T,d,a,b,c,10,9,22);
		round2(X,T,c,d,a,b,15,14,23);
		round2(X,T,b,c,d,a,4,20,24);
		round2(X,T,a,b,c,d,9,5,25);
		round2(X,T,d,a,b,c,14,9,26);
		round2(X,T,c,d,a,b,3,14,27);
		round2(X,T,b,c,d,a,8,20,28);
		round2(X,T,a,b,c,d,13,5,29);
		round2(X,T,d,a,b,c,2,9,30);
		round2(X,T,c,d,a,b,7,14,31);
		round2(X,T,b,c,d,a,12,20,32);

		// round 3
		round3(X,T,a,b,c,d,5,4,33);
		round3(X,T,d,a,b,c,8,11,34);
		round3(X,T,c,d,a,b,11,16,35);
		round3(X,T,b,c,d,a,14,23,36);
		round3(X,T,a,b,c,d,1,4,37);
		round3(X,T,d,a,b,c,4,11,38);
		round3(X,T,c,d,a,b,7,16,39);
		round3(X,T,b,c,d,a,10,23,40);
		round3(X,T,a,b,c,d,13,4,41);
		round3(X,T,d,a,b,c,0,11,42);
		round3(X,T,c,d,a,b,3,16,43);
		round3(X,T,b,c,d,a,6,23,44);
		round3(X,T,a,b,c,d,9,4,45);
		round3(X,T,d,a,b,c,12,11,46);
		round3(X,T,c,d,a,b,15,16,47);
		round3(X,T,b,c,d,a,2,23,48);

		// round 4
		round4(X,T,a,b,c,d,0,6,49);
		round4(X,T,d,a,b,c,7,10,50);
		round4(X,T,c,d,a,b,14,15,51);
		round4(X,T,b,c,d,a,5,21,52);
		round4(X,T,a,b,c,d,12,6,53);
		round4(X,T,d,a,b,c,3,10,54);
		round4(X,T,c,d,a,b,10,15,55);
		round4(X,T,b,c,d,a,1,21,56);
		round4(X,T,a,b,c,d,8,6,57);
		round4(X,T,d,a,b,c,15,10,58);
		round4(X,T,c,d,a,b,6,15,59);
		round4(X,T,b,c,d,a,13,21,60);
		round4(X,T,a,b,c,d,4,6,61);
		round4(X,T,d,a,b,c,11,10,62);
		round4(X,T,c,d,a,b,2,15,63);
		round4(X,T,b,c,d,a,9,21,64);

		add_registers(aa, a);
		add_registers(bb, b);
		add_registers(cc, c);
		add_registers(dd, d);
	}

	char *msg = malloc(128*sizeof(char));
	for (int i=0; i<32; ++i) {
		msg[i+32*0] = (char)a[32-1-i];
		msg[i+32*1] = (char)b[32-1-i];
		msg[i+32*2] = (char)c[32-1-i];
		msg[i+32*3] = (char)d[32-1-i];
	}

	return msg;
}

int main(void) {
	char *hash = md5("abcdef609043");
	printf("%s\n", hash);
	free(hash);
}