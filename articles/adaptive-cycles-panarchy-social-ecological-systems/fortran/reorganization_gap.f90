program reorganization_gap
  implicit none

  real :: release_risk_index
  real :: revolt_cascade_pressure
  real :: resilience_trap_index
  real :: inequality_pressure
  real :: transformation_readiness
  real :: gap

  release_risk_index = 0.74
  revolt_cascade_pressure = 0.82
  resilience_trap_index = 0.70
  inequality_pressure = 0.76
  transformation_readiness = 0.44

  gap = (0.32 * release_risk_index + &
         0.26 * revolt_cascade_pressure + &
         0.22 * resilience_trap_index + &
         0.20 * inequality_pressure) * &
         (1.0 + 0.30 * inequality_pressure) - transformation_readiness

  if (gap < 0.0) gap = 0.0

  print *, "justice_weighted_reorganization_gap:", gap
end program reorganization_gap
