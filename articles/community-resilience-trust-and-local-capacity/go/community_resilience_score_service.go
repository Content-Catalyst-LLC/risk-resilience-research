package main

import (
	"encoding/json"
	"log"
	"math"
	"net/http"
)

type Profile struct {
	HazardPressure              float64 `json:"hazard_pressure"`
	Exposure                    float64 `json:"exposure"`
	SocialVulnerability          float64 `json:"social_vulnerability"`
	TrustLevel                  float64 `json:"trust_level"`
	LocalOrganizationalCapacity  float64 `json:"local_organizational_capacity"`
	MutualAidStrength           float64 `json:"mutual_aid_strength"`
	CommunicationAccess         float64 `json:"communication_access"`
	LocalKnowledgeIntegration    float64 `json:"local_knowledge_integration"`
	InstitutionalSupport        float64 `json:"institutional_support"`
	ParticipationQuality        float64 `json:"participation_quality"`
	RecoveryCapacity            float64 `json:"recovery_capacity"`
	ExclusionPressure           float64 `json:"exclusion_pressure"`
	InstitutionalFollowThrough  float64 `json:"institutional_follow_through"`
	BrokenPromisePressure       float64 `json:"broken_promise_pressure"`
}

type Result struct {
	CommunityHazardPressure       float64 `json:"community_hazard_pressure"`
	LocalResilienceCapacity       float64 `json:"local_resilience_capacity"`
	TrustAdjustedResponseCapacity float64 `json:"trust_adjusted_response_capacity"`
	ParticipationLegitimacy       float64 `json:"participation_legitimacy"`
	CommunityResilienceGap        float64 `json:"community_resilience_gap"`
	UpdatedTrustProjection        float64 `json:"updated_trust_projection"`
}

func clamp(value float64, lower float64, upper float64) float64 {
	return math.Max(lower, math.Min(upper, value))
}

func score(p Profile) Result {
	hazardPressure := p.HazardPressure *
		p.Exposure *
		(1 + 0.40*p.SocialVulnerability)

	localCapacity := 0.16*p.TrustLevel +
		0.15*p.LocalOrganizationalCapacity +
		0.14*p.MutualAidStrength +
		0.13*p.CommunicationAccess +
		0.14*p.LocalKnowledgeIntegration +
		0.12*p.InstitutionalSupport +
		0.08*p.ParticipationQuality +
		0.08*p.RecoveryCapacity

	responseCapacity := (
		0.28*p.LocalOrganizationalCapacity +
			0.25*p.MutualAidStrength +
			0.24*p.CommunicationAccess +
			0.23*p.LocalKnowledgeIntegration) *
		(1 + 0.35*p.TrustLevel)
	responseCapacity = clamp(responseCapacity, 0, 1.5)

	participation := p.ParticipationQuality *
		(1 + 0.25*p.InstitutionalSupport) *
		(1 - 0.35*p.ExclusionPressure)
	participation = clamp(participation, 0, 1.5)

	gap := math.Max(0, hazardPressure-responseCapacity-participation)

	trustProjection := p.TrustLevel +
		0.30*p.InstitutionalFollowThrough -
		0.35*p.BrokenPromisePressure -
		0.20*p.ExclusionPressure
	trustProjection = clamp(trustProjection, 0, 1)

	return Result{
		CommunityHazardPressure: hazardPressure,
		LocalResilienceCapacity: localCapacity,
		TrustAdjustedResponseCapacity: responseCapacity,
		ParticipationLegitimacy: participation,
		CommunityResilienceGap: gap,
		UpdatedTrustProjection: trustProjection,
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
