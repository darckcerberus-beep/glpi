# GLPI Deployment (Docker Compose)

This directory contains the Docker configuration for **GLPI 12.0.1** and **MariaDB 11.4**, along with the custom **Vulnerability Management** plugin.

> [!TIP]
> See [**RESUME_GUIDE.md**](file:///home/romain/glpi/RESUME_GUIDE.md) for a summary of all recent modifications, architectural changes, database updates, and instructions on how to resume this project on another instance.

---

## 🌐 Accessing GLPI

- **URL:** [http://localhost:8080](http://localhost:8080)
- **Status:** Running & Database schema initialized

### Default Accounts

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Administrator** | `glpi` | `glpi` | Full admin privileges (change immediately) |
| **Technician** | `tech` | `tech` | Technician access |
| **Normal User** | `normal` | `normal` | Standard user access |
| **Read-Only / Post-only** | `post-only` | `postonly` | Ticket submission only |

> [!WARNING]
> For security reasons, please log in and change the default passwords for these accounts as soon as possible via **Administration > Users**.

---

## 🛠 Management Commands

From this directory (`/home/romain/glpi`):

- **Start services:**
  ```bash
  docker compose up -d
  ```

- **Stop services:**
  ```bash
  docker compose stop
  ```

- **View logs:**
  ```bash
  docker compose logs -f glpi
  ```

- **Run GLPI Console commands:**
  ```bash
  docker compose exec glpi /var/www/glpi/bin/console <command>
  ```

- **Database Backup:**
  ```bash
  docker compose exec db mariadb-dump -u glpi -pglpi_secret_password_2026 glpi > backup_$(date +%Y%m%d).sql
  ```

- **Deploy / Update Vulnerability Management Plugin:**
  ```bash
  tar -czf - -C plugins vulnerabilitymanagement | docker exec -i -u www-data glpi-app tar -xzf - -C /var/glpi/marketplace/
  docker compose exec -u www-data glpi /var/www/glpi/bin/console plugin:install vulnerabilitymanagement --no-interaction
  docker compose exec -u www-data glpi /var/www/glpi/bin/console cache:clear
  ```

- **Seed Mock CMDB & Vulnerability Dataset:**
  ```bash
  docker compose exec -T db mariadb -u glpi -pglpi_secret_password_2026 glpi < mock_data/sql/seed_glpi_mock_data.sql
  ```

---

## 📁 File Structure

- [`docker-compose.yml`](file:///home/romain/glpi/docker-compose.yml): Service specifications for GLPI and MariaDB.
- [`.env`](file:///home/romain/glpi/.env): Environment variables and credentials (ignored by git).
- [`plugins/vulnerabilitymanagement/`](file:///home/romain/glpi/plugins/vulnerabilitymanagement/README.md): Business-aware Vulnerability Management plugin (`Application`, `ApplicationAsset`, `Vulnerability`, `VulnerabilityInstance`, `DashboardProvider`, and Web UI `CsvImport` at **Management > Import CSV Data**).
- [`mock_data/`](file:///home/romain/glpi/mock_data/README.md): Enterprise CMDB & Vulnerability Management mock dataset (`csv/`, `json/`, `sql/seed_glpi_mock_data.sql`, and `scripts/`).

---

## 📝 Recent Modifications (Post-`29eae5b` Update & Asset Scope Restriction)

The following changes were applied to integrate the `mock_data` commit (`29eae5b`), fix GLPI 12 runtime compatibility issues, and restrict visible GLPI assets exclusively to **Applications**, **Computers / Servers**, **Software**, and **Vulnerabilities**:

### 1. GLPI 12 Compatibility & Bug Fixes
- **`plugins/vulnerabilitymanagement/src/CsvImport.php` (`CsvImport::getSearchURL()`):**
  - Replaced the call to `Plugin::getWebDir('vulnerabilitymanagement')` (removed in GLPI 12, which caused a fatal error when rendering the navigation menu) with `$CFG_GLPI['root_doc'] . '/plugins/vulnerabilitymanagement/front/import.php'`.
- **`plugins/vulnerabilitymanagement/front/import.php`:**
  - Guarded `include('../../../inc/includes.php')` with `if (!defined('GLPI_ROOT') && file_exists(__DIR__ . '/../../../inc/includes.php'))`. In GLPI 12 Docker deployments where the plugin resides in `/var/glpi/marketplace/vulnerabilitymanagement/`, `LegacyFileLoadController` already boots the kernel and `../../../inc/includes.php` does not exist under `/var/glpi/`.
  - Fixed the `glpi_items_softwareversions` insert payload during `server_software` CSV import to use `'date_install' => date('Y-m-d')` instead of non-existent `'date_creation'` / `'date_mod'` columns.
  - Enabled the `scan_flat` handler to also process standalone `vulnerabilities` CSV files (`$detected_format === 'scan_flat' || $detected_format === 'vulnerabilities'`).
- **`plugins/vulnerabilitymanagement/src/Vulnerability.php` (`Vulnerability::rawSearchOptions()`):**
  - Changed the search option IDs for `exploit_status`, `cisa_kev`, and `exploit_frameworks` from `'15'`, `'16'`, `'17'` to `'18'`, `'19'`, `'20'` so they do not collide with existing search option IDs `'15'` (`Application Environment`), `'16'` (`Application Exposure`), and `'17'` (`Business Unit`).
- **`plugins/vulnerabilitymanagement/hook.php` (`plugin_vulnerabilitymanagement_install()`):**
  - Added `$DB->fieldExists(...)` schema migration checks (`ALTER TABLE`) so existing installations automatically add `exploit_status`, `cisa_kev`, and `exploit_frameworks` to `glpi_plugin_vulnerabilitymanagement_vulnerabilities` and `exposure` to `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances`.

### 2. Asset Scope Restriction (Apps, Computers/Servers, Software & Vulnerabilities Only)
- **Navigation Menu Filtering (`plugins/vulnerabilitymanagement/setup.php` & `hook.php`):**
  - Set `$CFG_GLPI['asset_types'] = ['Computer', 'Software']` and `$CFG_GLPI['devices_in_menu'] = []`.
  - Registered `Hooks::REDEFINE_MENUS` (`plugin_vulnerabilitymanagement_redefine_menus()`) and `Hooks::MENU_TOADD` so:
    - **Assets Menu** displays only: `Computer` (*Computers*), `Software` (*Software*), `Application` (*Applications (Business View)*), `Vulnerability` (*Vulnerabilities (KnowledgeBase)*), `VulnerabilityInstance` (*Vulnerability Instances*), and `CsvImport` (*Import CSV Data*). All other GLPI asset types (`Monitor`, `NetworkEquipment`, `Peripheral`, `Printer`, `CartridgeItem`, `ConsumableItem`, `Phone`, `Rack`, `Enclosure`, `PDU`, `PassiveDCEquipment`, `Unmanaged`, `Cable`, `Simcard`, `AllAssets`) are hidden.
    - **Management Menu** displays only: `Application`, `Vulnerability`, `VulnerabilityInstance`, and `CsvImport` (hiding `SoftwareLicense`, `Budget`, `Supplier`, `Contact`, `Contract`, `Document`, `Line`, `Certificate`, `Datacenter`, `Cluster`, `Domain`, `Appliance`, `Database`).
- **Central & Assets Dashboards (`plugins/vulnerabilitymanagement/hook.php`):**
  - Cleaned up `glpi_dashboards_items` on both the `central` and `assets` dashboards to remove cards for `Monitor`, `NetworkEquipment`, `Phone`, `Printer`, `Rack`, `Enclosure`, `PDU`, `SoftwareLicense`, `Supplier`, `Document`, `KnowbaseItem`, `Project`, and `Ticket`, retaining only cards for **Business Applications**, **Computers / Servers**, **Software**, and **Vulnerabilities / Open Findings**.
- **Supported Plugin Itemtypes & Search Options (`src/ApplicationAsset.php`, `src/VulnerabilityInstance.php`, `src/Application.php`):**
  - Restricted `SUPPORTED_ITEMTYPES` in both `ApplicationAsset` and `VulnerabilityInstance` to `['Computer', 'Software']` (removing `NetworkEquipment`, `Database`, `Peripheral`, `Printer`, `Phone`).
  - Removed `Network Equipment` (`id = 36`) and `Database` (`id = 37`) search options from `Application::rawSearchOptions()`.

### 3. Time-Series Vulnerability Tracking & Microsoft Defender Extract Reconciliation
- **Snapshot History Table (`glpi_plugin_vulnerabilitymanagement_snapshots` & `src/Snapshot.php`):**
  - Stores daily/weekly point-in-time vulnerability snapshots (`snapshot_date`, `source`, `filename`, `total_open`, `count_new`, `count_active`, `count_reopened`, `count_fixed`, `newly_fixed`, `count_ignored`, `open_urgent`, `open_critical`, `open_serious`, `open_medium`, `open_minimal`, `open_kev`, `app_metrics_json`).
  - Added `date_fixed` (`timestamp`) to `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances` (with search option `21` and Twig form field) to track remediation timestamps and Mean Time To Remediate (**MTTR**).
- **Microsoft Defender Extract Importer & Lifecycle State Machine (`front/import.php`):**
  - Native auto-detection for **Microsoft Defender Vulnerability Management (MDVM)** CSV exports (`CveId`, `DeviceName`, `VulnerabilitySeverityLevel`, `CvssScore`, `SoftwareVendor`, `SoftwareName`, `SoftwareVersion`, `RecommendedSecurityUpdate`, `ExploitabilityLevel`, `FirstSeenTimestamp`, `LastSeenTimestamp`).
  - Automatic status lifecycle transitions across daily/weekly extracts:
    - **New (`1`):** First time `(DeviceName, CveId)` is seen.
    - **Active (`2`):** Finding persists in subsequent daily/weekly extracts (`times_found` incremented, `last_found` updated).
    - **Fixed (`4`):** Previously open finding on a scanned host is absent from the new extract (`date_fixed = snapshot_date`).
    - **Re-opened (`3`):** Previously `Fixed` finding reappears in a subsequent extract.
- **Over-Time Evolution Charts (`src/DashboardProvider.php` & `front/import.php`):**
  - Added **Vulnerability Status Evolution Over Time** (`vm_trend_status_evolution`) and **Open Vulnerabilities by Severity Over Time** (`vm_trend_severity_evolution`) charts to GLPI's **Central Dashboard**, plus interactive SVG trend charts, KPI delta cards, and a chronological Snapshot History table on **Management > Import CSV Data**.
  - Added sample weekly Microsoft Defender extracts in `mock_data/csv/defender/` (`defender_extract_2026-11-01.csv`, `defender_extract_2026-11-08.csv`) and 6 weeks of pre-seeded snapshot history in `mock_data/sql/seed_glpi_mock_data.sql`.

---

## 🤖 LLM Implementation & Deployment Guide (Replicating Elsewhere)

If you are an LLM or engineer deploying or porting these modifications to another GLPI 11/12 instance, follow the exact specifications below.

### A. Quick Deployment (From This Repository to Another Target GLPI)

If you have access to this repository on the target machine:

```bash
# 1. Copy / extract the plugin into GLPI's marketplace or plugins directory
# For Docker (official glpi/glpi image):
tar -czf - -C plugins vulnerabilitymanagement | docker exec -i -u www-data <glpi_container> tar -xzf - -C /var/glpi/marketplace/

# For Bare-Metal Linux:
sudo cp -a plugins/vulnerabilitymanagement /var/www/glpi/plugins/
sudo chown -R www-data:www-data /var/www/glpi/plugins/vulnerabilitymanagement

# 2. Run plugin install/migration & clear GLPI cache
# Calling plugin_vulnerabilitymanagement_install() runs all CREATE TABLE / ALTER TABLE migrations
# and provisions the Central Dashboard cards (including the 2 time-series trend charts).
docker exec -u www-data <glpi_container> php -r '
require "/var/www/glpi/vendor/autoload.php";
$k = new \Glpi\Kernel\Kernel();
$k->boot();
include_once "/var/glpi/marketplace/vulnerabilitymanagement/setup.php";
include_once "/var/glpi/marketplace/vulnerabilitymanagement/hook.php";
plugin_vulnerabilitymanagement_install();
'
docker exec -u www-data <glpi_container> /var/www/glpi/bin/console cache:clear

# 3. (Optional) Seed the mock CMDB + 6 weeks of vulnerability snapshot history
docker exec -i <db_container> mariadb -u <db_user> -p<db_pass> <db_name> < mock_data/sql/seed_glpi_mock_data.sql
```

---

### B. Complete List of Added & Modified Files

| File Path | Action | Purpose |
| :--- | :--- | :--- |
| `plugins/vulnerabilitymanagement/src/Snapshot.php` | **Created** | `CommonDBTM` model (`glpi_plugin_vulnerabilitymanagement_snapshots`) with `Snapshot::captureSnapshot($date, $source, $filename, $newly_fixed)` and `Snapshot::getTimeline($limit)` to record and query historical vulnerability metrics. |
| `plugins/vulnerabilitymanagement/hook.php` | **Modified** | Adds `glpi_plugin_vulnerabilitymanagement_snapshots` table creation, `ALTER TABLE` migrations (`date_fixed`, `exposure`, `exploit_status`, `cisa_kev`, `exploit_frameworks`), `Hooks::REDEFINE_MENUS` menu filtering, and Central Dashboard cards (`vm_trend_status_evolution`, `vm_trend_severity_evolution`). |
| `plugins/vulnerabilitymanagement/setup.php` | **Modified** | Registers `Snapshot::class` and `CsvImport::class`, restricts `$CFG_GLPI['asset_types'] = ['Computer', 'Software']`, hooks `Hooks::REDEFINE_MENUS`, and invalidates cached session menus when old asset types are present. |
| `plugins/vulnerabilitymanagement/front/import.php` | **Modified** | Adds Microsoft Defender CSV auto-detection (`defender_extract`), extract date selector (`snapshot_date`), full-snapshot auto-remediation (`auto_remediate`), `New -> Active -> Fixed -> Re-opened` state machine, automatic snapshot capture, MTTR calculation, interactive SVG trend charts, and Snapshot History table. |
| `plugins/vulnerabilitymanagement/src/DashboardProvider.php` | **Modified** | Adds `vm_trend_status_evolution` (`statusEvolutionOverTime`, diverging `stackedbars` widget with positive `Active (+)`, `Re-opened (+)`, `New (+)` and negative `Fixed (-)`) and `vm_trend_severity_evolution` (`severityEvolutionOverTime`, `stackedbars` widget) to the Central Dashboard. |
| `plugins/vulnerabilitymanagement/src/VulnerabilityInstance.php` | **Modified** | Restricts `SUPPORTED_ITEMTYPES` to `['Computer', 'Software']`; auto-populates/clears `date_fixed` in `prepareInputForAdd()` and `prepareInputForUpdate()`; adds search option `21` (`Date Fixed / Remediated`); adds status breakdown badges (`New`, `Active`, `Re-opened`, `Fixed`, `Ignored`) to the Business Application tab. |
| `plugins/vulnerabilitymanagement/templates/vulnerability_instance.html.twig` | **Modified** | Adds `date_fixed` (`Date Fixed / Remediated`) datetime field to the Vulnerability Instance form. |
| `plugins/vulnerabilitymanagement/src/Vulnerability.php` | **Modified** | Fixes search option ID collision by assigning IDs `18` (`exploit_status`), `19` (`cisa_kev`), and `20` (`exploit_frameworks`). |
| `plugins/vulnerabilitymanagement/src/CsvImport.php` | **Modified** | Fixes GLPI 12 fatal error by replacing removed `Plugin::getWebDir()` with `$CFG_GLPI['root_doc'] . '/plugins/vulnerabilitymanagement/front/import.php'`. |
| `plugins/vulnerabilitymanagement/src/ApplicationAsset.php` | **Modified** | Restricts `SUPPORTED_ITEMTYPES` to `['Computer', 'Software']`. |
| `plugins/vulnerabilitymanagement/src/Application.php` | **Modified** | Removes `Network Equipment` (`36`) and `Database` (`37`) search options. |
| `mock_data/csv/defender/defender_extract_2026-11-01.csv` | **Created** | Week 1 sample Microsoft Defender Vulnerability Management (MDVM) CSV extract. |
| `mock_data/csv/defender/defender_extract_2026-11-08.csv` | **Created** | Week 2 sample MDVM CSV extract demonstrating `New`, `Active`, `Fixed`, and `Re-opened` transitions. |
| `mock_data/sql/seed_glpi_mock_data.sql` | **Modified** | Populates `date_fixed` on remediated findings and seeds 6 weekly historical snapshots (`2026-10-04` to `2026-11-08`). |

---

### C. Exact SQL Schema Changes

If applying schema changes manually against MariaDB / MySQL:

```sql
-- 1. Threat Intelligence columns on Generic Vulnerabilities
ALTER TABLE `glpi_plugin_vulnerabilitymanagement_vulnerabilities`
  ADD COLUMN IF NOT EXISTS `exploit_status` tinyint NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS `cisa_kev` tinyint NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS `exploit_frameworks` varchar(255) DEFAULT NULL;

-- 2. Exposure & Remediation Timestamp on Vulnerability Instances
ALTER TABLE `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances`
  ADD COLUMN IF NOT EXISTS `exposure` varchar(64) DEFAULT 'internal',
  ADD COLUMN IF NOT EXISTS `date_fixed` timestamp NULL DEFAULT NULL;

-- 3. Time-Series Vulnerability Snapshots Table
CREATE TABLE IF NOT EXISTS `glpi_plugin_vulnerabilitymanagement_snapshots` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `snapshot_date` date NOT NULL,
  `source` varchar(128) DEFAULT 'Defender Extract',
  `filename` varchar(255) DEFAULT NULL,
  `total_open` int unsigned NOT NULL DEFAULT 0,
  `count_new` int unsigned NOT NULL DEFAULT 0,
  `count_active` int unsigned NOT NULL DEFAULT 0,
  `count_reopened` int unsigned NOT NULL DEFAULT 0,
  `count_fixed` int unsigned NOT NULL DEFAULT 0,
  `newly_fixed` int unsigned NOT NULL DEFAULT 0,
  `count_ignored` int unsigned NOT NULL DEFAULT 0,
  `open_urgent` int unsigned NOT NULL DEFAULT 0,
  `open_critical` int unsigned NOT NULL DEFAULT 0,
  `open_serious` int unsigned NOT NULL DEFAULT 0,
  `open_medium` int unsigned NOT NULL DEFAULT 0,
  `open_minimal` int unsigned NOT NULL DEFAULT 0,
  `open_kev` int unsigned NOT NULL DEFAULT 0,
  `app_metrics_json` longtext DEFAULT NULL,
  `date_creation` timestamp NULL DEFAULT NULL,
  `date_mod` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_snapshot_date_source` (`snapshot_date`, `source`),
  KEY `snapshot_date` (`snapshot_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
```

---

### D. Architectural Specifications for Re-Implementation

#### 1. Microsoft Defender Extract Format & Auto-Detection (`front/import.php`)
- **Auto-Detection Rule:** In `detect_csv_format(array $headers)`, if headers contain `cveid` and `devicename` (or `vulnerabilities_id`/`machineid` with `vulnerabilityseveritylevel` or `recommendedsecurityupdate`), classify as `'defender_extract'`.
- **Snapshot Date Resolution:**
  1. Uses the user-supplied `snapshot_date` form input (`YYYY-MM-DD`).
  2. Or parses `YYYY-MM-DD` from the uploaded filename (e.g., `defender_extract_2026-11-08.csv`).
  3. Or falls back to the maximum `LastSeenTimestamp` in the CSV rows.
- **Column Mapping:**
  - `CveId` -> `Vulnerability.cve` & `Vulnerability.vuln_code`
  - `DeviceName` -> `Computer.name` (matched by full FQDN or short hostname prefix before `.`)
  - `VulnerabilitySeverityLevel` -> `Critical` = `5` (Urgent), `High` = `4` (Critical), `Medium` = `3` (Serious), `Low` = `2` (Medium)
  - `CvssScore` -> `Vulnerability.cvss_score`
  - `SoftwareVendor`, `SoftwareName`, `SoftwareVersion` -> Upserts `Software`, `SoftwareVersion`, and links to host via `glpi_items_softwareversions` (`date_install`)
  - `ExploitabilityLevel` / `PublicExploit` / `IsExploitVerified` -> Maps `ExploitVerified` / `CISA KEV` to `exploit_status = 3, cisa_kev = 1`; `ExploitExists` / `Weaponized` to `exploit_status = 2`; `PoC` to `exploit_status = 1`
  - `RecommendedSecurityUpdate` / `RecommendedSecurityUpdateId` -> `Vulnerability.solution` and `Vulnerability.patch_available = 1`
  - `FirstSeenTimestamp`, `LastSeenTimestamp` -> `VulnerabilityInstance.first_found`, `VulnerabilityInstance.last_found`

#### 2. Status Lifecycle State Machine (`New -> Active -> Fixed -> Re-opened`)
When importing a Defender extract (`defender_extract`) or flat scan (`scan_flat`):
1. Track every seen host `$seen_host_ids[$comp_id] = true` and every seen pair `$seen_host_vulns[$comp_id][$vuln_id] = true`.
2. For each row in the extract:
   - **Not previously in DB:** Insert `VulnerabilityInstance` with `status = 1` (`STATUS_NEW`), `first_found = $first_seen`, `last_found = $last_seen`, `times_found = 1`.
   - **Previously `STATUS_FIXED` (`4`):** Transition to `status = 3` (`STATUS_REOPENED`), set `date_fixed = NULL`, increment `times_found`, and update `last_found = $snapshot_ts`.
   - **Previously `STATUS_NEW` (`1`), `STATUS_ACTIVE` (`2`), or `STATUS_REOPENED` (`3`):**
     - If `$existing['first_found'] < $snapshot_date . ' 00:00:00'`, transition `STATUS_NEW` (`1`) -> `STATUS_ACTIVE` (`2`).
     - Increment `times_found` and update `last_found = $snapshot_ts`.
3. **Full-Snapshot Auto-Remediation (`auto_remediate = 1`):**
   - Query all open `VulnerabilityInstance` rows (`status IN (1, 2, 3)`) where `itemtype = 'Computer'` and `items_id IN (array_keys($seen_host_ids))`.
   - Any instance whose `($items_id, $vuln_id)` is **not** in `$seen_host_vulns` is updated to `status = 4` (`STATUS_FIXED`) and `date_fixed = $snapshot_ts`, incrementing `$newly_fixed_count`.
4. **Snapshot Capture:**
   - Call `Snapshot::captureSnapshot($snapshot_date, $source_label, $filename, $newly_fixed_count)` which aggregates live counts from `glpi_plugin_vulnerabilitymanagement_vulnerabilityinstances` and upserts the row in `glpi_plugin_vulnerabilitymanagement_snapshots` keyed by `(snapshot_date, source)`.

#### 3. GLPI 12 Central Dashboard Multi-Series Chart Format (`src/DashboardProvider.php`)
- Register two cards in `DashboardProvider::getCards()`:
  - `'vm_trend_status_evolution'` -> `widgettype => ['stackedbars', 'bars', 'lines', 'areas']` (diverging stacked bar chart where `Active (+)`, `Re-opened (+)`, and `New (+)` are positive values above `0` and `Fixed (-)` is `-1 * count_fixed` below `0`)
  - `'vm_trend_severity_evolution'` -> `widgettype => ['stackedbars', 'lines', 'areas', 'bars']`
- GLPI 12 multi-series chart providers (`Widget::stackedBars`) require returning:
  ```php
  [
      'label' => 'Vulnerability Status Evolution Over Time (+Open vs -Fixed)',
      'icon'  => 'ti ti-chart-bar',
      'data'  => [
          'labels' => ['2026-10-04', '2026-10-11', ...],
          'series' => [
              ['name' => 'Active (+)',    'data' => [['value' => 6,  'url' => '...', 'itemStyle' => ['color' => '#f97316']], ...]],
              ['name' => 'Re-opened (+)', 'data' => [['value' => 1,  'url' => '...', 'itemStyle' => ['color' => '#eab308']], ...]],
              ['name' => 'New (+)',       'data' => [['value' => 2,  'url' => '...', 'itemStyle' => ['color' => '#0ea5e9']], ...]],
              ['name' => 'Fixed (-)',     'data' => [['value' => -2, 'url' => '...', 'itemStyle' => ['color' => '#16a34a']], ...]],
          ],
      ],
  ]
  ```



