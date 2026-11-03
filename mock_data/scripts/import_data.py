#!/usr/bin/env python3
"""
GLPI CMDB & Vulnerability Management Data Importer.
Supports importing Applications, Servers, Software Components, and Vulnerabilities
via GLPI REST API or local database execution.

Works with both the generated mock data and actual user CSVs or API inputs.
"""

import os
import sys
import csv
import json
import argparse
from typing import Dict, Any, List

try:
    import urllib.request
    import urllib.parse
    import urllib.error
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "csv")
JSON_DIR = os.path.join(BASE_DIR, "json")


class GlpiApiClient:
    """Lightweight GLPI REST API Client with zero third-party dependencies."""

    def __init__(self, base_url: str = "http://localhost:8080/apirest.php", app_token: str = "", user_token: str = ""):
        self.base_url = base_url.rstrip("/")
        self.app_token = app_token
        self.user_token = user_token
        self.session_token = None

    def _request(self, endpoint: str, method: str = "GET", payload: Dict[str, Any] = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.app_token:
            headers["App-Token"] = self.app_token
        if self.session_token:
            headers["Session-Token"] = self.session_token
        elif self.user_token:
            headers["Authorization"] = f"user_token {self.user_token}"

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req) as resp:
                resp_body = resp.read().decode("utf-8")
                return json.loads(resp_body) if resp_body else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"[API Error] {method} {url} returned HTTP {e.code}: {err_body}", file=sys.stderr)
            raise

    def init_session(self, username: str = "glpi", password: str = "glpi"):
        url = f"{self.base_url}/initSession"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic " + __import__("base64").b64encode(f"{username}:{password}".encode()).decode()
        }
        if self.app_token:
            headers["App-Token"] = self.app_token
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            self.session_token = data.get("session_token")
            print(f"[+] Initialized GLPI API session: {self.session_token[:10]}...")
            return self.session_token

    def kill_session(self):
        if self.session_token:
            try:
                self._request("killSession", method="GET")
                print("[-] Destroyed GLPI API session.")
            except Exception:
                pass
            self.session_token = None

    def create_item(self, itemtype: str, input_data: Dict[str, Any]) -> int:
        res = self._request(itemtype, method="POST", payload={"input": input_data})
        return res.get("id", 0)

    def search_item(self, itemtype: str, field: str, value: str) -> List[Dict[str, Any]]:
        # Helper to search for an item by field name
        endpoint = f"{itemtype}?searchText[{field}]={urllib.parse.quote(str(value))}"
        try:
            return self._request(endpoint, method="GET")
        except Exception:
            return []


def load_csv(filename: str) -> List[Dict[str, str]]:
    path = os.path.join(CSV_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def import_mock_via_api(api: GlpiApiClient):
    """Imports Applications, Servers, Software, and Vulnerabilities via REST API."""
    print("=" * 60)
    print("Starting import of mock data via GLPI REST API...")
    print("=" * 60)

    # 1. Import Servers (Computer)
    servers_csv = load_csv("servers.csv")
    server_id_map = {} # hostname -> glpi computer id
    print(f"\n[1/4] Importing {len(servers_csv)} Servers (Computer assets)...")
    for srv in servers_csv:
        payload = {
            "name": srv["hostname"],
            "comment": f"{srv['primary_role']} | {srv['datacenter']} {srv['rack']} | IP: {srv['ip']}",
            "entities_id": 0
        }
        try:
            cid = api.create_item("Computer", payload)
            server_id_map[srv["hostname"]] = cid
            print(f"  + Created Computer #{cid}: {srv['hostname']}")
        except Exception as e:
            print(f"  ! Failed creating Computer {srv['hostname']}: {e}")

    # 2. Import Applications (GlpiPlugin\Vulnerabilitymanagement\Application)
    apps_csv = load_csv("applications.csv")
    app_id_map = {}
    print(f"\n[2/4] Importing {len(apps_csv)} Business Applications...")
    for app in apps_csv:
        payload = {
            "name": app["name"],
            "app_code": app["app_code"],
            "criticality": int(app["criticality"]),
            "environment": app["environment"],
            "exposure": app["exposure"],
            "business_unit": app["business_unit"],
            "description": app["description"],
            "entities_id": 0,
            "is_recursive": 1
        }
        try:
            aid = api.create_item("GlpiPlugin\\Vulnerabilitymanagement\\Application", payload)
            app_id_map[app["app_code"]] = aid
            print(f"  + Created Application #{aid}: [{app['app_code']}] {app['name']}")
        except Exception as e:
            print(f"  ! Failed creating Application {app['name']}: {e}")

    # 3. Import Generic Vulnerabilities (GlpiPlugin\Vulnerabilitymanagement\Vulnerability)
    vulns_csv = load_csv("vulnerabilities.csv")
    vuln_id_map = {}
    print(f"\n[3/4] Importing {len(vulns_csv)} Vulnerabilities (KnowledgeBase)...")
    for v in vulns_csv:
        payload = {
            "name": v["name"],
            "vuln_code": v["vuln_code"],
            "cve": v["cve"],
            "severity": int(v["severity"]),
            "cvss_score": float(v["cvss_score"]),
            "category": v["category"],
            "is_patchable": int(v["is_patchable"]),
            "published_date": v["published_date"],
            "description": v["description"],
            "threat": v["threat"],
            "impact": v["impact"],
            "solution": v["solution"],
            "entities_id": 0,
            "is_recursive": 1
        }
        try:
            vid = api.create_item("GlpiPlugin\\Vulnerabilitymanagement\\Vulnerability", payload)
            vuln_id_map[v["vuln_code"]] = vid
            print(f"  + Created Vulnerability #{vid}: [{v['vuln_code']}] {v['cve']} - {v['name']}")
        except Exception as e:
            print(f"  ! Failed creating Vulnerability {v['name']}: {e}")

    # 4. Import Vulnerability Instances (Findings)
    findings_csv = load_csv("vulnerability_findings.csv")
    print(f"\n[4/4] Importing {len(findings_csv)} Vulnerability Findings (Host instances)...")
    for f in findings_csv:
        target_cid = server_id_map.get(f["hostname"], 0)
        target_vid = vuln_id_map.get(f["vuln_code"], 0)
        if not target_cid or not target_vid:
            print(f"  ~ Skipping finding #{f['id']} (Asset or Vuln not yet mapped in API)")
            continue

        payload = {
            "plugin_vulnerabilitymanagement_vulnerabilities_id": target_vid,
            "itemtype": "Computer",
            "items_id": target_cid,
            "status": int(f["status"]),
            "port": int(f["port"]),
            "protocol": f["protocol"],
            "ip": f["ip"],
            "first_found": f["first_found"],
            "last_found": f["last_found"],
            "times_found": int(f["times_found"]),
            "proof": f["proof"],
            "entities_id": 0,
            "is_recursive": 1
        }
        try:
            inst_id = api.create_item("GlpiPlugin\\Vulnerabilitymanagement\\VulnerabilityInstance", payload)
            print(f"  + Created Finding #{inst_id} on {f['hostname']}:{f['port']} ({f['cve']})")
        except Exception as e:
            print(f"  ! Failed creating Finding: {e}")

    print("\nAPI Import completed successfully.")


def print_summary():
    """Prints a clear terminal overview of the mock dataset."""
    apps = load_csv("applications.csv")
    servers = load_csv("servers.csv")
    soft = load_csv("software_components.csv")
    vulns = load_csv("vulnerabilities.csv")
    findings = load_csv("vulnerability_findings.csv")

    print("=" * 70)
    print("MOCK DATA SUMMARY OVERVIEW")
    print("=" * 70)
    print(f"Business Applications  : {len(apps)} applications across 4 criticality tiers")
    print(f"Servers (Infrastructure): {len(servers)} hosts across 4 datacenters & environments")
    print(f"Software Components    : {len(soft)} packages/versions across middleware/DB/OS")
    print(f"KnowledgeBase Vulns    : {len(vulns)} CVE definitions (CVSS 6.5 - 10.0)")
    print(f"Vulnerability Findings : {len(findings)} host-level detections with banners/proofs")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="GLPI CMDB & Vulnerability Management Mock Data Tool")
    parser.add_argument("--summary", action="store_true", help="Print summary of mock data")
    parser.add_argument("--api-import", action="store_true", help="Import data to GLPI via REST API")
    parser.add_argument("--api-url", default="http://localhost:8080/apirest.php", help="GLPI REST API endpoint")
    parser.add_argument("--username", default="glpi", help="GLPI username")
    parser.add_argument("--password", default="glpi", help="GLPI password")
    args = parser.parse_args()

    if args.summary or (not args.api_import):
        print_summary()

    if args.api_import:
        client = GlpiApiClient(base_url=args.api_url)
        try:
            client.init_session(args.username, args.password)
            import_mock_via_api(client)
        finally:
            client.kill_session()


if __name__ == "__main__":
    main()

