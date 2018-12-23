#include <stdio.h>

int main() {
        long long r0 = 0;
        long long r1 = 0;
        long long r2 = 0;
        long long r3 = 0;
        long long r4 = 0;
        long long r5 = 0;

        goto seventeen;

one:
        r2 = 2;
        r1 = 1;
three:
        r4 = r2 * r1;
        r4 = r3 == r4;
        if (r4)
          goto seven
        goto eight;
seven:
        r0 += r2;
eight:
        r1++;
        r4 = r1 > r3;
        if (r4)
          goto twelve;
        goto three;
twelve:
        r2 += 1;

        if (r2 > r3)
          goto sixteen;

        goto one;

sixteen:
        printf("MULR 5 5\n");
        printf("[%lld %lld %lld %lld %lld %lld]\n", r0, r1, r2, r3, r4, r5);
        return 0;

seventeen:
        r3 += 2;
        r3 = r3 * r3;
        r3 = r5 * r3;
        r3 = r3 * 11;
        r4 += 6;  // twentyone
        r4 = r4 * r5;
        r4 += 5;
        r3 = r3 + r4;

}
