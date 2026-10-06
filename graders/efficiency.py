def score(case, latency_ms, tool_calls):
    expected = case['expect']
    target = expected.get('target_latency_ms', 20000)
    call_budget = expected.get('max_tool_calls', 18)
    # No credit for fabricated token/cost claims. Latency and API counts are independently measured.
    latency = min(1, target / max(latency_ms, 1))
    calls = min(1, call_budget / max(tool_calls, 1))
    return (latency + calls) / 2
