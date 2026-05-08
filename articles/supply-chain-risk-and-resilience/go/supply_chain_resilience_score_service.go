package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	Criticality                  float64 `json:"criticality"`
	SupplierConcentration        float64 `json:"supplier_concentration"`
	DependencyIntensity          float64 `json:"dependency_intensity"`
	LogisticsExposure            float64 `json:"logistics_exposure"`
	CyberDigitalRisk             float64 `json:"cyber_digital_risk"`
	WorkforceVulnerability       float64 `json:"workforce_vulnerability"`
	ClimateHazardExposure        float64 `json:"climate_hazard_exposure"`
	InventoryBuffer             float64 `json:"inventory_buffer"`
	Substitutability             float64 `json:"substitutability"`
	SupplierRedundancy           float64 `json:"supplier_redundancy"`
	ModularProductionCapacity    float64 `json:"modular_production_capacity"`
	GovernanceCapacity           float64 `json:"governance_capacity"`
	LogisticsFlexibility         float64 `json:"logistics_flexibility"`
	RecoveryTimePressure         float64 `json:"recovery_time_pressure"`
	VulnerablePopulationExposure float64 `json:"vulnerable_population_exposure"`
	EssentialServiceRelevance    float64 `json:"essential_service_relevance"`
}

type Result struct {
	DisruptionPressure              float64 `json:"disruption_pressure"`
	ResilienceBufferCapacity        float64 `json:"resilience_buffer_capacity"`
	ShortageRisk                    float64 `json:"shortage_risk"`
	ConcentrationAdjustedDependency float64 `json:"concentration_adjusted_dependency"`
	ServiceContinuityGap            float64 `json:"service_continuity_gap"`
	PublicPriorityScore             float64 `json:"public_priority_score"`
}

func score(p Profile) Result {
	disruptionPressure := p.Criticality *
		(0.22*p.SupplierConcentration +
			0.20*p.DependencyIntensity +
			0.18*p.LogisticsExposure +
			0.16*p.CyberDigitalRisk +
			0.14*p.WorkforceVulnerability +
			0.10*p.ClimateHazardExposure)

	bufferCapacity := 0.22*p.InventoryBuffer +
		0.20*p.Substitutability +
		0.20*p.SupplierRedundancy +
		0.16*p.ModularProductionCapacity +
		0.12*p.GovernanceCapacity +
		0.10*p.LogisticsFlexibility

	shortageRisk := disruptionPressure *
		(1 + 0.40*p.RecoveryTimePressure) *
		(1 - 0.45*bufferCapacity)

	dependency := p.SupplierConcentration *
		p.DependencyIntensity *
		(1 - p.Substitutability)

	serviceGap := math.Max(0, p.Criticality+shortageRisk-bufferCapacity)

	publicPriority := serviceGap +
		0.30*p.Criticality +
		0.25*p.VulnerablePopulationExposure +
		0.25*p.EssentialServiceRelevance

	return Result{
		DisruptionPressure: disruptionPressure,
		ResilienceBufferCapacity: bufferCapacity,
		ShortageRisk: shortageRisk,
		ConcentrationAdjustedDependency: dependency,
		ServiceContinuityGap: serviceGap,
		PublicPriorityScore: publicPriority,
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
