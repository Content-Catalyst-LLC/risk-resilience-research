program mobility_resilience_gap
  implicit none

  real :: forced_displacement_risk
  real :: trapped_population_risk
  real :: destination_stress
  real :: adaptive_mobility_capacity
  real :: resilience_gap

  forced_displacement_risk = 0.72
  trapped_population_risk = 0.24
  destination_stress = 0.48
  adaptive_mobility_capacity = 0.34

  resilience_gap = forced_displacement_risk + trapped_population_risk + destination_stress - adaptive_mobility_capacity
  if (resilience_gap < 0.0) resilience_gap = 0.0

  print *, "mobility_resilience_gap:", resilience_gap
end program mobility_resilience_gap
