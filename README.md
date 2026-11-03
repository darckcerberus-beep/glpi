# GLPI Deployment (Docker Compose)

This directory contains the Docker configuration for **GLPI 12.0.1** and **MariaDB 11.4**.

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


