"""
collect_products_versions.py
Patrick Stingley  4/1/2026

Collect installed software product names and versions from Windows registry
and write results to products_versions.csv with columns Product, Version.
"""

import csv
import winreg

OUTPUT_FILE = "products_versions.csv"

REG_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]


def get_value(key, value_name):
    try:
        value, _ = winreg.QueryValueEx(key, value_name)
        return str(value).strip()
    except Exception:
        return ""


def get_installed_software():
    software = set()

    for hive, path in REG_PATHS:
        try:
            with winreg.OpenKey(hive, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            product = get_value(subkey, "DisplayName")
                            version = get_value(subkey, "DisplayVersion")

                            if product:
                                software.add((product, version))
                    except Exception:
                        continue
        except Exception:
            continue

    return sorted(software, key=lambda x: x[0].lower())


def main():
    software = get_installed_software()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Version"])
        writer.writerows(software)

    print(f"Wrote {len(software)} products to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()