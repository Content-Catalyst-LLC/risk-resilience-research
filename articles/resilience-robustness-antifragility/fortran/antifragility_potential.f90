program antifragility_potential
  implicit none

  real :: learning
  real :: experimentation
  real :: optionality
  real :: modularity
  real :: containment
  real :: monitoring
  real :: antifragility

  learning = 0.86
  experimentation = 0.88
  optionality = 0.84
  modularity = 0.72
  containment = 0.82
  monitoring = 0.62

  antifragility = 0.24 * learning + 0.22 * experimentation + 0.20 * optionality + &
                  0.16 * modularity + 0.10 * containment + 0.08 * monitoring

  print *, "antifragility_potential:", antifragility
end program antifragility_potential
