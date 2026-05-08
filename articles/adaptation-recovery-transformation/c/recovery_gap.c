#include <stdio.h>

int main(void) {
    double disruption_severity = 0.86;
    double recovery_score = 0.38;
    double recovery_gap = disruption_severity - recovery_score;

    if (recovery_gap < 0.0) {
        recovery_gap = 0.0;
    }

    printf("recovery_gap: %.3f\n", recovery_gap);
    return 0;
}
