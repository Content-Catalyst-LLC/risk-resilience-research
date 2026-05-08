package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	EcosystemCondition      float64 `json:"ecosystem_condition"`
	BiodiversityBenefit     float64 `json:"biodiversity_benefit"`
	EcologicalConnectivity  float64 `json:"ecological_connectivity"`
	InterventionQuality     float64 `json:"intervention_quality"`
	GovernanceCapacity      float64 `json:"governance_capacity"`
	MaintenanceCapacity     float64 `json:"maintenance_capacity"`
	HazardPressure          float64 `json:"hazard_pressure"`
	Exposure                float64 `json:"exposure"`
	SocialVulnerability     float64 `json:"social_vulnerability"`
	SocialLegitimacy        float64 `json:"social_legitimacy"`
	LivelihoodBenefit       float64 `json:"livelihood_benefit"`
	DisplacementPressure    float64 `json:"displacement_pressure"`
}

type Result struct {
	NBSIntegrity                 float64 `json:"nbs_integrity"`
	HazardVulnerabilityPressure  float64 `json:"hazard_vulnerability_pressure"`
	BufferEffectiveness         float64 `json:"buffer_effectiveness"`
	NatureAdjustedRisk          float64 `json:"nature_adjusted_risk"`
	CredibilityRisk             float64 `json:"credibility_risk"`
	JusticeWeightedNBSRisk      float64 `json:"justice_weighted_nbs_risk"`
	NBSResilienceGap            float64 `json:"nbs_resilience_gap"`
}

func score(p Profile) Result {
	integrity := 0.20*p.EcosystemCondition +
		0.18*p.BiodiversityBenefit +
		0.16*p.EcologicalConnectivity +
		0.16*p.InterventionQuality +
		0.15*p.GovernanceCapacity +
		0.15*p.MaintenanceCapacity

	pressure := p.HazardPressure * p.Exposure * (1 + 0.35*p.SocialVulnerability)

	buffer := integrity *
		(1 + 0.22*p.SocialLegitimacy) *
		(1 + 0.18*p.LivelihoodBenefit)
	buffer = math.Min(1.5, buffer)

	natureAdjusted := pressure *
		(1 - 0.45*math.Min(1, buffer)) *
		(1 - 0.25*p.GovernanceCapacity)

	credibility := 0.22*(1-p.EcosystemCondition) +
		0.20*(1-p.BiodiversityBenefit) +
		0.18*(1-p.SocialLegitimacy) +
		0.18*(1-p.MaintenanceCapacity) +
		0.22*p.DisplacementPressure

	justice := (natureAdjusted + credibility) * (1 + 0.30*p.SocialVulnerability)
	gap := math.Max(0, justice-buffer)

	return Result{
		NBSIntegrity: integrity,
		HazardVulnerabilityPressure: pressure,
		BufferEffectiveness: buffer,
		NatureAdjustedRisk: natureAdjusted,
		CredibilityRisk: credibility,
		JusticeWeightedNBSRisk: justice,
		NBSResilienceGap: gap,
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
