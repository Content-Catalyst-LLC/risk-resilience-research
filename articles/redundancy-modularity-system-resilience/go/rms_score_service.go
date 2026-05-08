package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	PrimaryFailurePressure float64 `json:"primary_failure_pressure"`
	RedundancyCapacity     float64 `json:"redundancy_capacity"`
	ModularityCapacity     float64 `json:"modularity_capacity"`
	BackupDiversity        float64 `json:"backup_diversity"`
	PathwayDiversity       float64 `json:"pathway_diversity"`
	SpareCapacity          float64 `json:"spare_capacity"`
	CouplingIntensity      float64 `json:"coupling_intensity"`
	DependencyConcentration float64 `json:"dependency_concentration"`
	ContainmentStrength    float64 `json:"containment_strength"`
	RestorationCapacity    float64 `json:"restoration_capacity"`
	MonitoringCapacity     float64 `json:"monitoring_capacity"`
	GovernanceCoordination float64 `json:"governance_coordination"`
	SocialVulnerability    float64 `json:"social_vulnerability"`
	SystemCriticality      float64 `json:"system_criticality"`
	EfficiencyPressure     float64 `json:"efficiency_pressure"`
}

type Result struct {
	RedundancyIndex               float64 `json:"redundancy_index"`
	ModularityIndex               float64 `json:"modularity_index"`
	ResilienceDesignCapacity      float64 `json:"resilience_design_capacity"`
	PropagationPressure           float64 `json:"propagation_pressure"`
	ContinuityCapacity            float64 `json:"continuity_capacity"`
	EfficiencyFragilityPressure    float64 `json:"efficiency_fragility_pressure"`
	JusticeWeightedResilienceGap  float64 `json:"justice_weighted_resilience_gap"`
}

func score(p Profile) Result {
	redundancy := 0.32*p.RedundancyCapacity + 0.24*p.BackupDiversity + 0.22*p.PathwayDiversity + 0.22*p.SpareCapacity

	modularity := 0.42*p.ModularityCapacity +
		0.28*p.ContainmentStrength +
		0.18*(1-p.CouplingIntensity) +
		0.12*(1-p.DependencyConcentration)

	design := 0.30*redundancy + 0.30*modularity + 0.16*p.RestorationCapacity + 0.14*p.MonitoringCapacity + 0.10*p.GovernanceCoordination

	propagation := p.PrimaryFailurePressure *
		(1 + p.CouplingIntensity) *
		(1 + p.DependencyConcentration) *
		(1 + 0.25*p.SystemCriticality) *
		(1 - 0.45*modularity)

	continuity := 0.28*redundancy + 0.22*p.RestorationCapacity + 0.20*p.GovernanceCoordination + 0.16*p.MonitoringCapacity + 0.14*p.ContainmentStrength

	effFragility := 0.34*p.EfficiencyPressure +
		0.22*(1-p.RedundancyCapacity) +
		0.22*(1-p.ModularityCapacity) +
		0.22*p.DependencyConcentration

	gap := math.Max(0,
		(0.34*propagation+
			0.28*effFragility+
			0.22*p.SocialVulnerability+
			0.16*p.SystemCriticality)*
			(1+0.30*p.SocialVulnerability)-
			continuity,
	)

	return Result{
		RedundancyIndex:              redundancy,
		ModularityIndex:              modularity,
		ResilienceDesignCapacity:     design,
		PropagationPressure:          propagation,
		ContinuityCapacity:           continuity,
		EfficiencyFragilityPressure:   effFragility,
		JusticeWeightedResilienceGap: gap,
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
