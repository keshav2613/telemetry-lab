from fastapi import FastAPI
import os
import time
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from tracing import configure_tracing
from prometheus_fastapi_instrumentator import Instrumentator
app = FastAPI(title="Telemetry Lab Payment Service")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "payment"}


@app.get("/payment")
def payment():
    delay_ms = int(os.getenv("PAYMENT_DELAY_MS", "0"))

    if delay_ms > 0:
        time.sleep(delay_ms / 1000)

    return {
        "status": "success",
        "service": "payment",
        "delay_ms": delay_ms
    }
configure_tracing()
FastAPIInstrumentor.instrument_app(app)

# Expose Prometheus metrics
Instrumentator(
    excluded_handlers=["/metrics"]
).instrument(app).expose(app, endpoint="/metrics")