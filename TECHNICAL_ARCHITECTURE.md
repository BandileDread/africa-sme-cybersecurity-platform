# Technical Architecture Documentation
## Cybersecurity SaaS Platform for African SMEs

**Document Version:** 1.0  
**Last Updated:** 2026-03-24  
**Status:** Draft - Brainstorming Phase

---

## 1. Executive Summary

This document outlines the technical architecture for a multi-tenant SaaS cybersecurity platform targeting Small and Medium Enterprises (SMEs) in South Africa, with expansion capability across Africa. The platform provides vulnerability management and threat detection services with optional automated response capabilities.

### Core Value Propositions
- **Accessible Security:** Enterprise-grade capability packaged for SME budgets
- **Compliance Ready:** POPIA, ISO 27001, PCI DSS aligned
- **African Optimized:** Connectivity-resilient, bandwidth-conscious, locally hosted
- **Progressive Capability:** Start simple, scale to full XDR

---

## 2. System Overview

### 2.1 Architecture Philosophy
- **Cloud-Native:** Kubernetes-based microservices architecture
- **Multi-Tenant:** Cost-efficient SaaS delivery with proper data isolation
- **API-First:** All functionality exposed via RESTful APIs
- **Event-Driven:** Asynchronous processing for scalability
- **Open Source Core:** Build on proven open-source tools, own the integration layer

### 2.2 Service Tiers
```
┌─────────────────────────────────────────────────────────────┐
│                    PLATFORM                                  │
│    Tier: Fully customizable, API access, white-label        │
│    Target: Enterprise, MSSPs                                 │
├─────────────────────────────────────────────────────────────┤
│                   RESPOND + DETECT                          │
│    Tier: Automated playbooks, active response             │
│    Target: Security-conscious mid-sized businesses          │
├─────────────────────────────────────────────────────────────┤
│               DETECT + VULN MANAGE                         │
│    Tier: Combined threat detection + vulnerability scanning  │
│    Target: General SMEs, regulated industries               │
├─────────────────────────────────────────────────────────────┤
│                    CORE DETECT                             │
│    Tier: Basic threat detection, alerting                    │
│    Target: Entry-level, budget-conscious SMEs               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │  Web Dashboard  │  │  Mobile App     │  │  API Clients    │          │
│  │  (React SPA)    │  │  (Future)       │  │                 │          │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘          │
└───────────┼──────────────────────│─────────────────────│──────────────────┘
            │                      │                     │
            │                      │                     │ HTTP(S)/WSS
            ▼                      ▼                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           EDGE LAYER (CDN)                               │
│  CloudFront / Cloudflare / Local CDN for African regions                 │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          CONTROL PLANE (K8s)                             │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │                        Ingress Controller                             ││
│  │              (NGINX GW / Traefik / Kong)                           ││
│  └────────────────────────────────┬───────────────────────────────────┘│
│                                   │                                    │
│  ┌──────────────┐  ┌──────────────┴──────────────┐  ┌──────────────┐  │
│  │   Auth       │  │       API Gateway           │  │   Admin      │  │
│  │  Keycloak    │  │   (Rate Limit, Authz)       │  │   Service    │  │
│  └──────────────┘  └──────────────┬──────────────┘  └──────────────┘  │
│                                   │                                    │
│  ┌────────────────────────────────┼────────────────────────────────┐  │
│  │                    Core Business Services                        │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ Tenant   │ │ Detection│ │ Vuln     │ │ Response │          │  │
│  │  │ Service  │ │ Engine   │ │ Scanner  │ │ Service  │          │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │  │
│  │                                                                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ Asset    │ │ Rules    │ │ Report   │ │ Billing  │          │  │
│  │  │ Mgmt     │ │ Engine   │ │ Gen      │ │ Service  │          │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Integration Services                          │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ Webhook  │ │ Ticketing│ │ SIEM     │ │ Intel    │          │  │
│  │  │ Service  │ │ Connect  │ │ Export   │ │ Feed     │          │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         MESSAGE BUS LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │   NATS / Kafka     │  │   Event Router   │  │   Dead Letter    │      │
│  │   (Pub/Sub)        │  │                  │  │   Queue          │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │   Time-Series DB │  │   Document Store │  │   Object Store   │        │
│  │   (TimescaleDB)  │  │   (PostgreSQL   │  │   (MinIO/S3)     │        │
│  │                  │  │    JSONB)        │  │                  │        │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │   Cache          │  │   Search         │  │   Archive        │        │
│  │   (Redis)        │  │   (OpenSearch)   │  │   (Cold Storage) │        │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘        │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              AGENT LAYER                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │  OSQuery Agent   │  │  Velociraptor   │  │ Custom Agent     │        │
│  │  (Telemetry)     │  │  (IR/Forensics) │  │ (Future)         │        │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘        │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Deep Dive

### 4.1 Agent Layer

The agent layer deploys on customer endpoints to collect telemetry and execute response actions.

**Phase 1: Established Open Source Agents**
- **OSQuery**: SQL-based endpoint telemetry
  - Process listings, network connections, user sessions
  - File integrity monitoring (FIM)
  - Scheduled queries every 5 minutes
  
- **Velociraptor**: Deep forensics and incident response
  - Artifact-based collection
  - Memory analysis capabilities
  - On-demand or scheduled deep inspection

- **Wazuh Agent**: SIEM-forwarding agent
  - Log collection and forwarding
  - Rootkit detection
  - Policy monitoring

**Phase 2: Hybrid Agent (Your IP)**
Custom lightweight agent that:
- Wraps OSQuery/Velociraptor
- Normalizes output to your schema
- Handles offline buffering
- Compression and encryption

**Phase 3: Native Agent (Full IP)**
Replace open-source components with in-house implementations while maintaining compatibility.

### 4.2 Data Pipeline Architecture

```
Raw Events → Normalizer → Enricher → Detector → Responder → Storage
     ↓            ↓           ↓          ↓          ↓          ↓
  Agent      Schema      Threat     Rule       Playbooks  Time-series
  Output     Transform   Intel                 Actions    Object Store
```

**Event Flow:**
1. **Ingestion**: Agents → NATS/Kafka topics (per-tenant)
2. **Parsing**: Vector/Fluent Bit consumers normalize payload
3. **Enrichment**: Add context (geolocation, threat intel, asset tags)
4. **Detection**: Stream processing (Apache Flink or custom Go services)
   - Sigma rule evaluation
   - Statistical anomaly detection
   - ML inference (future tier)
5. **Routing**: Critical alerts → Immediate processing; Normal events → Batch
6. **Persistence**: TimescaleDB for hot data, S3/MinIO for cold storage

### 4.3 Detection Engine

**Rule Types:**
| Type | Description | Example |
|------|-------------|---------|
| **Signature** | Pattern matching (Sigma rules) | Known malware hashes, suspicious PowerShell |
| **Behavioral** | MITRE ATT&CK technique detection | Lateral movement, credential dumping |
| **Anomaly** | Statistical deviations from baseline | Unusual login times, data transfer spikes |
| **Threat Intel** | IOC matching | Malicious IPs/Domains from MISP/OpenCTI |

**Rule Execution Model:**
```
Event Stream → Filter by Asset/OS → Match Rules → Output Alert
                    ↓                      ↓
               Pre-filtering          Severity Assignment
               (reduce compute)       (Critical/High/Med/Low)
```

---

## 5. Security Architecture

### 5.1 Data Isolation Strategies

**Option A: Row-Level Security (Recommended for MVP)**
```sql
-- PostgreSQL RLS policies
ALTER TABLE detection_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON detection_events 
USING (tenant_id = current_setting('app.current_tenant')::UUID);

-- Application sets tenant context per request
SET app.current_tenant = 'tenant-uuid';
```

**Option B: Schema Per Tenant (Platform Tier)**
```sql
-- Enterprise customers get dedicated schema
CREATE SCHEMA tenant_abc123;
CREATE TABLE tenant_abc123.events (...);
```

**Option C: Database Per Tenant (Future)**
Full isolation at database level for compliance requirements.

### 5.2 Encryption Strategy

| Layer | Mechanism | Implementation |
|-------|-----------|----------------|
| **In Transit** | TLS 1.3 | All service-to-service communication |
| **At Rest (DB)** | AES-256 | PostgreSQL with pgcrypto extension |
| **At Rest (Obj)** | SSE-S3/SSE-KMS | MinIO or AWS S3 encryption |
| **Application** | Field-level | Encrypt integration credentials, PII |
| **Backup** | AES-256 | Encrypted backups with customer-managed keys |

### 5.3 Authentication & Authorization

**Identity Provider: Keycloak**
- OpenID Connect / OAuth 2.0
- MFA support (TOTP, WebAuthn)
- LDAP/Active Directory federation for enterprise
- Session management per tenant

**Authorization Model:**
```
Role Hierarchy per Tenant:
├── Admin (Full access)
├── Security Analyst (Read + Write + Response)
├── Viewer (Read-only)
└── API Key (Service-to-service)

Permissions:
├── assets:read, assets:write
├── detections:read, detections:acknowledge
├── response:execute (tier-dependent)
└── admin:* (tenant config)
```

---

## 6. Deployment Architecture

### 6.1 Infrastructure as Code

**Technology Stack:**
- **Terraform**: Infrastructure provisioning
- **Helm**: Kubernetes application deployment
- **GitOps**: ArgoCD or Flux for continuous deployment

**Environment Strategy:**
```
┌─────────────────────────────────────────────────────────┐
│                  PRODUCTION                            │
│  Region: South Africa (AWS Cape Town / Azure Gauteng)   │
│  Profile: High availability, multi-AZ, backups       │
├─────────────────────────────────────────────────────────┤
│                  STAGING                               │
│  Region: Same as prod (smaller instances)             │
│  Profile: Production-like for testing                   │
├─────────────────────────────────────────────────────────┤
│                  DEVELOPMENT                           │
│  Region: Local minikube / k3s or cloud dev             │
│  Profile: Minimal resources, fast iteration             │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Kubernetes Architecture

**Namespace Strategy (per-environment):**
```
namespace: production
├── ingress-nginx (Ingress controller)
├── keycloak (Auth)
├── platform-core (Core services)
├── platform-data (Databases, caches)
├── platform-agents (Agent management)
└── monitoring (Prometheus, Grafana)
```

**Pod Security:**
- Non-root containers
- Read-only filesystems
- Security contexts (drop all capabilities)
- Network policies (intra-service firewalls)

---

## 7. Scalability & Performance

### 7.1 Horizontal Scaling Targets

| Metric | MVP | Scale Target |
|--------|-----|--------------|
| Concurrent Tenants | 50 | 500+ |
| Agents per Tenant | 100 | 1000+ |
| Events/sec (total) | 1,000 | 50,000+ |
| Event Retention | 30 days | 90 days hot, 1 year cold |
| API Response Time | <500ms p95 | <200ms p95 |
| Dashboard Load | <3s | <1s |

### 7.2 Performance Optimizations

**Database:**
- TimescaleDB chunking by time + tenant
- Continuous aggregates for common queries
- Partition pruning for efficient deletes
- Read replicas for analytics queries

**Caching Strategy:**
- Redis for session tokens (TTL: 24h)
- Asset metadata caching (TTL: 5min)
- Threat intel lists (TTL: 1h)
- Dashboard query results (TTL: 1-5min)

**Network (African Context):**
- Edge caching for dashboard assets (CDN)
- Delta compression for agent updates
- Configurable batch sizes (work with constrained bandwidth)
- Local agents buffer during outages

---

## 8. Observability & Monitoring

### 8.1 Three Pillars

**Metrics (Prometheus/Grafana):**
- API request latency, error rates, throughput
- Database connection pools, query times
- Agent heartbeat status per tenant
- Infrastructure utilization (CPU, memory, disk)

**Logging (OpenSearch/Loki):**
- Structured JSON logging from all services
- Correlation IDs across distributed traces
- Per-tenant log aggregation (with access controls)
- Alert on ERROR/FATAL patterns

**Tracing (Jaeger/Zipkin):**
- Distributed request tracing
- Latency analysis across services
- Error propagation tracking

### 8.2 Health Checks

- **Liveness/Readiness**: Kubernetes probes for all services
- **Synthetic Transactions**: Periodic end-to-end tests
- **Agent Heartbeat**: Expected check-in intervals with alerting
- **Data Freshness**: Monitoring for stalled ingestion pipelines

---

## 9. Disaster Recovery & Business Continuity

### 9.1 Backup Strategy

**Hot Data (TimescaleDB):**
- Hourly snapshots to object storage
- Point-in-time recovery (PITR) enabled
- Cross-region replication for critical tenants

**Cold Data (Object Storage):**
- Versioning enabled
- Cross-region replication (asynchronous)
- Glacier Deep Archive for long-term retention

**Configuration:**
- Git-based infrastructure (Terraform/Helm)
- Regular etcd backups for Kubernetes
- Keycloak realm exports

### 9.2 Recovery Time Objectives

| Component | RTO | RPO |
|-----------|-----|-----|
| Control Plane | <30 min | <15 min |
| Data Plane (Hot) | <60 min | <5 min |
| Data Plane (Cold) | <4 hours | <1 hour |
| Agent Fleet | <15 min (reconnect) | N/A |

### 9.3 Multi-Region Deployment (Future)

For Platform tier customers requiring geographic redundancy:
- Active-passive setup between SA and EU regions
- DNS failover with health checks
- Eventual consistency for non-critical data
- Manual failover for data integrity assurance

---

## 10. African Market Optimizations

### 10.1 Connectivity Resilience

**Agent-Side:**
- Local SQLite buffer during outages
- Configurable sync intervals (15min - 24h)
- Exponential backoff for failed transmissions
- Bandwidth throttling options

**Service-Side:**
- Idempotent event processing (handle duplicates gracefully)
- Out-of-order event tolerance
- Graceful degradation when upstream dependencies lag
- Bandwidth-aware alerting (reduce frequency during detected congestion)

### 10.2 Localization & Compliance

**Data Residency:**
- Tenant-selectable regions (ZA-CPT-01, ZA-JHB-01, EU-FRK-01)
- Data never leaves selected region without explicit consent
- POPIA-compliant data processing agreements

**Local Threat Intelligence:**
- Integration with African CERT feeds
- Regional malware signature packs
- Local language support for alerts/reports (English, Afrikaans, Zulu, Xhosa)

### 10.3 Cost Optimization

**Tiered Storage:**
- Hot (SSD): Last 7 days
- Warm (HDD): Days 8-30
- Cold (Object): Beyond 30 days
- Archive (Glacier): Beyond 1 year for compliance

**Right-sizing:**
- Burstable instances for dev/test
- Spot instances for batch processing
- Autoscaling based on actual tenant load

---

## 11. Technology Stack Details

### 11.1 Backend Services

| Service | Technology | Purpose |
|---------|------------|---------|
| API Gateway | Kong / Traefik | Rate limiting, auth, routing |
| Auth Service | Keycloak | OIDC, SAML, LDAP, MFA |
| Tenant Service | Go / Python | Provisioning, config management |
| Detection Engine | Go (Apache Flink optional) | Stream processing, rule engine |
| Vulnerability Scanner | Go / Python | Trivy/OpenVAS wrapper, scheduling |
| Asset Service | Python / Node.js | Inventory management, grouping |
| Notification Service | Python | Email, SMS, webhook delivery |
| Billing Service | Python | Usage metering, invoice generation |
| Admin Dashboard | React/TypeScript | Super-admin tenant management |

### 11.2 Data Stores

| Store | Technology | Use Case |
|-------|------------|----------|
| Primary OLTP | PostgreSQL 15 | Tenant config, user management, assets |
| Time-Series | TimescaleDB 2.9 | Detection events, metrics, audit logs |
| Document Store | PostgreSQL JSONB | Flexible schemas (scan results, configs) |
| Search | OpenSearch 2.x | Log search, threat intel lookup |
| Cache | Redis 7 | Sessions, rate limiting, frequent queries |
| Object Storage | MinIO / AWS S3 | Forensics, backups, long-term retention |
| Message Bus | NATS / Kafka | Event streaming, decoupling services |

### 11.3 Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Dashboard | React 18 + TypeScript | Main user interface |
| State Management | Redux Toolkit / Zustand | Predictable state updates |
| UI Library | Ant Design / Material-UI | Consistent, accessible components |
| Charts | Recharts / Chart.js | Visualization of metrics/trends |
| Maps | Leaflet / Mapbox | Geolocation of assets/events |
| Mobile | React Native (Future) | Limited field operations view |

### 11.4 DevOps & Infrastructure

| Tool | Purpose |
|------|---------|
| Terraform | Infrastructure provisioning (AWS/Azure) |
| Helm | Kubernetes application packaging |
| ArgoCD | GitOps continuous deployment |
| GitHub Actions | CI/CD pipeline |
| Prometheus + Grafana | Infrastructure & application monitoring |
| Loki | Log aggregation |
| Jaeger | Distributed tracing |
| Trivy | Container image scanning |
| SOPS | Secret encryption |

---

## 12. Implementation Roadmap

### 12.0 Phase 0: Foundations (Month 0)
- [ ] Set up GitHub repo with branch protection
- [ ] Establish CI/CD pipeline (linting, testing)
- [ ] Create basic Kubernetes manifests
- [ ] Design and implement tenant onboarding flow
- [ ] Set up development environment (minikube/k3s)

### 12.1 Phase 1: MVP - Core Detection (Months 1-3)
- [ ] Implement OSQuery/Wazuh agent deployment
- [ ] Build event ingestion pipeline (NATS → Vector → TimescaleDB)
- [ ] Create detection rule engine (Sigma rule support)
- [ ] Develop basic asset management CRUD
- [ ] Build alerting system (email/webhook)
- [ ] Implement Role-Based Access Control (RBAC)
- [ ] Create tenant isolation (RLS implementation)
- [ ] Develop Grafana dashboard templates
- [ ] Setup Keycloak for authentication
- [ ] Implement audit logging

### 12.2 Phase 2: Vulnerability Management & Response (Months 4-6)
- [ ] Integrate OpenVAS/Trivy for vulnerability scanning
- [ ] Build vulnerability tracking and remediation workflow
- [ ] Add Velociraptor for deep forensics capability
- [ ] Implement basic response actions (isolate endpoint, block IP)
- [ ] Create response playbook editor (YAML/JSON based)
- [ ] Add threat intelligence feeds (MISP/Abuse.ch)
- [ ] Implement continuous compliance reporting (POPIA basics)
- [ ] Build customer self-service portal

### 12.3 Phase 3: Scaling & African Optimizations (Months 7-9)
- [ ] Implement multi-tenant database sharding strategy
- [ ] Add connection pooling and query optimization
- [ ] Develop bandwidth optimization (delta compression, batching)
- [ ] Add local buffering for intermittent connectivity
- [ ] Implement CDN for dashboard assets
- [ ] Add multi-region deployment capability
- [ ] Create automated backup and disaster recovery procedures
- [ ] Implement usage-based metering and billing

### 12.4 Phase 4: Advanced Features & Enterprise (Months 10-12)
- [ ] Develop native agent to replace open-source components
- [ ] Add machine learning anomaly detection (optional tier)
- [ ] Build full SOAR capabilities (Shuffle integration)
- [ ] Implement white-labeling for Platform tier
- [ ] Add API rate limiting and quota management
- [ ] Create partner/MSSP portal
- [ ] Achieve ISO 27001 certification baseline
- [ ] Conduct penetration testing and security audit
- [ ] Launch pilot with 3-5 South African SMEs

---

## 13. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Agent deployment complexity | High | Medium | Provide multiple deployment methods (script, MSI, deb/rpm, container) |
| Data overload from agents | Medium | High | Implement aggressive filtering at agent, configurable sampling |
| Alert fatigue | Medium | High | Tiered alerting, suppression rules, ML-based prioritization |
| Connectivity issues in Africa | High | Medium | Robust offline buffering, configurable sync, bandwidth awareness |
| Open source dependency risks | Low | Medium | Maintain abstraction layers, track CVEs, have replacement paths |
| Regulatory changes (POPIA) | Low | High | Modular compliance framework, regular legal review |
| Competition from established players | Medium | Medium | Focus on African market, SME-specific pricing, local support |
| Talent acquisition | Medium | Medium | Remote-first hiring, competitive compensation, clear mission |

---

## 14. Open Questions for Next Steps

1. **Initial Technology Choice**: Python/FastAPI vs Go for backend services?
2. **Message Bus**: NATS (simpler) vs Kafka (more enterprise features)?
3. **Frontend Framework**: React vs Vue.js vs Svelte?
4. **Deployment Target**: Managed K8s (EKS/AKS) vs self-managed vs k3s for edge?
5. **Pilot Design**: Which 2-3 South African SMEs for initial testing?
6. **Compliance Priority**: POPIA first vs ISO 27001 vs PCI DSS?
7. **Partner Strategy**: Build direct sales vs MSSP channel first?
8. **Funding Approach**: Bootstrapped vs seek angel/VC for faster growth?

---

**Document Status**: This is a living document that will evolve as the architecture is validated through prototyping and customer feedback.  
**Next Review**: Schedule technical architecture review after MVP feature completion (end of Month 3).

*Authored by: Rosie Bandile, AI Assistant*  
*For: Tshephang (Founder) & Sisa (Marketing Director)*  
*Company: Cybersecurity SaaS Platform for African SMEs*