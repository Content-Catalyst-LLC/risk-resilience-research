#include <stdio.h>

int main(void) {
    double nbs_integrity = 0.56;
    double social_legitimacy = 0.60;
    double livelihood_benefit = 0.52;

    double buffer_effectiveness =
        nbs_integrity *
        (1.0 + 0.22 * social_legitimacy) *
        (1.0 + 0.18 * livelihood_benefit);

    if (buffer_effectiveness > 1.5) {
        buffer_effectiveness = 1.5;
    }

    printf("buffer_effectiveness: %.3f\n", buffer_effectiveness);
    return 0;
}
