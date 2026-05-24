program service_continuity
  implicit none

  real :: desalination_output, outage_fraction, alternative_supply
  real :: emergency_transfer, losses, priority_demand, outage_supply
  logical :: stable

  desalination_output = 420.0
  outage_fraction = 0.25
  alternative_supply = 85.0
  emergency_transfer = 40.0
  losses = 28.0
  priority_demand = 360.0

  outage_supply = ((1.0 - outage_fraction) * desalination_output) + &
                  alternative_supply + emergency_transfer - losses

  stable = outage_supply >= priority_demand

  print *, "Synthetic system meets priority demand under outage:", stable
end program service_continuity
