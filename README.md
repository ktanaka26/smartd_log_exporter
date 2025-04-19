# smartd-exporter for Prometheus

This project parses `smartd` logs from syslog and exports them as Prometheus metrics via the `textfile_collector` interface of `node_exporter`.

## Features

- Extracts `Currently unreadable (pending) sectors` messages from syslog
- Outputs metrics in Prometheus textfile format
- Dockerized with multi-arch support (`amd64`, `arm64`)
- Works with Prometheus + Alertmanager for alerting
- Logs all executions for auditability

## Usage

### With Docker Compose

1. Build and start the exporter:

```bash
docker-compose up -d --build
```

2. Ensure the following paths are correctly mounted:
   - `/var/log` from host for syslog access
   - `/var/lib/node_exporter/textfile_collector` for `.prom` file output

### Environment Variables

- `SYSLOG_PATH`: path to syslog file (default: `/var/log/syslog`)
- `OUTPUT_PATH`: path to `.prom` file (default: `/var/lib/node_exporter/textfile_collector/smartd.prom`)

## Prometheus Setup

### Rule File Example

Put the following in your Prometheus rule directory:

```yaml
groups:
  - name: smartd_alerts
    rules:
      - alert: SmartdPendingSectorsDetected
        expr: smartd_unreadable_sectors > 0
        for: 5m
        labels:
          severity: warn
        annotations:
          summary: "Unreadable sectors detected on {{ $labels.device }}"
          description: "Device {{ $labels.device }} has {{ $value }} unreadable sectors for more than 5 minutes."
```

### Alertmanager Integration

Alerts can be routed to Discord, Slack, or Email using Alertmanager.

## Building Docker Image

```bash
docker build -t smartd-exporter .
```

Multi-architecture builds using GitHub Actions are supported (see `.github/workflows/docker-build.yml`).
