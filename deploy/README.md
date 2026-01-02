# Deployment Guide

This directory contains the Helm charts for deploying TrendLab to Kubernetes.

## Prerequisites

- `helm` installed
- `kubectl` configured with cluster access

## Environments

| Environment | Values File       | Namespace | Description |
|-------------|-------------------|-----------|-------------|
| **Dev**     | `values-dev.yaml` | `dev`     | Ephemeral storage, single replica |
| **Hml**     | `values-hml.yaml` | `hml`     | Persistent storage, HPA enabled (2-4 replicas) |
| **Prd**     | `values-prd.yaml` | `prd`     | Large storage, HPA enabled (3-10 replicas) |

## Manual Deployment

To manually install or upgrade the chart:

```bash
helm upgrade --install trendlab ./helm/trendlab \
  -f ./helm/values-dev.yaml \
  --namespace dev \
  --create-namespace
```

## Scaling (HPA)

Horizontal Pod Autoscaling is enabled for HML and PRD. It scales based on CPU utilization (target 60%).

To verify:
```bash
kubectl get hpa -n hml
```

