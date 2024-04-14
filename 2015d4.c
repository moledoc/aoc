#include <stdio.h>

#define MD5_IMPLEMENTATION
#include "md5.h"

int e1(char *base) {
	size_t base_len = md5_strlen(base);
	unsigned char digest[16];
	for (int i=0;i<1000000;++i) {
		char message[base_len+10];
		int n = snprintf(message, base_len+10, "%s%d", base, i);
		message[n] = '\0';
		md5(message, digest);
		if (digest[0]==0 && digest[1]==0 && digest[2] < 10) {
			return i;
		}
		md5_memset(digest, 0, 16);
	}
	return -1;
}


int e2(char *base) {
	size_t base_len = md5_strlen(base);
	unsigned char digest[16];
	for (int i=0;i<10000000;++i) {
		char message[base_len+10];
		int n = snprintf(message, base_len+10, "%s%d", base, i);
		message[n] = '\0';
		md5(message, digest);
		if (digest[0]==0 && digest[1]==0 && digest[2] == 0) {
			return i;
		}
		md5_memset(digest, 0, 16);
	}
	return -1;
}


int main(void) {
	printf("e1: %d\n", e1("bgvyzdsv"));
	printf("e2: %d\n", e2("bgvyzdsv"));
}