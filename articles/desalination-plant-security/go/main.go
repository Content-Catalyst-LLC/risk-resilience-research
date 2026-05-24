package main

import "fmt"

func MeetsPriorityDemand(
	desalinationOutput float64,
	outageFraction float64,
	alternativeSupply float64,
	emergencyTransfer float64,
	losses float64,
	priorityDemand float64,
) bool {
	outageSupply := ((1.0 - outageFraction) * desalinationOutput) +
		alternativeSupply + emergencyTransfer - losses
	return outageSupply >= priorityDemand
}

func main() {
	stable := MeetsPriorityDemand(420.0, 0.25, 85.0, 40.0, 28.0, 360.0)
	fmt.Printf("Synthetic system meets priority demand under outage: %t\n", stable)
}
