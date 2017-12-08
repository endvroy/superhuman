#include <stdio.h>

int main(int argc, const char* argv[]) {
    int mem[2] = {-1, -1};
    // inbox
    int a = 2;
    mem[0] = a;
    // add 0 0 1
    a = mem[0];
    a = a + mem[0];
    mem[1] = a;
    // add 1 0 0
    a = mem[1];
    a = a + mem[0];
    mem[0] = a;
    // add 0 1 1
    a = mem[0];
    a = a + mem[1];
    mem[1] = a;
    // add 1 0 0
    a = mem[1];
    a = a + mem[0];
    mem[0] = a;
    // outbox 0
    a = mem[0];
    printf("Result = %d\n", a);
}