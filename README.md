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

---

## 📁 File Structure

- [`docker-compose.yml`](file:///home/romain/glpi/docker-compose.yml): Service specifications for GLPI and MariaDB.
- [`.env`](file:///home/romain/glpi/.env): Environment variables and credentials (ignored by git).

