# Live change: regional scheduling blackouts

Structured policy now includes `scheduling.blackout_windows`, a list of objects with region, start and end (ISO-8601 UTC). A one-hour visit must not overlap its region's blackout. The current slot API still reports capacity without this new business rule, so your orchestration must apply it.

Example: north blackout from 2030-04-08T09:00:00Z to 2030-04-08T12:00:00Z excludes the north 10:00 visit; 14:00 remains valid. End is exclusive. A blackout in south must not block north service. If no eligible slot remains, hand off without booking.

You have 45 minutes. Add overlap, all-slots-blocked and different-region evals plus an unaffected baseline regression. Show explicit timestamp/region handling and actual booking state. AI coding tools are permitted.
