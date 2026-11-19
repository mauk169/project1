import csv
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
import yaml

DB_PATH = "finance.db"
OUT_DIR = "out"

def fetch_operations_with_authors(db_path: str = DB_PATH) -> list[dict]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            o.operation_id,
            o.operation_type,
            o.amount,
            o.description,
            u.user_id,
            u.login
        FROM operations o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.operation_id
    """)
    rows = cur.fetchall()
    conn.close()

    records = []
    for row in rows:
        record = {
            "operation_id": row[0],
            "operation_type": row[1],
            "amount": row[2],
            "description": row[3] if row[3] is not None else "",
            "author": {
                "user_id": row[4],
                "login": row[5],
            },
        }
        records.append(record)

    return records

def save_json(records: list[dict], out_dir: str = OUT_DIR) -> str:
    file_path = os.path.join(out_dir, "data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return file_path

def save_csv(records: list[dict], out_dir: str = OUT_DIR) -> str:
    file_path = os.path.join(out_dir, "data.csv")
    fieldnames = [
        "operation_id",
        "operation_type",
        "amount",
        "description",
        "author_id",
        "author_login",
    ]

    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in records:
            writer.writerow({
                "operation_id": item["operation_id"],
                "operation_type": item["operation_type"],
                "amount": item["amount"],
                "description": item["description"],
                "author_id": item["author"]["user_id"],
                "author_login": item["author"]["login"],
            })

    return file_path

def save_xml(records: list[dict], out_dir: str = OUT_DIR) -> str:
    file_path = os.path.join(out_dir, "data.xml")
    root = ET.Element("operations")

    for item in records:
        op_elem = ET.SubElement(root, "operation")

        ET.SubElement(op_elem, "operation_id").text = str(item["operation_id"])
        ET.SubElement(op_elem, "operation_type").text = str(item["operation_type"])
        ET.SubElement(op_elem, "amount").text = str(item["amount"])
        ET.SubElement(op_elem, "description").text = str(item["description"])

        author_elem = ET.SubElement(op_elem, "author")
        ET.SubElement(author_elem, "user_id").text = str(item["author"]["user_id"])
        ET.SubElement(author_elem, "login").text = str(item["author"]["login"])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    return file_path

def save_yaml(records: list[dict], out_dir: str = OUT_DIR) -> str:
    file_path = os.path.join(out_dir, "data.yaml")
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False)
    return file_path

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    records = fetch_operations_with_authors(DB_PATH)

    json_path = save_json(records, OUT_DIR)
    csv_path = save_csv(records, OUT_DIR)
    xml_path = save_xml(records, OUT_DIR)
    yaml_path = save_yaml(records, OUT_DIR)

    print("Файлы успешно сформированы:")
    print(" -", json_path)
    print(" -", csv_path)
    print(" -", xml_path)
    print(" -", yaml_path)

if __name__ == "__main__":
    main()