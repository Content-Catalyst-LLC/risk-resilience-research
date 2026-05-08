#include <iostream>
#include <algorithm>

int main() {
    double food_system_fragility = 0.72;
    double food_access_vulnerability = 0.80;
    double trade_dependency = 0.58;
    double cross_sector_linkage = 0.72;
    double inequality_pressure = 0.80;
    double resilience_capacity = 0.42;

    double cascading_food_risk =
        (food_system_fragility + food_access_vulnerability) *
        (1.0 + 0.30 * trade_dependency) *
        (1.0 + 0.30 * cross_sector_linkage);

    double justice_weighted_food_risk =
        cascading_food_risk * (1.0 + 0.35 * inequality_pressure);

    double gap = std::max(0.0, justice_weighted_food_risk - resilience_capacity);

    std::cout << "cascading_food_risk: " << cascading_food_risk << std::endl;
    std::cout << "justice_weighted_food_risk: " << justice_weighted_food_risk << std::endl;
    std::cout << "food_resilience_gap: " << gap << std::endl;
    return 0;
}
