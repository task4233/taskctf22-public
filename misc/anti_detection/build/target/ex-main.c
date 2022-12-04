#include <stdio.h>

int main() {
  FILE *fp = fopen("*.txt", "r");
  if (fp == NULL) return -1;

  char flag[0x30];
  fscanf(fp, "%s", flag);
  printf("flag: %s", flag);
  fclose(fp);
  return 0;
}
