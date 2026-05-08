package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	InitiatingShockSeverity float64 `json:"initiating_shock_severity"`
	DependencyDensity      float64 `json:"dependency_density"`
	HiddenCoupling         float64 `json:"hidden_coupling"`
	CriticalNodeExposure   float64 `json:"critical_node_exposure"`
	BackupCapacity        float64 `json:"backup_capacity"`
	ModularityCapacity    float64 `json:"modularity_capacity"`
	CrossSectorCoordination float64 `json:"cross_sector_coordination"`
	RestorationSpeed      float64 `json:"restoration_speed"`
	RedundancyCapacity    float64 `json:"redundancy_capacity"`
	SocialVulnerability   float64 `json:"social_vulnerability"`
	GovernanceReadiness   float64 `json:"governance_readiness"`
	SystemCriticality     float64 `json:"system_criticality"`
	CascadeExposure       float64 `json:"cascade_exposure"`
	MonitoringCapacity    float64 `json:"monitoring_capacity"`
	PublicTrust           float64 `json:"public_trust"`
}

type Result struct {
	DependencyPressure       float64 `json:"dependency_pressure"`
	ContainmentCapacity      float64 `json:"containment_capacity"`
	GovernanceResponse       float64 `json:"governance_response_capacity"`
	PropagationLikelihood    float64 `json:"propagation_likelihood"`
	CascadeAmplification     float64 `json:"cascade_amplification"`
	ContinuityGap            float64 `json:"continuity_gap"`
	JusticeWeightedRisk      float64 `json:"justice_weighted_cascade_risk"`
}

func score(p Profile) Result {
	dependencyPressure := 0.34*p.DependencyDensity + 0.30*p.HiddenCoupling + 0.22*p.CriticalNodeExposure + 0.14*p.SystemCriticality

	containment := 0.22*p.BackupCapacity + 0.24*p.ModularityCapacity + 0.20*p.RedundancyCapacity + 0.18*p.MonitoringCapacity + 0.16*p.CrossSectorCoordination

	governance := 0.30*p.CrossSectorCoordination + 0.24*p.RestorationSpeed + 0.20*p.GovernanceReadiness + 0.14*p.MonitoringCapacity + 0.12*p.PublicTrust

	propagation := p.InitiatingShockSeverity *
		(1 + dependencyPressure) *
		(1 + 0.35*p.CascadeExposure) *
		(1 - 0.45*containment)

	cascade := propagation *
		(1 + p.SystemCriticality) *
		(1 + p.SocialVulnerability) *
		(1 - 0.35*governance)

	continuity := 0.26*p.BackupCapacity + 0.22*p.RedundancyCapacity + 0.20*p.RestorationSpeed + 0.18*p.CrossSectorCoordination + 0.14*p.PublicTrust
	gap := math.Max(0, cascade-continuity)

	risk := (0.34*propagation + 0.30*cascade + 0.20*gap + 0.16*p.SocialVulnerability) * (1 + 0.30*p.SocialVulnerability)

	return Result{
		DependencyPressure:    dependencyPressure,
		ContainmentCapacity:   containment,
		GovernanceResponse:    governance,
		PropagationLikelihood: propagation,
		CascadeAmplification:  cascade,
		ContinuityGap:         gap,
		JusticeWeightedRisk:   risk,
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
