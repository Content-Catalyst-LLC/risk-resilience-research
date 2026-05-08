program resilience_gap
  implicit none

  real :: propagation_pressure
  real :: efficiency_fragility_pressure
  real :: social_vulnerability
  real :: system_criticality
  real :: continuity_capacity
  real :: gap

  propagation_pressure = 1.40
  efficiency_fragility_pressure = 0.72
  social_vulnerability = 0.58
  system_criticality = 0.92
  continuity_capacity = 0.43

  gap = (0.34 * propagation_pressure + &
         0.28 * efficiency_fragility_pressure + &
         0.22 * social_vulnerability + &
         0.16 * system_criticality) * &
         (1.0 + 0.30 * social_vulnerability) - continuity_capacity

  if (gap < 0.0) gap = 0.0

  print *, "justice_weighted_resilience_gap:", gap
end program resilience_gap
