package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	ConcurrentHazardIntensity float64 `json:"concurrent_hazard_intensity"`
	SequentialHazardPressure float64 `json:"sequential_hazard_pressure"`
	Exposure                 float64 `json:"exposure"`
	SocialVulnerability       float64 `json:"social_vulnerability"`
	InfrastructureFragility   float64 `json:"infrastructure_fragility"`
	HealthSystemStrain       float64 `json:"health_system_strain"`
	FoodWaterEnergyStress     float64 `json:"food_water_energy_stress"`
	GovernanceReadiness       float64 `json:"governance_readiness"`
	CrossSectorDependency     float64 `json:"cross_sector_dependency"`
	RecoveryDeficit          float64 `json:"recovery_deficit"`
	InequalityPressure        float64 `json:"inequality_pressure"`
	EcologicalBufferCondition float64 `json:"ecological_buffer_condition"`
	SocialProtectionCapacity  float64 `json:"social_protection_capacity"`
	CommunicationReliability  float64 `json:"communication_reliability"`
}

type Result struct {
	CompoundEventSeverity    float64 `json:"compound_event_severity"`
	SocialSensitivityIndex   float64 `json:"social_sensitivity_index"`
	SystemFragilityIndex     float64 `json:"system_fragility_index"`
	CascadePotential         float64 `json:"cascade_potential"`
	JusticeWeightedRisk      float64 `json:"justice_weighted_social_risk"`
	ContinuityCapacity       float64 `json:"continuity_capacity"`
	CompoundResilienceGap    float64 `json:"compound_resilience_gap"`
}

func score(p Profile) Result {
	compound := 0.42*p.ConcurrentHazardIntensity + 0.34*p.SequentialHazardPressure + 0.24*p.Exposure

	social := 0.30*p.SocialVulnerability + 0.22*p.HealthSystemStrain + 0.20*p.FoodWaterEnergyStress + 0.16*p.RecoveryDeficit + 0.12*p.InequalityPressure

	fragility := 0.30*p.InfrastructureFragility + 0.28*p.CrossSectorDependency + 0.18*p.FoodWaterEnergyStress + 0.14*p.RecoveryDeficit + 0.10*(1-p.CommunicationReliability)

	resilience := 0.24*p.GovernanceReadiness + 0.22*p.EcologicalBufferCondition + 0.22*p.SocialProtectionCapacity + 0.18*p.CommunicationReliability + 0.14*(1-p.RecoveryDeficit)

	cascade := compound * (1 + 0.45*fragility) * (1 + 0.35*p.CrossSectorDependency) * (1 - 0.30*resilience)

	justice := (0.38*cascade + 0.30*social + 0.18*p.RecoveryDeficit + 0.14*p.InequalityPressure) * (1 + 0.35*p.InequalityPressure)

	continuity := 0.28*p.GovernanceReadiness + 0.22*p.SocialProtectionCapacity + 0.20*p.CommunicationReliability + 0.18*p.EcologicalBufferCondition + 0.12*(1-p.InfrastructureFragility)

	gap := math.Max(0, justice-continuity)

	return Result{
		CompoundEventSeverity: compound,
		SocialSensitivityIndex: social,
		SystemFragilityIndex: fragility,
		CascadePotential: cascade,
		JusticeWeightedRisk: justice,
		ContinuityCapacity: continuity,
		CompoundResilienceGap: gap,
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
