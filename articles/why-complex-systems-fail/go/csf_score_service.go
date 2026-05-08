package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	DependencyDensity    float64 `json:"dependency_density"`
	HiddenCoupling       float64 `json:"hidden_coupling"`
	FeedbackDelay        float64 `json:"feedback_delay"`
	SignalVisibility     float64 `json:"signal_visibility"`
	BufferCapacity       float64 `json:"buffer_capacity"`
	RedundancyCapacity   float64 `json:"redundancy_capacity"`
	ModularityCapacity   float64 `json:"modularity_capacity"`
	AdaptationDebt       float64 `json:"adaptation_debt"`
	OptimizationPressure float64 `json:"optimization_pressure"`
	MaintenanceDeficit   float64 `json:"maintenance_deficit"`
	MonitoringCapacity   float64 `json:"monitoring_capacity"`
	GovernanceCoordination float64 `json:"governance_coordination"`
	SocialVulnerability  float64 `json:"social_vulnerability"`
	SystemCriticality    float64 `json:"system_criticality"`
	ExternalStress       float64 `json:"external_stress"`
}

type Result struct {
	CouplingPressure      float64 `json:"coupling_pressure"`
	DeteriorationPressure float64 `json:"deterioration_pressure"`
	SlackDeficit         float64 `json:"slack_deficit"`
	ResilienceCapacity   float64 `json:"resilience_capacity"`
	CascadePotential     float64 `json:"cascade_potential"`
	FailureRisk          float64 `json:"failure_risk"`
	FailureGap           float64 `json:"failure_gap"`
}

func score(p Profile) Result {
	coupling := 0.48*p.DependencyDensity + 0.36*p.HiddenCoupling + 0.16*p.SystemCriticality

	deterioration := 0.30*p.FeedbackDelay +
		0.28*(1-p.SignalVisibility) +
		0.22*p.MaintenanceDeficit +
		0.20*p.AdaptationDebt

	slackDeficit := 0.34*(1-p.BufferCapacity) +
		0.30*(1-p.RedundancyCapacity) +
		0.20*(1-p.ModularityCapacity) +
		0.16*p.OptimizationPressure

	resilience := 0.20*p.BufferCapacity +
		0.20*p.RedundancyCapacity +
		0.18*p.ModularityCapacity +
		0.18*p.MonitoringCapacity +
		0.14*p.GovernanceCoordination +
		0.10*p.SignalVisibility

	cascade := coupling *
		(1 + p.ExternalStress) *
		(1 + 0.5*p.SystemCriticality) *
		(1 - 0.35*p.ModularityCapacity)

	structuralFragility := 0.30*coupling +
		0.28*deterioration +
		0.24*slackDeficit +
		0.18*p.SocialVulnerability

	failureRisk := structuralFragility *
		(1 + p.ExternalStress) *
		(1 + 0.35*p.SystemCriticality) *
		(1 - 0.45*resilience)

	gap := math.Max(0, failureRisk-resilience)

	return Result{
		CouplingPressure:      coupling,
		DeteriorationPressure: deterioration,
		SlackDeficit:         slackDeficit,
		ResilienceCapacity:   resilience,
		CascadePotential:     cascade,
		FailureRisk:          failureRisk,
		FailureGap:           gap,
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
