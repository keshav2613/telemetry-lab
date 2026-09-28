# Telemetry Lab

> Cloud-Native Observability & Incident Analysis Lab

🚧 **Status: In Development**

Telemetry Lab is a cloud-native observability project designed to explore how engineers can investigate distributed-system failures by correlating **metrics, logs, and distributed traces**.

Rather than focusing only on dashboards, the project will simulate real reliability problems across distributed services and use observability signals to move from **alert → investigation → root cause**.

---

## Why Telemetry Lab?

In distributed applications, identifying that a system is unhealthy is only the beginning.

Useful diagnostic information is often distributed across:

- application metrics
- infrastructure metrics
- service logs
- distributed traces
- alerts
- database behavior
- external dependencies

Telemetry Lab will provide a controlled environment for reproducing failures and investigating them using modern cloud-native observability practices.

---

## Planned Architecture

```text
                         Load Generator
                               |
                               v
                          API Service
                          /         \
                         /           \
                        v             v
                Orders Service   Payment Service
                     |                 |
                     v                 v
                PostgreSQL       External API
                         \           /
                          \         /
                           v       v

                    OpenTelemetry
                         |
                         v
               OpenTelemetry Collector
                    /      |       \
                   /       |        \
                  v        v         v
             Prometheus   Loki      Tempo
              Metrics     Logs      Traces
                   \       |        /
                    \      |       /
                     v     v      v
                        Grafana
                           |
                    Dashboards
                      Alerts
                    SLIs / SLOs