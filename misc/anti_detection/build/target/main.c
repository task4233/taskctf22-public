#include <stdio.h>

int main() {
  FILE *fp = fopen("flag.txt", "r");
  if (fp == NULL) {
    puts("cant open file");
    return -1;
  }

  char flag[0x20];
  fscanf(fp, "%s", flag);
  printf("flag: %s", flag);
  fclose(fp);
  return 0;
}
