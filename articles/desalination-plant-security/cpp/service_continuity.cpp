#include <iostream>

bool meets_priority_demand(
    double desalination_output,
    double outage_fraction,
    double alternative_supply,
    double emergency_transfer,
    double losses,
    double priority_demand
) {
    const double outage_supply = ((1.0 - outage_fraction) * desalination_output)
                               + alternative_supply
                               + emergency_transfer
                               - losses;
    return outage_supply >= priority_demand;
}

int main() {
    const bool stable = meets_priority_demand(420.0, 0.25, 85.0, 40.0, 28.0, 360.0);
    std::cout << "Synthetic system meets priority demand under outage: "
              << (stable ? "true" : "false") << "\n";
    return 0;
}
