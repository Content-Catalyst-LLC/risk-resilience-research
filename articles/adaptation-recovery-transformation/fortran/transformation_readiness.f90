program transformation_readiness
  implicit none

  real :: transformation_readiness_score
  real :: governance_capacity
  real :: learning_capacity
  real :: public_legitimacy
  real :: social_protection_capacity
  real :: transformation_score

  transformation_readiness_score = 0.58
  governance_capacity = 0.40
  learning_capacity = 0.46
  public_legitimacy = 0.44
  social_protection_capacity = 0.32

  transformation_score = 0.34 * transformation_readiness_score + &
                         0.22 * governance_capacity + &
                         0.18 * learning_capacity + &
                         0.14 * public_legitimacy + &
                         0.12 * social_protection_capacity

  print *, "transformation_score:", transformation_score
end program transformation_readiness
