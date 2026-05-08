package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	EcosystemCondition      float64 `json:"ecosystem_condition"`
	EcologicalConnectivity float64 `json:"ecological_connectivity"`
	FunctionalBiodiversity float64 `json:"functional_biodiversity"`
	MaintenanceCapacity    float64 `json:"maintenance_capacity"`
	RestorationInvestment  float64 `json:"restoration_investment"`
	HazardPressure         float64 `json:"hazard_pressure"`
	Exposure               float64 `json:"exposure"`
	SocialVulnerability    float64 `json:"social_vulnerability"`
	GovernanceCapacity     float64 `json:"governance_capacity"`
	DegradationPressure    float64 `json:"degradation_pressure"`
}

type Result struct {
	NaturalBufferCapacity      float64 `json:"natural_buffer_capacity"`
	HazardExposurePressure     float64 `json:"hazard_exposure_pressure"`
	BufferAdjustedRisk        float64 `json:"buffer_adjusted_risk"`
	EcologicalFragility        float64 `json:"ecological_fragility"`
	JusticeWeightedRisk        float64 `json:"justice_weighted_ecosystem_risk"`
	EcosystemResilienceGap     float64 `json:"ecosystem_resilience_gap"`
}

func score(p Profile) Result {
	buffer := 0.24*p.EcosystemCondition +
		0.20*p.EcologicalConnectivity +
		0.20*p.FunctionalBiodiversity +
		0.18*p.MaintenanceCapacity +
		0.18*p.RestorationInvestment

	pressure := p.HazardPressure * p.Exposure * (1 + 0.35*p.SocialVulnerability)

	adjusted := pressure *
		(1 - 0.45*buffer) *
		(1 - 0.25*p.GovernanceCapacity)

	fragility := 0.28*(1-p.EcosystemCondition) +
		0.24*(1-p.EcologicalConnectivity) +
		0.22*(1-p.FunctionalBiodiversity) +
		0.14*(1-p.MaintenanceCapacity) +
		0.12*p.DegradationPressure

	justice := (adjusted + fragility) * (1 + 0.30*p.SocialVulnerability)
	gap := math.Max(0, justice-buffer)

	return Result{
		NaturalBufferCapacity: buffer,
		HazardExposurePressure: pressure,
		BufferAdjustedRisk: adjusted,
		EcologicalFragility: fragility,
		JusticeWeightedRisk: justice,
		EcosystemResilienceGap: gap,
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
