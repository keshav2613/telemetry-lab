
# Incident Simulation: Slow Checkout Due to Payment Latency

## Scenario

A simulated production incident where checkout requests become slow because the downstream Payment service introduces a 2-second delay.

## Architecture

Client → FastAPI API Service → FastAPI Payment Service

Both services are instrumented with OpenTelemetry.
Traces are exported through the OpenTelemetry Collector to Grafana Tempo and visualized in Grafana.

## Reproduction

Start the Payment service with:

```powershell
$env:PAYMENT_DELAY_MS="2000"
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir services\payment --reload --port 8001
```

Call:

`GET http://127.0.0.1:8000/checkout`

## Investigation

Using Grafana Tempo, inspect the distributed trace for `GET /checkout`.

Observed measurements:

| Span | With delay | Without delay |
|---|---:|---:|
| Checkout | 4.78s | 813.98ms |
| API to Payment HTTP request | 2.12s | 11.04ms |
| Payment endpoint | 2.07s | 2.48ms |

The Payment service accounted for approximately 2 seconds of the slow request.

## Root Cause

The Payment service was intentionally configured with `PAYMENT_DELAY_MS=2000`.

## Resolution

Restart the Payment service with `PAYMENT_DELAY_MS=0`.

## Verification

A subsequent distributed trace confirmed that the Payment span decreased from approximately 2.07 seconds to 2.48 milliseconds.

The overall checkout trace decreased from 4.78 seconds to approximately 814 milliseconds.

## Lessons Learned

- Distributed tracing identifies latency across service boundaries.
- Trace context propagation connects upstream and downstream spans.
- A slow downstream dependency can affect overall request latency.
- End-to-end latency can include additional overhead beyond the downstream service.
- Controlled failure injection provides repeatable troubleshooting exercises.

## Scope

This was a local, controlled incident simulation, not a production outage.
