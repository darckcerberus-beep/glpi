#!/usr/bin/env python3
"""
Generate comprehensive mock data for Applications, Servers, Software Components, and Vulnerabilities.
Outputs in both CSV and JSON formats, as well as a direct SQL seeding script for GLPI.
"""

import os
import json
import csv
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "csv")
JSON_DIR = os.path.join(BASE_DIR, "json")
SQL_DIR = os.path.join(BASE_DIR, "sql")

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

# --------------------------------------------------------------------------
# 1. Applications Mock Data
# --------------------------------------------------------------------------
APPLICATIONS = [
    {
        "id": 1,
        "app_code": "APP-BANK-001",
        "name": "Core Banking API Gateway",
        "criticality": 4, # 4 = Mission Critical (Tier 1)
        "criticality_label": "4 - Mission Critical (Tier 1)",
        "environment": "production",
        "exposure": "partner",
        "business_unit": "Retail & Digital Banking",
        "business_owner": "Sarah Jenkins (VP Digital Banking)",
        "tech_lead": "Alex Rivera (Principal SRE)",
        "team": "Banking Core Infrastructure",
        "description": "High-throughput API gateway routing real-time customer account inquiries, ledger updates, and balance checks."
    },
    {
        "id": 2,
        "app_code": "APP-ECOM-002",
        "name": "Customer E-Commerce Storefront",
        "criticality": 4,
        "criticality_label": "4 - Mission Critical (Tier 1)",
        "environment": "production",
        "exposure": "external",
        "business_unit": "Digital Commerce",
        "business_owner": "Michael Chang (VP Customer Experience)",
        "tech_lead": "Elena Rostova (Lead Web Architect)",
        "team": "Frontend Operations",
        "description": "Public-facing international shopping platform, product catalog search, and customer checkout engine."
    },
    {
        "id": 3,
        "app_code": "APP-PAY-003",
        "name": "Global Payment Settlement Engine",
        "criticality": 4,
        "criticality_label": "4 - Mission Critical (Tier 1)",
        "environment": "production",
        "exposure": "external",
        "business_unit": "Payment Services",
        "business_owner": "David Chen (Director of Merchant Solutions)",
        "tech_lead": "Marcus Brody (Security & Compliance Lead)",
        "team": "Payments Engineering",
        "description": "PCI-DSS Level 1 compliant credit card processing, 3D-Secure 2.0 authorization, and SEPA/SWIFT clearing system."
    },
    {
        "id": 4,
        "app_code": "APP-DATA-004",
        "name": "Real-Time Fraud & Risk Analytics Pipeline",
        "criticality": 3, # 3 = High (Tier 2)
        "criticality_label": "3 - High (Tier 2)",
        "environment": "production",
        "exposure": "internal",
        "business_unit": "Risk Management & Compliance",
        "business_owner": "Patricia Howard (Chief Risk Officer)",
        "tech_lead": "Vikram Patel (Principal Data Engineer)",
        "team": "Data Platform Team",
        "description": "Streaming analytics pipeline utilizing Apache Spark and machine learning models for anomaly scoring on transactions."
    },
    {
        "id": 5,
        "app_code": "APP-HR-005",
        "name": "Human Resources & Payroll Hub",
        "criticality": 2, # 2 = Medium (Tier 3)
        "criticality_label": "2 - Medium (Tier 3)",
        "environment": "production",
        "exposure": "internal",
        "business_unit": "People & Organization",
        "business_owner": "Claire Dubois (Head of HR Ops)",
        "tech_lead": "Thomas Weber (Enterprise Systems Specialist)",
        "team": "Corporate Systems",
        "description": "Internal employee self-service portal, annual compensation review, payroll records, and benefits administration."
    },
    {
        "id": 6,
        "app_code": "APP-OPS-006",
        "name": "DevOps CI/CD Automation Platform",
        "criticality": 3,
        "criticality_label": "3 - High (Tier 2)",
        "environment": "production",
        "exposure": "internal",
        "business_unit": "Engineering Platform",
        "business_owner": "Arjun Mehta (VP Platform Engineering)",
        "tech_lead": "Samira Khan (Staff DevOps Engineer)",
        "team": "Platform SRE",
        "description": "Central build and continuous delivery cluster orchestrating container builds, vulnerability scans, and deployments."
    },
    {
        "id": 7,
        "app_code": "APP-STG-007",
        "name": "Customer Support Staging Environment",
        "criticality": 1, # 1 = Low (Tier 4)
        "criticality_label": "1 - Low (Tier 4)",
        "environment": "staging",
        "exposure": "internal",
        "business_unit": "Customer Support",
        "business_owner": "Laura Gomez (Support Director)",
        "tech_lead": "Kevin O'Connor (QA Lead)",
        "team": "QA & Automation",
        "description": "Pre-production mirror used for regression validation and customer support agent training before releases."
    },
    {
        "id": 8,
        "app_code": "APP-DR-008",
        "name": "Disaster Recovery Standby Core",
        "criticality": 4,
        "criticality_label": "4 - Mission Critical (Tier 1)",
        "environment": "dr",
        "exposure": "internal",
        "business_unit": "Business Continuity",
        "business_owner": "Robert Henderson (Head of BCP)",
        "tech_lead": "Alex Rivera (Principal SRE)",
        "team": "Banking Core Infrastructure",
        "description": "Warm standby cluster synchronized asynchronously with Core Banking API and ledger databases in secondary DC."
    }
]

# --------------------------------------------------------------------------
# 2. Servers Mock Data (GLPI Computers)
# --------------------------------------------------------------------------
SERVERS = [
    {
        "id": 1,
        "hostname": "srv-bank-api-01.prod.internal",
        "ip": "10.10.10.11",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-A04",
        "cpu_cores": 16,
        "ram_gb": 64,
        "status": "In Service",
        "primary_role": "Primary API Gateway"
    },
    {
        "id": 2,
        "hostname": "srv-bank-api-02.prod.internal",
        "ip": "10.10.10.12",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-A05",
        "cpu_cores": 16,
        "ram_gb": 64,
        "status": "In Service",
        "primary_role": "Secondary API Gateway"
    },
    {
        "id": 3,
        "hostname": "srv-bank-db-01.prod.internal",
        "ip": "10.10.10.21",
        "os": "Red Hat Enterprise Linux",
        "os_version": "9.2",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-B01",
        "cpu_cores": 32,
        "ram_gb": 256,
        "status": "In Service",
        "primary_role": "Primary Relational DB"
    },
    {
        "id": 4,
        "hostname": "srv-ecom-web-01.prod.internal",
        "ip": "10.20.10.11",
        "os": "Debian GNU/Linux",
        "os_version": "12.1",
        "environment": "production",
        "datacenter": "DC-Amsterdam-02",
        "rack": "RACK-W01",
        "cpu_cores": 8,
        "ram_gb": 32,
        "status": "In Service",
        "primary_role": "Web Reverse Proxy / Load Balancer"
    },
    {
        "id": 5,
        "hostname": "srv-ecom-web-02.prod.internal",
        "ip": "10.20.10.12",
        "os": "Debian GNU/Linux",
        "os_version": "12.1",
        "environment": "production",
        "datacenter": "DC-Amsterdam-02",
        "rack": "RACK-W02",
        "cpu_cores": 8,
        "ram_gb": 32,
        "status": "In Service",
        "primary_role": "Web Reverse Proxy / Load Balancer"
    },
    {
        "id": 6,
        "hostname": "srv-ecom-app-01.prod.internal",
        "ip": "10.20.10.21",
        "os": "Ubuntu Linux",
        "os_version": "20.04 LTS",
        "environment": "production",
        "datacenter": "DC-Amsterdam-02",
        "rack": "RACK-W03",
        "cpu_cores": 16,
        "ram_gb": 64,
        "status": "In Service",
        "primary_role": "E-Commerce Application Server"
    },
    {
        "id": 7,
        "hostname": "srv-ecom-cache-01.prod.internal",
        "ip": "10.20.10.31",
        "os": "Debian GNU/Linux",
        "os_version": "12.1",
        "environment": "production",
        "datacenter": "DC-Amsterdam-02",
        "rack": "RACK-W04",
        "cpu_cores": 8,
        "ram_gb": 32,
        "status": "In Service",
        "primary_role": "Redis Cache & Session Store"
    },
    {
        "id": 8,
        "hostname": "srv-pay-proc-01.pci.internal",
        "ip": "10.30.10.10",
        "os": "Red Hat Enterprise Linux",
        "os_version": "8.8",
        "environment": "production",
        "datacenter": "DC-Dublin-PCI",
        "rack": "RACK-PCI-01",
        "cpu_cores": 16,
        "ram_gb": 64,
        "status": "In Service",
        "primary_role": "Transaction Processing Engine"
    },
    {
        "id": 9,
        "hostname": "srv-pay-hsm-01.pci.internal",
        "ip": "10.30.10.20",
        "os": "Hardened Linux",
        "os_version": "Enterprise 5.4",
        "environment": "production",
        "datacenter": "DC-Dublin-PCI",
        "rack": "RACK-PCI-02",
        "cpu_cores": 8,
        "ram_gb": 16,
        "status": "In Service",
        "primary_role": "Hardware Security Module (HSM) Proxy"
    },
    {
        "id": 10,
        "hostname": "srv-data-spark-01.prod.internal",
        "ip": "10.50.10.31",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-D01",
        "cpu_cores": 32,
        "ram_gb": 128,
        "status": "In Service",
        "primary_role": "Spark Master Node"
    },
    {
        "id": 11,
        "hostname": "srv-data-worker-01.prod.internal",
        "ip": "10.50.10.32",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-D02",
        "cpu_cores": 32,
        "ram_gb": 128,
        "status": "In Service",
        "primary_role": "Spark Analytics Worker"
    },
    {
        "id": 12,
        "hostname": "srv-hr-app-01.corp.internal",
        "ip": "10.40.10.15",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-C03",
        "cpu_cores": 8,
        "ram_gb": 32,
        "status": "In Service",
        "primary_role": "HR Self-Service Host"
    },
    {
        "id": 13,
        "hostname": "srv-ops-ci-01.corp.internal",
        "ip": "10.60.10.50",
        "os": "Ubuntu Linux",
        "os_version": "22.04 LTS",
        "environment": "production",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-O01",
        "cpu_cores": 24,
        "ram_gb": 96,
        "status": "In Service",
        "primary_role": "Jenkins CI Master & Build Engine"
    },
    {
        "id": 14,
        "hostname": "srv-sup-stage-01.stg.internal",
        "ip": "10.70.10.88",
        "os": "Debian GNU/Linux",
        "os_version": "11.7",
        "environment": "staging",
        "datacenter": "DC-Frankfurt-01",
        "rack": "RACK-T01",
        "cpu_cores": 4,
        "ram_gb": 16,
        "status": "In Service",
        "primary_role": "Staging Support Application"
    },
    {
        "id": 15,
        "hostname": "srv-dr-core-01.dr.internal",
        "ip": "10.80.10.101",
        "os": "Red Hat Enterprise Linux",
        "os_version": "9.2",
        "environment": "dr",
        "datacenter": "DC-Paris-DR",
        "rack": "RACK-DR-01",
        "cpu_cores": 32,
        "ram_gb": 256,
        "status": "In Service",
        "primary_role": "Disaster Recovery Warm Standby"
    }
]

# --------------------------------------------------------------------------
# 3. Software Components Mock Data (GLPI Softwares & Versions)
# --------------------------------------------------------------------------
SOFTWARE_COMPONENTS = [
    {
        "software_id": 1,
        "name": "Apache Tomcat",
        "category": "Application Server / Servlet Container",
        "vendor": "Apache Software Foundation",
        "version_id": 1,
        "version": "9.0.58",
        "is_vulnerable": True,
        "cve_ref": "CVE-2022-22965"
    },
    {
        "software_id": 1,
        "name": "Apache Tomcat",
        "category": "Application Server / Servlet Container",
        "vendor": "Apache Software Foundation",
        "version_id": 2,
        "version": "10.1.18",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 2,
        "name": "Spring Framework",
        "category": "Java Application Framework",
        "vendor": "VMware / Spring",
        "version_id": 3,
        "version": "5.3.18",
        "is_vulnerable": True,
        "cve_ref": "CVE-2022-22965"
    },
    {
        "software_id": 2,
        "name": "Spring Framework",
        "category": "Java Application Framework",
        "vendor": "VMware / Spring",
        "version_id": 4,
        "version": "6.0.14",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 3,
        "name": "Apache Log4j",
        "category": "Java Logging Framework",
        "vendor": "Apache Software Foundation",
        "version_id": 5,
        "version": "2.14.1",
        "is_vulnerable": True,
        "cve_ref": "CVE-2021-44228"
    },
    {
        "software_id": 3,
        "name": "Apache Log4j",
        "category": "Java Logging Framework",
        "vendor": "Apache Software Foundation",
        "version_id": 6,
        "version": "2.17.1",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 4,
        "name": "Nginx",
        "category": "Web Server / Reverse Proxy",
        "vendor": "F5 / Nginx",
        "version_id": 7,
        "version": "1.20.1",
        "is_vulnerable": True,
        "cve_ref": "CVE-2023-44487"
    },
    {
        "software_id": 4,
        "name": "Nginx",
        "category": "Web Server / Reverse Proxy",
        "vendor": "F5 / Nginx",
        "version_id": 8,
        "version": "1.24.0",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 5,
        "name": "OpenSSH",
        "category": "Remote Access / Secure Shell",
        "vendor": "OpenBSD Foundation",
        "version_id": 9,
        "version": "8.9p1",
        "is_vulnerable": True,
        "cve_ref": "CVE-2024-6387"
    },
    {
        "software_id": 5,
        "name": "OpenSSH",
        "category": "Remote Access / Secure Shell",
        "vendor": "OpenBSD Foundation",
        "version_id": 10,
        "version": "9.8p1",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 6,
        "name": "OpenSSL",
        "category": "Cryptographic Library",
        "vendor": "OpenSSL Project",
        "version_id": 11,
        "version": "1.1.1k",
        "is_vulnerable": True,
        "cve_ref": "CVE-2022-3602"
    },
    {
        "software_id": 6,
        "name": "OpenSSL",
        "category": "Cryptographic Library",
        "vendor": "OpenSSL Project",
        "version_id": 12,
        "version": "3.0.12",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 7,
        "name": "PostgreSQL",
        "category": "Relational Database Management System",
        "vendor": "PostgreSQL Global Development Group",
        "version_id": 13,
        "version": "14.8",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 8,
        "name": "Redis",
        "category": "In-Memory Data Store & Cache",
        "vendor": "Redis Ltd",
        "version_id": 14,
        "version": "6.2.5",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 9,
        "name": "RabbitMQ",
        "category": "Message Broker",
        "vendor": "VMware",
        "version_id": 15,
        "version": "3.9.15",
        "is_vulnerable": False,
        "cve_ref": ""
    },
    {
        "software_id": 10,
        "name": "Apache Spark",
        "category": "Distributed Computing Framework",
        "vendor": "Apache Software Foundation",
        "version_id": 16,
        "version": "3.2.0",
        "is_vulnerable": True,
        "cve_ref": "CVE-2022-33891"
    },
    {
        "software_id": 11,
        "name": "Apache HTTP Server",
        "category": "Web Server",
        "vendor": "Apache Software Foundation",
        "version_id": 17,
        "version": "2.4.49",
        "is_vulnerable": True,
        "cve_ref": "CVE-2021-41773"
    },
    {
        "software_id": 12,
        "name": "Jenkins",
        "category": "Continuous Integration Automation Server",
        "vendor": "Jenkins Project",
        "version_id": 18,
        "version": "2.441",
        "is_vulnerable": True,
        "cve_ref": "CVE-2024-23897"
    },
    {
        "software_id": 13,
        "name": "Node.js",
        "category": "JavaScript Runtime",
        "vendor": "OpenJS Foundation",
        "version_id": 19,
        "version": "16.14.0",
        "is_vulnerable": True,
        "cve_ref": "CVE-2023-30533"
    }
]

# --------------------------------------------------------------------------
# 4. Application <-> Server Mappings (ApplicationAsset links)
# --------------------------------------------------------------------------
APPLICATION_SERVERS = [
    {"application_id": 1, "server_id": 1, "role": "Primary API Gateway"},
    {"application_id": 1, "server_id": 2, "role": "Secondary API Gateway"},
    {"application_id": 1, "server_id": 3, "role": "Transactional Database"},
    {"application_id": 2, "server_id": 4, "role": "Web Load Balancer (Front)"},
    {"application_id": 2, "server_id": 5, "role": "Web Load Balancer (Front)"},
    {"application_id": 2, "server_id": 6, "role": "Application Server"},
    {"application_id": 2, "server_id": 7, "role": "Session Cache"},
    {"application_id": 3, "server_id": 8, "role": "Payment Settlement Core"},
    {"application_id": 3, "server_id": 9, "role": "Hardware Security Module"},
    {"application_id": 4, "server_id": 10, "role": "Spark Analytics Master"},
    {"application_id": 4, "server_id": 11, "role": "Spark Worker Node"},
    {"application_id": 5, "server_id": 12, "role": "Corporate HR Portal Host"},
    {"application_id": 6, "server_id": 13, "role": "CI/CD Master Build Host"},
    {"application_id": 7, "server_id": 14, "role": "Staging Application Server"},
    {"application_id": 8, "server_id": 15, "role": "DR Standby Node"}
]

# --------------------------------------------------------------------------
# 5. Server <-> Software Installed (glpi_items_softwareversions)
# --------------------------------------------------------------------------
SERVER_SOFTWARE = [
    # srv-bank-api-01 (Ubuntu 22.04): OpenSSH 8.9p1, Apache Tomcat 9.0.58, Spring 5.3.18
    {"server_id": 1, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},
    {"server_id": 1, "software_id": 1, "software_name": "Apache Tomcat", "version_id": 1, "version": "9.0.58"},
    {"server_id": 1, "software_id": 2, "software_name": "Spring Framework", "version_id": 3, "version": "5.3.18"},

    # srv-bank-api-02: OpenSSH 8.9p1, Apache Tomcat 9.0.58, Spring 5.3.18
    {"server_id": 2, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},
    {"server_id": 2, "software_id": 1, "software_name": "Apache Tomcat", "version_id": 1, "version": "9.0.58"},
    {"server_id": 2, "software_id": 2, "software_name": "Spring Framework", "version_id": 3, "version": "5.3.18"},

    # srv-bank-db-01: OpenSSH 9.8p1 (patched), PostgreSQL 14.8
    {"server_id": 3, "software_id": 5, "software_name": "OpenSSH", "version_id": 10, "version": "9.8p1"},
    {"server_id": 3, "software_id": 7, "software_name": "PostgreSQL", "version_id": 13, "version": "14.8"},

    # srv-ecom-web-01: Nginx 1.20.1, OpenSSH 8.9p1
    {"server_id": 4, "software_id": 4, "software_name": "Nginx", "version_id": 7, "version": "1.20.1"},
    {"server_id": 4, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-ecom-web-02: Nginx 1.20.1, OpenSSH 8.9p1
    {"server_id": 5, "software_id": 4, "software_name": "Nginx", "version_id": 7, "version": "1.20.1"},
    {"server_id": 5, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-ecom-app-01: Apache Log4j 2.14.1, Node.js 16.14.0, OpenSSH 8.9p1
    {"server_id": 6, "software_id": 3, "software_name": "Apache Log4j", "version_id": 5, "version": "2.14.1"},
    {"server_id": 6, "software_id": 13, "software_name": "Node.js", "version_id": 19, "version": "16.14.0"},
    {"server_id": 6, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-ecom-cache-01: Redis 6.2.5, OpenSSH 9.8p1
    {"server_id": 7, "software_id": 8, "software_name": "Redis", "version_id": 14, "version": "6.2.5"},
    {"server_id": 7, "software_id": 5, "software_name": "OpenSSH", "version_id": 10, "version": "9.8p1"},

    # srv-pay-proc-01: OpenSSL 1.1.1k, RabbitMQ 3.9.15, OpenSSH 8.9p1
    {"server_id": 8, "software_id": 6, "software_name": "OpenSSL", "version_id": 11, "version": "1.1.1k"},
    {"server_id": 8, "software_id": 9, "software_name": "RabbitMQ", "version_id": 15, "version": "3.9.15"},
    {"server_id": 8, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-pay-hsm-01: OpenSSL 3.0.12 (patched)
    {"server_id": 9, "software_id": 6, "software_name": "OpenSSL", "version_id": 12, "version": "3.0.12"},

    # srv-data-spark-01: Apache Spark 3.2.0, OpenSSH 8.9p1
    {"server_id": 10, "software_id": 10, "software_name": "Apache Spark", "version_id": 16, "version": "3.2.0"},
    {"server_id": 10, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-data-worker-01: Apache Spark 3.2.0, OpenSSH 8.9p1
    {"server_id": 11, "software_id": 10, "software_name": "Apache Spark", "version_id": 16, "version": "3.2.0"},
    {"server_id": 11, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-hr-app-01: Apache HTTP Server 2.4.49, OpenSSH 8.9p1
    {"server_id": 12, "software_id": 11, "software_name": "Apache HTTP Server", "version_id": 17, "version": "2.4.49"},
    {"server_id": 12, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-ops-ci-01: Jenkins 2.441, OpenSSH 8.9p1
    {"server_id": 13, "software_id": 12, "software_name": "Jenkins", "version_id": 18, "version": "2.441"},
    {"server_id": 13, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-sup-stage-01: Node.js 16.14.0, OpenSSH 8.9p1
    {"server_id": 14, "software_id": 13, "software_name": "Node.js", "version_id": 19, "version": "16.14.0"},
    {"server_id": 14, "software_id": 5, "software_name": "OpenSSH", "version_id": 9, "version": "8.9p1"},

    # srv-dr-core-01: PostgreSQL 14.8, OpenSSH 9.8p1
    {"server_id": 15, "software_id": 7, "software_name": "PostgreSQL", "version_id": 13, "version": "14.8"},
    {"server_id": 15, "software_id": 5, "software_name": "OpenSSH", "version_id": 10, "version": "9.8p1"}
]

# --------------------------------------------------------------------------
# 6. Generic Vulnerabilities Mock Data (KnowledgeBase definitions)
# --------------------------------------------------------------------------
# Exploit Availability Constants:
# 0 = None / Unproven
# 1 = Public Proof of Concept (PoC)
# 2 = Weaponized (Metasploit / Exploit Kit)
# 3 = Actively Exploited in the Wild (CISA KEV)

def compute_exploitability(exploit_status: int, exposure: str):
    exp = (exposure or "internal").lower()
    if exploit_status == 3: # Actively exploited in wild / CISA KEV
        if exp == "external":
            return 4, "Critical (Actively Exploited & Internet-Facing)"
        else:
            return 3, "High (Actively Exploited - Internal Lateral Threat)"
    elif exploit_status == 2: # Weaponized exploit
        if exp == "external":
            return 4, "Critical (Weaponized Exploit & Internet-Facing)"
        elif exp == "partner":
            return 3, "High (Weaponized Exploit & Partner Exposed)"
        else:
            return 3, "High (Weaponized Exploit - Internal Network)"
    elif exploit_status == 1: # PoC available
        if exp == "external":
            return 3, "High (Public PoC & Internet-Facing)"
        else:
            return 2, "Medium (Public PoC & Internal Network)"
    else: # None / unproven
        if exp == "external":
            return 2, "Medium (Exposed Surface, No Public Exploit)"
        else:
            return 1, "Low (Internal Network, No Public Exploit)"


VULNERABILITIES = [
    {
        "id": 1,
        "vuln_code": "QUALYS-377399",
        "cve": "CVE-2024-6387",
        "name": "OpenSSH Remote Code Execution (regreSSHion)",
        "severity": 5, # 5 = Urgent / Critical
        "cvss_score": 8.1,
        "exploit_status": 1,
        "exploit_status_label": "Public Proof of Concept (PoC)",
        "cisa_kev": 0,
        "exploit_frameworks": "Exploit-DB, GitHub PoC",
        "category": "Remote Code Execution",
        "is_patchable": 1,
        "published_date": "2024-07-01",
        "description": "A signal handler race condition in OpenSSH sshd allows unauthenticated remote attackers to execute arbitrary code with root privileges on glibc-based Linux systems.",
        "threat": "Attackers can exploit the race condition during asynchronous SIGALRM timeout handling to hijack execution flow and obtain an unauthenticated root shell.",
        "impact": "Complete compromise of the underlying host, root privilege escalation, credential theft, and unauthorized lateral movement across the internal subnet.",
        "solution": "Upgrade OpenSSH to version 9.8p1 or newer. Workaround: Set 'LoginGraceTime 0' in /etc/ssh/sshd_config (note: disables timeout and may expose to DoS)."
    },
    {
        "id": 2,
        "vuln_code": "QUALYS-376157",
        "cve": "CVE-2021-44228",
        "name": "Apache Log4j JNDI Remote Code Execution (Log4Shell)",
        "severity": 5,
        "cvss_score": 10.0,
        "exploit_status": 3,
        "exploit_status_label": "Actively Exploited in the Wild (CISA KEV)",
        "cisa_kev": 1,
        "exploit_frameworks": "Metasploit, Core Impact, Exploit-DB, CISA KEV",
        "category": "Remote Code Execution",
        "is_patchable": 1,
        "published_date": "2021-12-10",
        "description": "Apache Log4j2 versions 2.0-beta9 through 2.14.1 JNDI features used in configuration, log messages, and parameters do not protect against attacker-controlled LDAP and other JNDI related endpoints.",
        "threat": "An unauthenticated remote attacker can submit a crafted string containing '${jndi:ldap://...}' in HTTP headers, parameters, or forms, forcing the vulnerable server to load and execute malicious arbitrary Java byte code.",
        "impact": "Full takeover of the application server container, shell access, exfiltration of environment variables, secrets, and database credentials.",
        "solution": "Upgrade Log4j to 2.17.1 or higher. Immediate workaround: set system property 'log4j2.formatMsgNoLookups=true' or remove JndiLookup.class from log4j-core JAR."
    },
    {
        "id": 3,
        "vuln_code": "QUALYS-376527",
        "cve": "CVE-2022-22965",
        "name": "Spring Framework Remote Code Execution (Spring4Shell)",
        "severity": 5,
        "cvss_score": 9.8,
        "exploit_status": 2,
        "exploit_status_label": "Weaponized (Metasploit / Exploit Kit)",
        "cisa_kev": 1,
        "exploit_frameworks": "Metasploit, Exploit-DB, CISA KEV",
        "category": "Remote Code Execution",
        "is_patchable": 1,
        "published_date": "2022-03-31",
        "description": "A Spring MVC or Spring WebFlux application running on JDK 9+ may be vulnerable to remote code execution via data binding when packaged as a traditional WAR deployed to an Apache Tomcat servlet container.",
        "threat": "Attackers manipulate ClassLoader properties via request parameter binding to modify Tomcat AccessLogValve patterns, writing a web shell directly to disk.",
        "impact": "Persistent backdoor installation, remote arbitrary code execution, and data compromise.",
        "solution": "Upgrade Spring Framework to version 5.3.18 / 6.0 or higher. Upgrade Tomcat to latest maintenance release."
    },
    {
        "id": 4,
        "vuln_code": "QUALYS-377701",
        "cve": "CVE-2023-44487",
        "name": "HTTP/2 Rapid Reset Denial of Service",
        "severity": 4, # 4 = High
        "cvss_score": 7.5,
        "exploit_status": 3,
        "exploit_status_label": "Actively Exploited in the Wild (CISA KEV)",
        "cisa_kev": 1,
        "exploit_frameworks": "In The Wild DDoS scripts, CISA KEV",
        "category": "Denial of Service",
        "is_patchable": 1,
        "published_date": "2023-10-10",
        "description": "The HTTP/2 protocol allows a denial of service (server resource consumption) because request cancellation can reset many streams rapidly without the server being able to enforce rate limits.",
        "threat": "A single client can send high volumes of RST_STREAM frames immediately following HEADERS frames, exhausting server CPU and memory resources.",
        "impact": "Service degradation or complete unavailability for legitimate users across public web services.",
        "solution": "Apply vendor security updates to Nginx (1.25.3 / 1.24.1+), Apache HTTP Server, or cloud load balancers; configure HTTP/2 stream limiters."
    },
    {
        "id": 5,
        "vuln_code": "QUALYS-376911",
        "cve": "CVE-2022-3602",
        "name": "OpenSSL X.509 Email Address Buffer Overflow",
        "severity": 4,
        "cvss_score": 7.5,
        "exploit_status": 0,
        "exploit_status_label": "None / Unproven",
        "cisa_kev": 0,
        "exploit_frameworks": "None",
        "category": "Memory Corruption / RCE",
        "is_patchable": 1,
        "published_date": "2022-11-01",
        "description": "A 4-byte stack buffer overflow can occur in OpenSSL during X.509 certificate verification, specifically in name constraint checking of email addresses.",
        "threat": "Maliciously crafted TLS client certificates containing punycode email addresses can trigger stack buffer corruption during TLS handshake verification.",
        "impact": "Denial of service (crash) or potential arbitrary code execution under specific compiler stack layouts.",
        "solution": "Upgrade OpenSSL to version 3.0.7 or later (or 1.1.1s for 1.1.1 series)."
    },
    {
        "id": 6,
        "vuln_code": "QUALYS-377450",
        "cve": "CVE-2024-23897",
        "name": "Jenkins CLI Arbitrary File Read Vulnerability",
        "severity": 5,
        "cvss_score": 9.8,
        "exploit_status": 2,
        "exploit_status_label": "Weaponized (Metasploit / Exploit Kit)",
        "cisa_kev": 1,
        "exploit_frameworks": "Metasploit, Exploit-DB, CISA KEV",
        "category": "Information Disclosure / RCE",
        "is_patchable": 1,
        "published_date": "2024-01-24",
        "description": "Jenkins uses the args4j library to parse command arguments on the Jenkins controller. This parser features '@' character argument expansion which replaces '@' followed by a file path with file contents.",
        "threat": "Unauthenticated attackers with read access can read the first few lines of arbitrary files on the Jenkins controller filesystem, or full files with admin privileges, enabling cryptographic key extraction and full RCE.",
        "impact": "Extraction of credentials, encryption master keys, source code, and potential elevation to full controller remote execution.",
        "solution": "Upgrade Jenkins core to 2.442 or LTS 2.426.3. Immediate workaround: disable CLI access via script console."
    },
    {
        "id": 7,
        "vuln_code": "QUALYS-376689",
        "cve": "CVE-2022-33891",
        "name": "Apache Spark Command Injection via ACL",
        "severity": 4,
        "cvss_score": 8.8,
        "exploit_status": 1,
        "exploit_status_label": "Public Proof of Concept (PoC)",
        "cisa_kev": 0,
        "exploit_frameworks": "GitHub PoC, Nuclei",
        "category": "Command Injection",
        "is_patchable": 1,
        "published_date": "2022-07-18",
        "description": "Apache Spark UI enables ACLs via 'spark.acls.enable'. With an improper configuration, a bash command is executed through Unix shell for user authentication with arbitrarily supplied user input.",
        "threat": "Attackers can supply arbitrary shell commands within the '?doAs=' HTTP query parameter when accessing the Spark Web UI.",
        "impact": "Remote shell execution under the spark system user account on the master node.",
        "solution": "Upgrade Apache Spark to 3.2.2, 3.3.0, or newer."
    },
    {
        "id": 8,
        "vuln_code": "QUALYS-376044",
        "cve": "CVE-2021-41773",
        "name": "Apache HTTP Server Path Traversal & Remote Code Execution",
        "severity": 4,
        "cvss_score": 7.5,
        "exploit_status": 2,
        "exploit_status_label": "Weaponized (Metasploit / Exploit Kit)",
        "cisa_kev": 1,
        "exploit_frameworks": "Metasploit, Exploit-DB, CISA KEV",
        "category": "Path Traversal / RCE",
        "is_patchable": 1,
        "published_date": "2021-10-05",
        "description": "A flaw was found in a change made to path normalization in Apache HTTP Server 2.4.49. An attacker could use a path traversal attack to map URLs to files outside the directories configured by Alias-like directives.",
        "threat": "If files outside of document roots are not protected by 'require all denied' and mod_cgi is enabled, path traversal triggers arbitrary CGI script execution.",
        "impact": "Arbitrary file disclosure (e.g., /etc/passwd) and execution of system commands.",
        "solution": "Upgrade Apache HTTP Server to version 2.4.51 or higher."
    },
    {
        "id": 9,
        "vuln_code": "QUALYS-377120",
        "cve": "CVE-2023-30533",
        "name": "Node.js Prototype Pollution in Core Stream APIs",
        "severity": 3, # 3 = Medium
        "cvss_score": 6.5,
        "exploit_status": 0,
        "exploit_status_label": "None / Unproven",
        "cisa_kev": 0,
        "exploit_frameworks": "None",
        "category": "Prototype Pollution",
        "is_patchable": 1,
        "published_date": "2023-06-20",
        "description": "Node.js contains a prototype pollution vulnerability in stream processing when untrusted user input is passed without sanitization into internal object properties.",
        "threat": "Attackers can manipulate JavaScript Object prototypes leading to unexpected logic bypass or application crash.",
        "impact": "Service disruption and potential authentication bypass depending on application property lookups.",
        "solution": "Upgrade Node.js to 16.20.1, 18.16.1, or 20.3.1."
    }
]

# --------------------------------------------------------------------------
# 7. Vulnerability Instances / Findings Mock Data (Per-Asset detections)
# --------------------------------------------------------------------------
# Status constants:
# 1 = New, 2 = Active, 3 = Re-opened, 4 = Fixed, 5 = Ignored
FINDINGS = [
    {
        "id": 1,
        "vuln_id": 1,
        "vuln_code": "QUALYS-377399",
        "cve": "CVE-2024-6387",
        "server_id": 1,
        "hostname": "srv-bank-api-01.prod.internal",
        "ip": "10.10.10.11",
        "port": 22,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-07-02 04:12:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 124,
        "proof": "SSH banner reported: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.7. Vulnerable glibc-based OpenSSH sshd version detected without vendor patch for SIGALRM race condition.",
        "remediation_ticket": "INC-89021"
    },
    {
        "id": 2,
        "vuln_id": 1,
        "vuln_code": "QUALYS-377399",
        "cve": "CVE-2024-6387",
        "server_id": 2,
        "hostname": "srv-bank-api-02.prod.internal",
        "ip": "10.10.10.12",
        "port": 22,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-07-02 04:15:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 124,
        "proof": "SSH banner reported: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.7. System vulnerable to regreSSHion unauthenticated RCE.",
        "remediation_ticket": "INC-89022"
    },
    {
        "id": 3,
        "vuln_id": 3,
        "vuln_code": "QUALYS-376527",
        "cve": "CVE-2022-22965",
        "server_id": 1,
        "hostname": "srv-bank-api-01.prod.internal",
        "ip": "10.10.10.11",
        "port": 8080,
        "protocol": "tcp",
        "exposure": "partner",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-05-10 14:22:15",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 178,
        "proof": "Spring Framework 5.3.18 detected running on Apache Tomcat 9.0.58. HTTP request parameter binding exposes classLoader attributes to manipulation.",
        "remediation_ticket": "SEC-44102"
    },
    {
        "id": 4,
        "vuln_id": 3,
        "vuln_code": "QUALYS-376527",
        "cve": "CVE-2022-22965",
        "server_id": 2,
        "hostname": "srv-bank-api-02.prod.internal",
        "ip": "10.10.10.12",
        "port": 8080,
        "protocol": "tcp",
        "exposure": "partner",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-05-10 14:25:10",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 178,
        "proof": "Spring Framework 5.3.18 on Tomcat 9.0.58 detected. Verified data-binding ClassLoader access on /api/v1 endpoints.",
        "remediation_ticket": "SEC-44103"
    },
    {
        "id": 5,
        "vuln_id": 4,
        "vuln_code": "QUALYS-377701",
        "cve": "CVE-2023-44487",
        "server_id": 4,
        "hostname": "srv-ecom-web-01.prod.internal",
        "ip": "10.20.10.11",
        "port": 443,
        "protocol": "tcp",
        "exposure": "external",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2023-10-15 08:30:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 384,
        "proof": "Nginx/1.20.1 detected on TLS port 443 supporting HTTP/2 with rapid reset stream vulnerability unpatched.",
        "remediation_ticket": "SEC-55091"
    },
    {
        "id": 6,
        "vuln_id": 4,
        "vuln_code": "QUALYS-377701",
        "cve": "CVE-2023-44487",
        "server_id": 5,
        "hostname": "srv-ecom-web-02.prod.internal",
        "ip": "10.20.10.12",
        "port": 443,
        "protocol": "tcp",
        "exposure": "external",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2023-10-15 08:35:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 384,
        "proof": "Nginx/1.20.1 detected on TLS port 443. Target vulnerable to rapid RST_STREAM DDoS attack.",
        "remediation_ticket": "SEC-55092"
    },
    {
        "id": 7,
        "vuln_id": 2,
        "vuln_code": "QUALYS-376157",
        "cve": "CVE-2021-44228",
        "server_id": 6,
        "hostname": "srv-ecom-app-01.prod.internal",
        "ip": "10.20.10.21",
        "port": 8443,
        "protocol": "tcp",
        "exposure": "external",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-01-12 11:00:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 296,
        "proof": "Log4j core library version 2.14.1 found in /opt/ecom/app/lib/log4j-core-2.14.1.jar. JndiLookup class present in archive.",
        "remediation_ticket": "INC-77180"
    },
    {
        "id": 8,
        "vuln_id": 5,
        "vuln_code": "QUALYS-376911",
        "cve": "CVE-2022-3602",
        "server_id": 8,
        "hostname": "srv-pay-proc-01.pci.internal",
        "ip": "10.30.10.10",
        "port": 443,
        "protocol": "tcp",
        "exposure": "external",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2023-01-05 09:14:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 668,
        "proof": "OpenSSL 1.1.1k FIPS 25 Mar 2021 detected. Subject Alternative Name punycode parser contains vulnerable stack buffer overflow.",
        "remediation_ticket": "PCI-VULN-09"
    },
    {
        "id": 9,
        "vuln_id": 7,
        "vuln_code": "QUALYS-376689",
        "cve": "CVE-2022-33891",
        "server_id": 10,
        "hostname": "srv-data-spark-01.prod.internal",
        "ip": "10.50.10.31",
        "port": 8080,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 2, # Active
        "status_label": "Active",
        "first_found": "2024-03-20 16:45:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 228,
        "proof": "Apache Spark Web UI version 3.2.0 responding on port 8080. Endpoint vulnerable to command injection via 'doAs' query parameter.",
        "remediation_ticket": "DATA-SEC-102"
    },
    {
        "id": 10,
        "vuln_id": 8,
        "vuln_code": "QUALYS-376044",
        "cve": "CVE-2021-41773",
        "server_id": 12,
        "hostname": "srv-hr-app-01.corp.internal",
        "ip": "10.40.10.15",
        "port": 80,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 4, # Fixed
        "status_label": "Fixed",
        "first_found": "2023-06-01 10:00:00",
        "last_found": "2023-06-15 14:00:00",
        "times_found": 15,
        "proof": "Historical detection: Apache/2.4.49 path traversal test returned /etc/passwd contents. Host subsequently patched to 2.4.54.",
        "remediation_ticket": "HR-CORP-401"
    },
    {
        "id": 11,
        "vuln_id": 6,
        "vuln_code": "QUALYS-377450",
        "cve": "CVE-2024-23897",
        "server_id": 13,
        "hostname": "srv-ops-ci-01.corp.internal",
        "ip": "10.60.10.50",
        "port": 8080,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 1, # New
        "status_label": "New",
        "first_found": "2024-11-01 18:30:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 3,
        "proof": "Jenkins 2.441 CLI interface exposed on port 8080. Command argument parser supports '@' arbitrary file expansion without authentication.",
        "remediation_ticket": "OPS-SECTOKEN-33"
    },
    {
        "id": 12,
        "vuln_id": 9,
        "vuln_code": "QUALYS-377120",
        "cve": "CVE-2023-30533",
        "server_id": 14,
        "hostname": "srv-sup-stage-01.stg.internal",
        "ip": "10.70.10.88",
        "port": 3000,
        "protocol": "tcp",
        "exposure": "internal",
        "status": 5, # Ignored (staging accepted risk)
        "status_label": "Ignored",
        "first_found": "2024-04-10 11:20:00",
        "last_found": "2024-11-03 02:00:00",
        "times_found": 208,
        "proof": "Node.js v16.14.0 stream prototype pollution vulnerability detected in staging environment. Risk accepted by QA lead for test lab.",
        "remediation_ticket": "RISK-ACCEPT-012"
    }
]

# Calculate exploitability for all findings
_vulns_map = {v["id"]: v for v in VULNERABILITIES}
for f in FINDINGS:
    v = _vulns_map[f["vuln_id"]]
    f["exploit_status"] = v["exploit_status"]
    f["cisa_kev"] = v["cisa_kev"]
    level, label = compute_exploitability(v["exploit_status"], f["exposure"])
    f["exploitability_level"] = level
    f["exploitability_label"] = label


def write_csv(filename, fieldnames, data):
    path = os.path.join(CSV_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated CSV: {path} ({len(data)} rows)")


def write_json(filename, data):
    path = os.path.join(JSON_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated JSON: {path}")


def generate_unified_graph():
    """Generates the hierarchical graph: Application -> Servers -> Installed Softwares -> Vulnerabilities"""
    # Index servers by ID
    servers_by_id = {s["id"]: dict(s) for s in SERVERS}
    for s in servers_by_id.values():
        s["installed_software"] = []
        s["vulnerability_findings"] = []

    # Map installed software to servers
    for sw in SERVER_SOFTWARE:
        sid = sw["server_id"]
        if sid in servers_by_id:
            servers_by_id[sid]["installed_software"].append({
                "software_id": sw["software_id"],
                "software_name": sw["software_name"],
                "version_id": sw["version_id"],
                "version": sw["version"]
            })

    # Index vulnerabilities by ID
    vulns_by_id = {v["id"]: dict(v) for v in VULNERABILITIES}

    # Map findings to servers
    for find in FINDINGS:
        sid = find["server_id"]
        if sid in servers_by_id:
            vuln_info = vulns_by_id.get(find["vuln_id"], {})
            finding_copy = dict(find)
            finding_copy["vulnerability"] = vuln_info
            servers_by_id[sid]["vulnerability_findings"].append(finding_copy)

    # Build applications with nested servers
    apps_graph = []
    for app in APPLICATIONS:
        app_copy = dict(app)
        app_copy["servers"] = []
        # Find mapped servers
        for link in APPLICATION_SERVERS:
            if link["application_id"] == app["id"]:
                server_id = link["server_id"]
                server_obj = dict(servers_by_id[server_id])
                server_obj["application_role"] = link["role"]
                app_copy["servers"].append(server_obj)
        
        # Summary counts
        total_findings = sum(len(srv["vulnerability_findings"]) for srv in app_copy["servers"])
        critical_findings = sum(
            1 for srv in app_copy["servers"]
            for f in srv["vulnerability_findings"]
            if f.get("vulnerability", {}).get("severity") == 5 and f["status"] in (1, 2, 3)
        )
        app_copy["total_findings_count"] = total_findings
        app_copy["open_critical_findings_count"] = critical_findings
        apps_graph.append(app_copy)

    return apps_graph


def generate_scanner_export_csv():
    """Generates a flat scanner export CSV (Qualys/Nessus style) that can be imported directly into GLPI or security tools"""
    rows = []
    vulns_by_id = {v["id"]: v for v in VULNERABILITIES}
    
    for f in FINDINGS:
        v = vulns_by_id[f["vuln_id"]]
        rows.append({
            "qid": v["vuln_code"],
            "title": v["name"],
            "cve": v["cve"],
            "severity": v["severity"],
            "cvss": v["cvss_score"],
            "exploit_status": v["exploit_status"],
            "exploit_status_label": v["exploit_status_label"],
            "cisa_kev": v["cisa_kev"],
            "exploit_frameworks": v["exploit_frameworks"],
            "exposure": f["exposure"],
            "exploitability_level": f["exploitability_level"],
            "exploitability_label": f["exploitability_label"],
            "category": v["category"],
            "threat": v["threat"],
            "impact": v["impact"],
            "solution": v["solution"],
            "hostname": f["hostname"],
            "ip": f["ip"],
            "port": f["port"],
            "protocol": f["protocol"],
            "status": f["status_label"],
            "results": f["proof"],
            "first_found": f["first_found"],
            "last_found": f["last_found"],
            "remediation_ticket": f["remediation_ticket"]
        })
    return rows


def generate_sql_seed():
    """Generates direct SQL seed statements for GLPI database schema"""
    sql_lines = [
        "-- GLPI & Vulnerability Management Plugin Mock Data Seed",
        "-- Auto-generated by generate_mock_data.py",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
        "-- 1. Business Applications (glpi_plugin_vulnerabilitymanagement_applications)",
        "DELETE FROM `glpi_plugin_vulnerabilitymanagement_applications` WHERE `id` BETWEEN 1 AND 50;"
    ]

    for app in APPLICATIONS:
        desc_escaped = app["description"].replace("'", "''")
        unit_escaped = app["business_unit"].replace("'", "''")
        sql_lines.append(
            f"INSERT INTO `glpi_plugin_vulnerabilitymanagement_applications` "
            f"(`id`, `entities_id`, `is_recursive`, `name`, `app_code`, `criticality`, `environment`, `exposure`, `business_unit`, `description`, `is_deleted`, `date_creation`, `date_mod`) "
            f"VALUES ({app['id']}, 0, 1, '{app['name']}', '{app['app_code']}', {app['criticality']}, '{app['environment']}', '{app['exposure']}', '{unit_escaped}', '{desc_escaped}', 0, NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("-- 2. Servers / Infrastructure Assets (glpi_computers)")
    sql_lines.append("DELETE FROM `glpi_computers` WHERE `id` BETWEEN 101 AND 150;")
    for srv in SERVERS:
        cid = 100 + srv["id"]
        comm = f"{srv['primary_role']} | {srv['datacenter']} {srv['rack']} | IP: {srv['ip']}".replace("'", "''")
        sql_lines.append(
            f"INSERT INTO `glpi_computers` (`id`, `entities_id`, `name`, `comment`, `is_deleted`, `date_creation`, `date_mod`) "
            f"VALUES ({cid}, 0, '{srv['hostname']}', '{comm}', 0, NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("-- 3. Software Components (glpi_softwares)")
    sql_lines.append("DELETE FROM `glpi_softwares` WHERE `id` BETWEEN 101 AND 150;")
    seen_soft = set()
    for sw in SOFTWARE_COMPONENTS:
        sid = 100 + sw["software_id"]
        if sid not in seen_soft:
            seen_soft.add(sid)
            sql_lines.append(
                f"INSERT INTO `glpi_softwares` (`id`, `entities_id`, `name`, `comment`, `is_deleted`, `date_creation`, `date_mod`) "
                f"VALUES ({sid}, 0, '{sw['name']}', '{sw['category']} - Vendor: {sw['vendor']}', 0, NOW(), NOW());"
            )

    sql_lines.append("")
    sql_lines.append("-- 4. Software Versions (glpi_softwareversions)")
    sql_lines.append("DELETE FROM `glpi_softwareversions` WHERE `id` BETWEEN 101 AND 150;")
    for sw in SOFTWARE_COMPONENTS:
        vid = 100 + sw["version_id"]
        sid = 100 + sw["software_id"]
        sql_lines.append(
            f"INSERT INTO `glpi_softwareversions` (`id`, `entities_id`, `softwares_id`, `name`, `date_creation`, `date_mod`) "
            f"VALUES ({vid}, 0, {sid}, '{sw['version']}', NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("-- 5. Installed Software on Servers (glpi_items_softwareversions)")
    sql_lines.append("DELETE FROM `glpi_items_softwareversions` WHERE `items_id` BETWEEN 101 AND 150 AND `itemtype` = 'Computer';")
    for sw_inst in SERVER_SOFTWARE:
        cid = 100 + sw_inst["server_id"]
        vid = 100 + sw_inst["version_id"]
        sql_lines.append(
            f"INSERT INTO `glpi_items_softwareversions` (`entities_id`, `items_id`, `itemtype`, `softwareversions_id`, `is_deleted`, `date_install`) "
            f"VALUES (0, {cid}, 'Computer', {vid}, 0, CURDATE());"
        )

    sql_lines.append("")
    sql_lines.append("-- 6. Application <-> Server Links (glpi_plugin_vulnerabilitymanagement_applicationassets)")
    sql_lines.append("DELETE FROM `glpi_plugin_vulnerabilitymanagement_applicationassets` WHERE `plugin_vulnerabilitymanagement_applications_id` BETWEEN 1 AND 50;")
    for link in APPLICATION_SERVERS:
        cid = 100 + link["server_id"]
        sql_lines.append(
            f"INSERT INTO `glpi_plugin_vulnerabilitymanagement_applicationassets` "
            f"(`plugin_vulnerabilitymanagement_applications_id`, `itemtype`, `items_id`, `role`, `date_creation`, `date_mod`) "
            f"VALUES ({link['application_id']}, 'Computer', {cid}, '{link['role']}', NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("-- 7. Generic Vulnerabilities (glpi_plugin_vulnerabilitymanagement_vulnerabilities)")
    sql_lines.append("DELETE FROM `glpi_plugin_vulnerabilitymanagement_vulnerabilities` WHERE `id` BETWEEN 1 AND 50;")
    for v in VULNERABILITIES:
        d = v["description"].replace("'", "''")
        t = v["threat"].replace("'", "''")
        imp = v["impact"].replace("'", "''")
        sol = v["solution"].replace("'", "''")
        fw = v["exploit_frameworks"].replace("'", "''")
        sql_lines.append(
            f"INSERT INTO `glpi_plugin_vulnerabilitymanagement_vulnerabilities` "
            f"(`id`, `entities_id`, `is_recursive`, `name`, `vuln_code`, `cve`, `severity`, `cvss_score`, `exploit_status`, `cisa_kev`, `exploit_frameworks`, `category`, `is_patchable`, `published_date`, `description`, `threat`, `impact`, `solution`, `is_deleted`, `date_creation`, `date_mod`) "
            f"VALUES ({v['id']}, 0, 1, '{v['name']}', '{v['vuln_code']}', '{v['cve']}', {v['severity']}, {v['cvss_score']}, {v['exploit_status']}, {v['cisa_kev']}, '{fw}', '{v['category']}', {v['is_patchable']}, '{v['published_date']}', '{d}', '{t}', '{imp}', '{sol}', 0, NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("-- 8. Vulnerability Instances / Findings (glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances)")
    sql_lines.append("DELETE FROM `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances` WHERE `id` BETWEEN 1 AND 50;")
    for f in FINDINGS:
        cid = 100 + f["server_id"]
        proof_escaped = f["proof"].replace("'", "''")
        sql_lines.append(
            f"INSERT INTO `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances` "
            f"(`id`, `entities_id`, `is_recursive`, `plugin_vulnerabilitymanagement_vulnerabilities_id`, `itemtype`, `items_id`, `status`, `port`, `protocol`, `exposure`, `ip`, `first_found`, `last_found`, `times_found`, `proof`, `tickets_id`, `is_deleted`, `date_creation`, `date_mod`) "
            f"VALUES ({f['id']}, 0, 1, {f['vuln_id']}, 'Computer', {cid}, {f['status']}, {f['port']}, '{f['protocol']}', '{f['exposure']}', '{f['ip']}', '{f['first_found']}', '{f['last_found']}', {f['times_found']}, '{proof_escaped}', 0, 0, NOW(), NOW());"
        )

    sql_lines.append("")
    sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;")
    return "\n".join(sql_lines)


def main():
    print("=" * 60)
    print("Generating Mock Data for CMDB & Vulnerability Management...")
    print("=" * 60)

    # 1. Write CSV files
    write_csv(
        "applications.csv",
        ["id", "app_code", "name", "criticality", "criticality_label", "environment", "exposure", "business_unit", "business_owner", "tech_lead", "team", "description"],
        APPLICATIONS
    )
    write_csv(
        "servers.csv",
        ["id", "hostname", "ip", "os", "os_version", "environment", "datacenter", "rack", "cpu_cores", "ram_gb", "status", "primary_role"],
        SERVERS
    )
    write_csv(
        "software_components.csv",
        ["software_id", "name", "category", "vendor", "version_id", "version", "is_vulnerable", "cve_ref"],
        SOFTWARE_COMPONENTS
    )
    write_csv(
        "application_servers.csv",
        ["application_id", "server_id", "role"],
        APPLICATION_SERVERS
    )
    write_csv(
        "server_software.csv",
        ["server_id", "software_id", "software_name", "version_id", "version"],
        SERVER_SOFTWARE
    )
    write_csv(
        "vulnerabilities.csv",
        ["id", "vuln_code", "cve", "name", "severity", "cvss_score", "exploit_status", "exploit_status_label", "cisa_kev", "exploit_frameworks", "category", "is_patchable", "published_date", "description", "threat", "impact", "solution"],
        VULNERABILITIES
    )
    write_csv(
        "vulnerability_findings.csv",
        ["id", "vuln_id", "vuln_code", "cve", "server_id", "hostname", "ip", "port", "protocol", "exposure", "exploit_status", "cisa_kev", "exploitability_level", "exploitability_label", "status", "status_label", "first_found", "last_found", "times_found", "proof", "remediation_ticket"],
        FINDINGS
    )

    # Scanner export flat CSV
    scanner_rows = generate_scanner_export_csv()
    write_csv(
        "vulnerability_scan_flat_export.csv",
        ["qid", "title", "cve", "severity", "cvss", "exploit_status", "exploit_status_label", "cisa_kev", "exploit_frameworks", "exposure", "exploitability_level", "exploitability_label", "category", "threat", "impact", "solution", "hostname", "ip", "port", "protocol", "status", "results", "first_found", "last_found", "remediation_ticket"],
        scanner_rows
    )

    # 2. Write JSON files
    write_json("applications.json", APPLICATIONS)
    write_json("servers.json", SERVERS)
    write_json("software_components.json", SOFTWARE_COMPONENTS)
    write_json("application_servers.json", APPLICATION_SERVERS)
    write_json("server_software.json", SERVER_SOFTWARE)
    write_json("vulnerabilities.json", VULNERABILITIES)
    write_json("vulnerability_findings.json", FINDINGS)
    write_json("vulnerability_scan_flat_export.json", scanner_rows)

    # Unified complete relational graph JSON
    graph = generate_unified_graph()
    write_json("unified_cmdb_risk_graph.json", graph)

    # 3. Write SQL Seed script
    sql_content = generate_sql_seed()
    sql_path = os.path.join(SQL_DIR, "seed_glpi_mock_data.sql")
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write(sql_content)
    print(f"Generated SQL: {sql_path}")

    print("=" * 60)
    print("Mock data generation successfully completed!")
    print("=" * 60)
    print("=" * 60)


if __name__ == "__main__":
    main()

