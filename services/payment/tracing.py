
import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


def configure_tracing():
    resource = Resource.create({
        "service.name": "payment-service"
    })

    provider = TracerProvider(resource=resource)

    # Print traces in the terminal
    provider.add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )

    # Export traces to OpenTelemetry Collector
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=os.getenv(
                    "OTEL_EXPORTER_OTLP_ENDPOINT",
                    "http://127.0.0.1:4317"
                ),
                insecure=True
            )
        )
    )

    trace.set_tracer_provider(provider)
