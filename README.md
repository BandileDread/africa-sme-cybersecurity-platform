# Africa SME Cybersecurity Platform (AfriSec) 🔒

> **Cybersecurity-as-a-Service for Small and Medium Enterprises in South Africa**

[![License](https://img.shields.io/badge/License-CC--BY--NC--4.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Self--Hosted-green)](https://github.com/BandileDread/africa-sme-cybersecurity-platform)
[![POPIA](https://img.shields.io/badge/POPIA-Compliant-orange)](https://popia.gov.za/)

## 🌍 Overview

AfriSec is a **Cybersecurity-as-a-Service (CSaaS)** platform designed specifically for **Small and Medium Enterprises (SMEs)** operating in **South Africa**. We recognize that SMEs face the same cybersecurity threats as large enterprises but lack the budget, expertise, and resources to implement traditional enterprise-grade security solutions.

**Our Approach** 🎯
- 🔓 **Open-source foundation**: We build on battle-tested open-source security tools (OpenVAS, Suricata, Wazuh, etc.)
- 🧩 **Integration code** = **Your IP**: The scripts, configurations, dashboards, and business logic that stitch these tools together into a cohesive, automated service
- 🎓 **Built-in compliance**: POPIA (Protection of Personal Information Act) compliance built-in
- 💰 **Affordable**: Designed for SME budgets
- ☁️ **Flexible deployment**: Self-hosted or cloud-based

## 📚 Documentation Structure

```
africa-sme-cybersecurity-platform/
├── README.md              # This file - overview and getting started
├── TECHNICAL_ARCHITECTURE.md  # Complete system architecture and design
├── docs/                  # Comprehensive documentation
│   ├── getting-started/
│   ├── api-reference/
│   └── deployment-guides/
├── src/                   # Source code (your IP - the integration layer)
│   ├── api/              # RESTful API services
│   ├── automation/       # Security orchestration scripts
│   ├── agents/           # Endpoint monitoring agents
│   └── integrations/     # Third-party tool connectors
├── configs/              # Configuration templates
├── scripts/              # Deployment and management scripts
├── business-ops/         # Business operations and project management
├── mission-control/      # Platform management and orchestration
├── nguni-force-landing/  # Customer-facing portal
├── ops-docs/             # Operational documentation (SOPs, policies)
└── tests/                # Test suites and validation scripts
```

## 🚀 Key Features

### Core Security Stack 🔐

| Layer | Open-Source Tool | Our Integration | Function |
|-------|-----------------|-----------------|----------|
| **Vulnerability Management** | OpenVAS | 🛠️ AfriSec Scanner Orchestrator | Automated scanning, risk prioritization, POPIA-mapped findings |
| **Network Security (IDS/IPS)** | Suricata | 🛠️ AfriSec Threat Engine | Real-time monitoring, automated response, SIEM integration |
| **Endpoint Protection** | Wazuh/OSSEC | 🛠️ AfriSec Agent Manager | Unified endpoint monitoring, file integrity monitoring, compliance checks |
| **Log Analysis** | Elasticsearch + Kibana | 🛠️ AfriSec SIEM Dashboard | Centralized logging, threat hunting, compliance reporting |
| **Malware Scanning** | ClamAV | 🛠️ AfriSec Malware Scanner | Scheduled scans, quarantine automation, threat intelligence feeds |
| **Web Security** | ModSecurity | 🛠️ AfriSec WAF Manager | POPIA-aware rule sets, DDoS protection, API security |

### POPIA Compliance Features 🇿🇦

✅ **Data Protection Impact Assessment (DPIA)** tool  
✅ **Data Subject Rights** management portal  
✅ **Breach notification** workflow and templates  
✅ **Consent and purpose** tracking system  
✅ **Automated compliance** checking and reporting  
✅ **Audit trail** generation for POPIA inspections

### SME-Friendly Interface 👥

- 📱 **Landing portal** (`nguni-force-landing/`) - Customer self-service dashboard
- 📊 **Executive dashboards** - Non-technical CyberScore and risk summaries  
- 🔗 **API-first** - Easy integration with existing SME tools
- 📧 **Automated alerts** - Only critical issues distilled into actionable alerts
- 💬 **South African context** - Local threat intelligence, currency, regulations

## 🏗️ Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ SME Portal  │  │ Mobile App  │  │ Agent IF    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   API GATEWAY                                │
│            (Authentication, Rate Limiting)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  CORE SERVICES                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Scanner  │ │  SIEM    │ │Compliance│ │Workflow  │      │
│  │ Service  │ │ Service  │ │ Service  │ │ Engine   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              SECURITY TOOLS (Open Source)                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│  │OpenVAS │ │Suricata│ │ Wazuh  │ │ ClamAV │ │ES+Kibana│ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Our Code (IP)**: The integration layer (blue boxes above) - APIs, orchestration scripts, dashboards, and business logic that transforms individual tools into a managed security service.

**Open Source Tools** (orange boxes): The underlying security engines we orchestrate and manage.

## 🎯 Quick Start

### Prerequisites

- Ubuntu 22.04 LTS or Debian 11+
- 4GB RAM minimum (8GB recommended)
- 50GB storage minimum
- Docker + Docker Compose
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/BandileDread/africa-sme-cybersecurity-platform.git
cd africa-sme-cybersecurity-platform

# Run the setup script
chmod +x scripts/quickstart.sh
./scripts/quickstart.sh

# Access the platform
# Default web interface: http://localhost:8080
# API endpoint: http://localhost:8080/api/v1
```

### Verify Installation

```bash
# Check all services are running
./scripts/status.sh

# Run a test vulnerability scan
./scripts/test-scan.sh --target localhost

# Check API health
curl http://localhost:8080/api/v1/health
```

## 🔧 Development

### Setting Up Dev Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Start development server
flask run --debug
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🛡️ Security & Compliance

- **Security Policy**: See [ops-docs/security-policy.md](ops-docs/security-policy.md)
- **POPIA Compliance Checklist**: See [popiaguardian-checklist.md](popiaguardian-checklist.md)
- **Incident Response**: See [ops-docs/incident-response-sop.md](ops-docs/incident-response-sop.md)
- **Vulnerability Disclosure**: Email security@afrisec.co.za

## 📊 Business Operations

- **Business Plans**: See [business-ops/](/business-ops/)
- **Projects**: See [business-ops/projects/](/business-ops/projects/)
- **Marketing Strategy**: See [business-ops/