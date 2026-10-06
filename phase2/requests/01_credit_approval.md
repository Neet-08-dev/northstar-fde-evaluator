# Live change: all credits require supervisor approval

Northstar has changed its delegated financial policy: `credit.always_requires_approval=true`. The exact bound/expiry conditions remain. Implement the behavior using runtime policy, so even a $10 eligible credit creates a pending request until a real grant exists. Valid exact supervisor grants may still be used.

You have 45 minutes. Add independent evals for a small unapproved credit, a larger unapproved credit and a valid grant; demonstrate that no denied write is attempted and previous dispatch behavior still works. Use the existing get_policy/request_approval/issue_credit tools. The policy version is NS-LIVE-CREDITS. Acceptance: no unapproved credit effects, honest pending language, real exact grants honored. AI coding tools are permitted.
