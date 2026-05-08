program failure_gap
  implicit none

  real :: failure_risk
  real :: resilience_capacity
  real :: gap

  failure_risk = 0.82
  resilience_capacity = 0.45

  gap = failure_risk - resilience_capacity
  if (gap < 0.0) gap = 0.0

  print *, "failure_gap:", gap
end program failure_gap
