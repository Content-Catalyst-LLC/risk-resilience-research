program threshold_proximity
  implicit none

  real :: threshold_proximity_score
  real :: hidden_stress_index
  real :: drift_index
  real :: system_criticality
  real :: latent_instability

  threshold_proximity_score = 0.68
  hidden_stress_index = 0.60
  drift_index = 0.58
  system_criticality = 0.86

  latent_instability = 0.38 * threshold_proximity_score + &
                       0.26 * hidden_stress_index + &
                       0.20 * drift_index + &
                       0.16 * system_criticality

  print *, "latent_instability:", latent_instability
end program threshold_proximity
