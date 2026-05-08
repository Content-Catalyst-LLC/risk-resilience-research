program uncertainty_adjusted_risk
  implicit none

  real :: hazard_probability
  real :: expected_loss_index
  real :: probability_uncertainty
  real :: loss_uncertainty
  real :: expected_risk
  real :: combined_uncertainty
  real :: adjusted_risk

  hazard_probability = 0.72
  expected_loss_index = 0.78
  probability_uncertainty = 0.26
  loss_uncertainty = 0.34

  expected_risk = hazard_probability * expected_loss_index
  combined_uncertainty = (probability_uncertainty + loss_uncertainty) / 2.0
  adjusted_risk = expected_risk * (1.0 + combined_uncertainty)

  print *, "expected_risk:", expected_risk
  print *, "uncertainty_adjusted_risk:", adjusted_risk
end program uncertainty_adjusted_risk
