# Live change: enterprise emergency acknowledgment

Enterprise S1 acknowledgment target changes from 10 to 5 minutes via `sla.enterprise_s1_ack_minutes=5`; standard S1 stays 15. Implement runtime policy/tier-based urgency and state the applicable target in the acknowledgment. Preserve immediate safety handoff and direction to move away/contact site emergency personnel. Routine S2 dispatch must keep working.

You have 45 minutes. Add an enterprise emergency, standard emergency and routine regression. Show your acknowledgment-time measurement and distinguish a target from a promised repair time. In this local harness the `/process` reply is the acknowledgment; it must complete within the five-minute target. Production delivery/retries can be described in DESIGN.md rather than implemented. The private checks cover correct tier/target language and safety state; the interviewer also reviews timestamp/budget logic. AI coding tools are permitted.
