program stress_test_continuity_gap
  implicit none

  real :: stress_load
  real :: resilience_capacity
  real :: continuity_gap

  stress_load = 1.05
  resilience_capacity = 0.48

  continuity_gap = stress_load - resilience_capacity
  if (continuity_gap < 0.0) continuity_gap = 0.0

  print *, "service_continuity_gap:", continuity_gap
end program stress_test_continuity_gap
