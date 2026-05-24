program food_redundancy
  implicit none

  real :: local_output_kg, essential_demand_kg, rho
  real :: external_supply_kg, shock_fraction, buffer_kg, losses_kg, supply

  local_output_kg = 8200.0
  essential_demand_kg = 52000.0
  external_supply_kg = 43800.0
  shock_fraction = 0.25
  buffer_kg = 2000.0
  losses_kg = 500.0

  rho = local_output_kg / essential_demand_kg
  supply = ((1.0 - shock_fraction) * external_supply_kg) + local_output_kg + buffer_kg - losses_kg

  print *, "Local redundancy ratio:", rho
  print *, "Shock scenario available supply:", supply, "kg"
end program food_redundancy
