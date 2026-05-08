program service_continuity_gap
  implicit none

  real :: service_demand_under_stress
  real :: resilience_capacity
  real :: continuity_gap

  service_demand_under_stress = 0.88
  resilience_capacity = 0.46

  continuity_gap = service_demand_under_stress - resilience_capacity
  if (continuity_gap < 0.0) continuity_gap = 0.0

  print *, "service_continuity_gap:", continuity_gap
end program service_continuity_gap
