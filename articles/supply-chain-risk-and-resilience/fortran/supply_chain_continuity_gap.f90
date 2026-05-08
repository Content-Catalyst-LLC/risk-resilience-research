program supply_chain_continuity_gap
  implicit none

  real :: criticality
  real :: shortage_risk
  real :: resilience_buffer_capacity
  real :: continuity_gap

  criticality = 0.96
  shortage_risk = 0.84
  resilience_buffer_capacity = 0.32

  continuity_gap = criticality + shortage_risk - resilience_buffer_capacity
  if (continuity_gap < 0.0) continuity_gap = 0.0

  print *, "service_continuity_gap:", continuity_gap
end program supply_chain_continuity_gap
