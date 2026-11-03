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

