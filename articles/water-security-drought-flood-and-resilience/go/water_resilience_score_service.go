package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	DroughtPressure           float64 `json:"drought_pressure"`
	FloodExposure             float64 `json:"flood_exposure"`
	WaterDemandPressure       float64 `json:"water_demand_pressure"`
	WaterAvailability         float64 `json:"water_availability"`
	InfrastructureReliability float64 `json:"infrastructure_reliability"`
	WaterQuality              float64 `json:"water_quality"`
	EcosystemBufferCondition  float64 `json:"ecosystem_buffer_condition"`
	GovernanceCapacity        float64 `json:"governance_capacity"`
	SocialProtectionCapacity  float64 `json:"social_protection_capacity"`
	LivelihoodWaterDependency float64 `json:"livelihood_water_dependency"`
	CriticalServiceDependence float64 `json:"critical_service_dependence"`
	InequalityPressure        float64 `json:"inequality_pressure"`
	RecoveryCapacity          float64 `json:"recovery_capacity"`
	MaintenanceDeficit        float64 `json:"maintenance_deficit"`
	PollutionPressure         float64 `json:"pollution_pressure"`
}

type Result struct {
	WaterStressRatio          float64 `json:"water_stress_ratio"`
	WaterSecurityCapacity     float64 `json:"water_security_capacity"`
	HydrologicalRiskPressure  float64 `json:"hydrological_risk_pressure"`
	SystemicWaterVulnerability float64 `json:"systemic_water_vulnerability"`
	JusticeWeightedWaterRisk  float64 `json:"justice_weighted_water_risk"`
	WaterResilienceGap        float64 `json:"water_resilience_gap"`
}

func score(p Profile) Result {
	stress := math.Min(2, p.WaterDemandPressure/(p.WaterAvailability+0.05))

	capacity := 0.20*p.WaterAvailability +
		0.18*p.InfrastructureReliability +
		0.16*p.WaterQuality +
		0.18*p.EcosystemBufferCondition +
		0.16*p.GovernanceCapacity +
		0.12*p.SocialProtectionCapacity

	hydrological := 0.24*p.DroughtPressure +
		0.24*p.FloodExposure +
		0.18*math.Min(1, stress) +
		0.18*p.PollutionPressure +
		0.16*p.MaintenanceDeficit

	vulnerability := 0.24*p.LivelihoodWaterDependency +
		0.20*(1-p.RecoveryCapacity) +
		0.20*p.CriticalServiceDependence +
		0.18*(1-p.GovernanceCapacity) +
		0.18*p.InequalityPressure

	justice := (hydrological + vulnerability) * (1 + 0.30*p.InequalityPressure)
	gap := math.Max(0, justice-capacity)

	return Result{
		WaterStressRatio: stress,
		WaterSecurityCapacity: capacity,
		HydrologicalRiskPressure: hydrological,
		SystemicWaterVulnerability: vulnerability,
		JusticeWeightedWaterRisk: justice,
		WaterResilienceGap: gap,
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
