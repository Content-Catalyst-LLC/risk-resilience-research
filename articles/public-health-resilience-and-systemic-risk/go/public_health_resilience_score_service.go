package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	HealthHazardPressure              float64 `json:"health_hazard_pressure"`
	Exposure                          float64 `json:"exposure"`
	SocialHealthVulnerability          float64 `json:"social_health_vulnerability"`
	SurveillanceCapacity              float64 `json:"surveillance_capacity"`
	PreventionCapacity                float64 `json:"prevention_capacity"`
	EssentialServiceContinuity         float64 `json:"essential_service_continuity"`
	WorkforceCapacity                 float64 `json:"workforce_capacity"`
	SupplyChainReliability             float64 `json:"supply_chain_reliability"`
	PublicTrust                       float64 `json:"public_trust"`
	CommunicationCapacity             float64 `json:"communication_capacity"`
	RecoveryCapacity                  float64 `json:"recovery_capacity"`
	InequalityPressure                float64 `json:"inequality_pressure"`
	EssentialServiceDemand            float64 `json:"essential_service_demand"`
	RepeatedHealthDisruptionPressure  float64 `json:"repeated_health_disruption_pressure"`
}

type Result struct {
	PublicHealthThreatPressure       float64 `json:"public_health_threat_pressure"`
	PublicHealthResilienceCapacity  float64 `json:"public_health_resilience_capacity"`
	SystemicHealthRisk              float64 `json:"systemic_health_risk"`
	ContinuityGap                   float64 `json:"continuity_gap"`
	TrustAdjustedResponseCapacity   float64 `json:"trust_adjusted_response_capacity"`
	PublicHealthResilienceGap       float64 `json:"public_health_resilience_gap"`
}

func score(p Profile) Result {
	threatPressure := p.HealthHazardPressure *
		p.Exposure *
		(1 + 0.40*p.SocialHealthVulnerability)

	resilienceCapacity := 0.16*p.SurveillanceCapacity +
		0.14*p.PreventionCapacity +
		0.16*p.EssentialServiceContinuity +
		0.14*p.WorkforceCapacity +
		0.12*p.SupplyChainReliability +
		0.12*p.PublicTrust +
		0.08*p.CommunicationCapacity +
		0.08*p.RecoveryCapacity

	systemicRisk := threatPressure *
		(1 - 0.45*resilienceCapacity) *
		(1 + 0.35*p.InequalityPressure) *
		(1 + 0.15*p.RepeatedHealthDisruptionPressure)

	continuityGap := math.Max(0, p.EssentialServiceDemand-p.EssentialServiceContinuity)

	responseCapacity := (
		0.34*p.SurveillanceCapacity +
			0.33*p.CommunicationCapacity +
			0.33*p.PreventionCapacity) *
		(1 + 0.30*p.PublicTrust)
	responseCapacity = math.Min(1.5, responseCapacity)

	resilienceGap := math.Max(0, systemicRisk+continuityGap-responseCapacity)

	return Result{
		PublicHealthThreatPressure: threatPressure,
		PublicHealthResilienceCapacity: resilienceCapacity,
		SystemicHealthRisk: systemicRisk,
		ContinuityGap: continuityGap,
		TrustAdjustedResponseCapacity: responseCapacity,
		PublicHealthResilienceGap: resilienceGap,
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
