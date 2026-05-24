package main

import "fmt"

func LocalRedundancyRatio(localOutputKg float64, essentialDemandKg float64) float64 {
	if essentialDemandKg <= 0 {
		return 0
	}
	return localOutputKg / essentialDemandKg
}

func ShockSupply(externalSupplyKg float64, shockFraction float64, localOutputKg float64, bufferKg float64, lossesKg float64) float64 {
	return ((1.0 - shockFraction) * externalSupplyKg) + localOutputKg + bufferKg - lossesKg
}

func main() {
	rho := LocalRedundancyRatio(8200.0, 52000.0)
	supply := ShockSupply(43800.0, 0.25, 8200.0, 2000.0, 500.0)

	fmt.Printf("Local redundancy ratio: %.3f\n", rho)
	fmt.Printf("Shock scenario available supply: %.2f kg\n", supply)
}
