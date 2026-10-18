import os
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from tracing import configure_tracing
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Telemetry Lab API",
    version="0.1.0"
)

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL",
    "http://127.0.0.1:8001"
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "telemetry-api"
    }


@app.get("/checkout")
async def checkout():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{PAYMENT_SERVICE_URL}/payment"
            )

            response.raise_for_status()

        return {
            "checkout_status": "completed",
            "payment": response.json()
        }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Payment service timed out"
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Payment service returned an error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Payment service unavailable"
        )
        
configure_tracing()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()