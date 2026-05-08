package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	HazardPressure              float64 `json:"hazard_pressure"`
	LivelihoodStress            float64 `json:"livelihood_stress"`
	ConflictInsecurityPressure  float64 `json:"conflict_insecurity_pressure"`
	Exposure                    float64 `json:"exposure"`
	SocialVulnerability          float64 `json:"social_vulnerability"`
	AdaptiveCapacity            float64 `json:"adaptive_capacity"`
	MobilityResources           float64 `json:"mobility_resources"`
	ProtectionAccess            float64 `json:"protection_access"`
	MigrationNetworkStrength    float64 `json:"migration_network_strength"`
	DestinationServiceCapacity   float64 `json:"destination_service_capacity"`
	HostCommunitySupport        float64 `json:"host_community_support"`
	RecoveryCapacity            float64 `json:"recovery_capacity"`
	ArrivalPressure             float64 `json:"arrival_pressure"`
}

type Result struct {
	MobilityPressure          float64 `json:"mobility_pressure"`
	AdaptiveMobilityCapacity float64 `json:"adaptive_mobility_capacity"`
	ForcedDisplacementRisk   float64 `json:"forced_displacement_risk"`
	TrappedPopulationRisk    float64 `json:"trapped_population_risk"`
	DestinationStress         float64 `json:"destination_stress"`
	MobilityResilienceGap     float64 `json:"mobility_resilience_gap"`
}

func clamp(value float64, lower float64, upper float64) float64 {
	return math.Max(lower, math.Min(upper, value))
}

func score(p Profile) Result {
	mobilityPressure := 0.22*p.HazardPressure +
		0.20*p.LivelihoodStress +
		0.20*p.ConflictInsecurityPressure +
		0.18*p.Exposure +
		0.20*p.SocialVulnerability

	adaptiveCapacity := 0.16*p.AdaptiveCapacity +
		0.15*p.MobilityResources +
		0.16*p.ProtectionAccess +
		0.14*p.MigrationNetworkStrength +
		0.14*p.DestinationServiceCapacity +
		0.13*p.HostCommunitySupport +
		0.12*p.RecoveryCapacity

	forcedRisk := mobilityPressure *
		(1 + 0.35*p.SocialVulnerability) *
		(1 - 0.45*adaptiveCapacity)

	trappedRisk := math.Max(
		0,
		mobilityPressure-p.MobilityResources-p.ProtectionAccess-p.MigrationNetworkStrength,
	)

	destinationStress := p.ArrivalPressure /
		(0.35 + p.DestinationServiceCapacity + p.HostCommunitySupport + p.RecoveryCapacity)
	destinationStress = clamp(destinationStress, 0, 1.5)

	gap := math.Max(0, forcedRisk+trappedRisk+destinationStress-adaptiveCapacity)

	return Result{
		MobilityPressure: mobilityPressure,
		AdaptiveMobilityCapacity: adaptiveCapacity,
		ForcedDisplacementRisk: forcedRisk,
		TrappedPopulationRisk: trappedRisk,
		DestinationStress: destinationStress,
		MobilityResilienceGap: gap,
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	var profile Profile
	if err := json.NewDecoder(r.Body).Decode(&profile); err != nil {
		http.Error(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(score(profile))
}

func main() {
	http.HandleFunc("/score", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
