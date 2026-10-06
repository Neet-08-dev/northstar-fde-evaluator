# Live change: the provider sometimes loses committed responses

The downstream provider now returns TIMEOUT after a ticket or credit has already committed. Improve the action boundary so retries use exactly the original key/arguments and produce one confirmed effect. Persistently unavailable operations need a bounded retry and contextual handoff.

You have 45 minutes. Use the public `TIMEOUT_AFTER_COMMIT` and `TEMPORARY_UNAVAILABLE` fixtures. Add ticket and credit lost-response evals plus a persistent outage. Demonstrate exact-once effects within one test session, honest failure language and a normal regression. Discuss durable idempotency across process restarts as a production boundary. AI coding tools are permitted.
