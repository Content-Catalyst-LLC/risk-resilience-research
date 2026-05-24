# Method Notes

This scaffold models desalination resilience through simplified service-continuity calculations.

Available daily supply under normal conditions:

\[
S = D + A + E - L
\]

where:

- \(D\) is desalination output.
- \(A\) is alternative supply.
- \(E\) is emergency transfer capacity.
- \(L\) represents system losses.

Available supply during an outage:

\[
S_{outage} = (1-\alpha)D + A + E - L
\]

where \( \alpha \) is the fraction of desalination output lost.

Service continuity condition:

\[
S_{outage} \geq P
\]

where \(P\) is priority demand.

Emergency storage coverage:

\[
C = \frac{R}{\max(P - S_{outage}, 0)}
\]

where \(R\) is stored reserve and \(C\) is the number of days storage can cover the deficit. If there is no deficit, storage coverage is treated as adequate for the scenario.

These formulas are simplified for demonstration. Operational water-resilience planning requires local utility data, infrastructure condition assessments, emergency operating rules, energy-system modeling, public-health priorities, environmental constraints, legal requirements, and expert review.
