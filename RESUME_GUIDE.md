# GLPI Vulnerability Management - Project Handover & Instance Resume Guide

This document summarizes all architectural changes, enhancements, database migrations, dashboard configurations, and steps required to resume or reproduce this setup on another GLPI instance.

---

## 1. Project Architecture Overview

The system consists of a Dockerized **GLPI 11.x/12.x** stack with a custom native plugin located in `plugins/vulnerabilitymanagement/`:

```text
glpi/
├── compose.yaml                               # Docker Compose configuration (glpi-app + glpi-db)
├── .env                                       # Database passwords and environment variables
├── RESUME_GUIDE.md                            # This handover & deployment guide
├── mock_data/
│   ├── README.md                              # Mock data generation & import documentation
│   ├── scripts/generate_mock_data.py          # Python mock data generator (assets, vulns, instances)
│   ├── sql/seed_glpi_mock_data.sql            # Seed SQL containing realistic enterprise vulnerability data
│   └── csv/defender/                          # Ingestible Defender VM CSV exports
└── plugins/vulnerabilitymanagement/
    ├── README.md                              # Plugin documentation & packaging instructions
    ├── setup.php                              # Hook registrations, menu redefining, filter hooks
    ├── hook.php                               # Idempotent DB schema migrations, central dashboard setup
    ├── front/
    │   └── import.php                         # CSV Import controller for Microsoft Defender extracts
    ├── src/
    │   ├── Application.php                    # Business Application object (Tier 1-4, Owner, Code)
    │   ├── ApplicationAsset.php               # Links Applications <-> Computers & Software with architectural role
    │   ├── ApplicationFilter.php              # Native Dashboard filter: Business Application
    │   ├── CsvImport.php                      # CSV ingestion and finding reconciliation engine
    │   ├── DashboardProvider.php              # KPI big numbers, severity donuts, bar charts, trend graphs
    │   ├── ServerFilter.php                   # Native Dashboard filter: Server / Host
    │   ├── Snapshot.php                       # Telemetry snapshot tracking for status & severity evolution
    │   ├── Vulnerability.php                  # KnowledgeBase definitions (CVE, CVSS, QID, Severity 1-5)
    │   ├── VulnerabilityFilter.php            # Native Dashboard filter: Vulnerability
    │   ├── VulnerabilityInstance.php          # Per-asset detection findings (Softwares ID, Status, Port)
    │   └── VulnerabilitySeverityFilter.php    # Native Dashboard filter: Vulnerability Criticality
    └── templates/
        ├── application.html.twig              # Business Application form template
        ├── application_asset.html.twig        # Application <-> Asset link template
        ├── vulnerability.html.twig            # Vulnerability KnowledgeBase template
        └── vulnerability_instance.html.twig   # Vulnerability Instance finding template
```

---

## 2. Key Components & What Was Done

### A. Vulnerability & Software Precise Mapping (`softwares_id`)
- **Problem solved:** Previously, vulnerability instances attached to a host showed all software installed on that host (e.g. OpenSSH appeared alongside Jenkins for `CVE-2024-23897`).
- **Implementation:**
  - Added indexed `softwares_id` column to `glpi_plugin_vulnerabilitymanagement_vulnerabilities` and `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances`.
  - Added idempotent migrations in [`plugins/vulnerabilitymanagement/hook.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/hook.php).
  - Search Option 17 in [`src/VulnerabilityInstance.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/VulnerabilityInstance.php) now joins directly on `softwares_id`.
  - Updated Defender CSV import engine ([`front/import.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/front/import.php)) to match and assign the exact software item automatically.
  - Updated seed data ([`mock_data/sql/seed_glpi_mock_data.sql`](file:///home/romain/glpi/mock_data/sql/seed_glpi_mock_data.sql)) and generator script.

### B. Navigation & Security Profile Streamlining
- **Navigation Menus:** Filtered out ~25 irrelevant GLPI asset/management types via `Hooks::REDEFINE_MENUS`. Only relevant IT & VM objects appear in the navbar:
  - *Assets:* Computers, Software, Applications (Business View), Vulnerabilities (KnowledgeBase), Vulnerability Instances, Import CSV.
  - *Management:* Applications (Business View), Vulnerabilities (KnowledgeBase), Vulnerability Instances, Import CSV.
- **Dedicated Profile:** Configured `Security analyst` (Profile ID 9) with customized permissions and assigned user `glpi` (User ID 2) to it in `glpi_profiles_users`.

### C. Native Central Dashboard Cards
Registered 8 custom cards in [`src/DashboardProvider.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/DashboardProvider.php) displayed on GLPI's Central Dashboard:
1. `vm_bn_applications`: Number of Business Applications (Big Number).
2. `vm_bn_vulnerabilities`: Vulnerabilities KnowledgeBase count (Big Number).
3. `vm_bn_open_findings`: Open Vulnerability Findings count (Big Number).
4. `vm_apps_by_criticality`: Business Applications by Criticality (Donut / Pie).
5. `vm_vulns_by_severity`: Vulnerabilities by Severity 1–5 (Donut / Pie).
6. `vm_open_findings_by_app`: Open Findings by Business Application (Horizontal Bar Chart).
7. `vm_trend_status_evolution`: 26-week status trend: Active, Re-opened, New vs Fixed.
8. `vm_trend_severity_evolution`: 26-week severity breakdown trend.

### D. Multi-Dimensional Interactive Dashboard Filters
Created 4 native GLPI filters extending `Glpi\Dashboard\Filters\AbstractFilter` registered in `$PLUGIN_HOOKS[Hooks::DASHBOARD_FILTERS]`:
1. **Business Application Filter ([`src/ApplicationFilter.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/ApplicationFilter.php)):**
   - Filter ID: `business_application`.
   - Single app selection zooms the horizontal bar chart into the vulnerabilities affecting that specific app.
2. **Vulnerability Filter ([`src/VulnerabilityFilter.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/VulnerabilityFilter.php)):**
   - Filter ID: `vulnerability`.
   - Filters the dashboard to a specific CVE/vulnerability, showing affected applications in the bar chart.
3. **Vulnerability Criticality Filter ([`src/VulnerabilitySeverityFilter.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/VulnerabilitySeverityFilter.php)):**
   - Filter ID: `vulnerability_severity`.
   - Dropdown of severity tiers (5 - Urgent, 4 - Critical, 3 - Serious, 2 - Medium, 1 - Minimal).
4. **Server / Host Filter ([`src/ServerFilter.php`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/src/ServerFilter.php)):**
   - Filter ID: `server`.
   - Filters the dashboard to findings and applications running on a specific host.
- **Combined Filtering:** All 4 filters can be applied simultaneously (e.g. *Server 101 + Severity 5*).
- **Pre-Configured Toolbar:** Pre-seeded in `glpi_dashboards_filters` for dashboard `1` (Central) so all 4 filters are immediately visible on initial page load.

---

## 3. How to Resume / Deploy in Another Instance

Follow these steps to restore or deploy this entire setup in a new environment or container:

### Step 1: Start the Docker Stack
```bash
# Clone/copy the project directory
git clone <repo-url> glpi
cd glpi

# Start MariaDB and GLPI containers
docker compose up -d
```

### Step 2: Sync the Plugin Code into the GLPI Container
GLPI plugins are located in `/var/glpi/marketplace/` (or `/var/www/glpi/plugins/`). Sync the workspace plugin code:
```bash
tar -czf - -C plugins vulnerabilitymanagement | docker exec -i -u www-data glpi-app tar -xzf - -C /var/glpi/marketplace/
```

### Step 3: Install / Enable the Plugin via GLPI CLI
```bash
# Install and enable the plugin
docker exec -u www-data glpi-app /var/www/glpi/bin/console plugin:install vulnerabilitymanagement -e
docker exec -u www-data glpi-app /var/www/glpi/bin/console plugin:activate vulnerabilitymanagement
```

### Step 4: Load Mock Data (If starting on a fresh database)
To seed the database with realistic business applications, assets, and vulnerability instances:
```bash
docker exec -i glpi-db mariadb -u glpi -pglpi_secret_password_2026 glpi < mock_data/sql/seed_glpi_mock_data.sql
```

### Step 5: Configure Pre-Seeded Dashboard Filters
Ensure the 4 filter controls appear on the Central Dashboard:
```bash
docker exec -i glpi-db mariadb -u glpi -pglpi_secret_password_2026 glpi -e "
REPLACE INTO glpi_dashboards_filters (dashboards_dashboards_id, users_id, filter) 
VALUES 
  (1, 0, '{\"business_application\":\"\",\"vulnerability\":\"\",\"vulnerability_severity\":\"\",\"server\":\"\"}'),
  (1, 2, '{\"business_application\":\"\",\"vulnerability\":\"\",\"vulnerability_severity\":\"\",\"server\":\"\"}'),
  (1, 7, '{\"business_application\":\"\",\"vulnerability\":\"\",\"vulnerability_severity\":\"\",\"server\":\"\"}');
"
```

### Step 6: Clear Cache & Restart
```bash
docker exec -u www-data glpi-app /var/www/glpi/bin/console cache:clear
docker compose restart
```

---

## 4. Key Verification Checks

After resuming on a new instance:

1. **Web Access:** Open `http://localhost:8080/` and log in (Credentials: `glpi` / `glpi` or `secu` / `secu`).
2. **Central Dashboard:**
   - Check that the 4 filter dropdowns are present at the top: `Business Application`, `Vulnerability`, `Vulnerability Criticality`, and `Server / Host`.
   - Verify that selecting an application (e.g. `DevOps CI/CD Automation Platform`) updates the bar chart to show its findings (*Jenkins CLI Arbitrary File Read*).
   - Verify that selecting `5 - Urgent` narrows the findings count down to 6 and shows only applications with urgent vulnerabilities.
3. **Software Association Check:**
   - Navigate to **Assets > Vulnerability Instances**.
   - Inspect Finding #11: verify that its Software column shows strictly **Jenkins**, and **OpenSSH** is not associated with this CVE.
4. **CLI Smoke Test:**
   ```bash
   docker exec -u www-data glpi-app php -r '
   require_once "/var/www/glpi/vendor/autoload.php";
   $kernel = new \Glpi\Kernel\Kernel();
   $kernel->boot();
   (new \Plugin())->init();
   print_r(\Glpi\Dashboard\Filter::getFilterChoices());
   '
   ```
   Should list `business_application`, `vulnerability`, `vulnerability_severity`, and `server`.

---

## 5. Development Notes & Helpful Commands

- **Sync local plugin edits into container:**
  ```bash
  tar -czf - -C plugins vulnerabilitymanagement | docker exec -i -u www-data glpi-app tar -xzf - -C /var/glpi/marketplace/ && docker exec -u www-data glpi-app /var/www/glpi/bin/console cache:clear
  ```
- **Direct Database Access:**
  ```bash
  docker exec -it glpi-db mariadb -u glpi -pglpi_secret_password_2026 glpi
  ```
- **Package plugin for standalone deployment:**
  ```bash
  tar -czvf vulnerabilitymanagement-1.0.0.tar.gz -C plugins vulnerabilitymanagement
  ```
