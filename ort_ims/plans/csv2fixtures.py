import csv
import json
from pathlib import Path

FILE_DIR_ = Path(__file__).resolve().parent


def read_csv_to_fixtures(file_path, model):
    # model = model.lower()
    try:
        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            fixtures = []
            for id, row in enumerate(reader):
                fields = {}
                for i, header in enumerate(headers):
                    fields[header] = row[i]
                fixture = {
                    "model": model,
                    "pk": id + 1,
                    "fields": fields,
                }
                fixtures.append(fixture)
            return fixtures
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return []
    except Exception as e:
        print(f"读取文件 {file_path} 时发生错误: {e}")
        return []


customer = read_csv_to_fixtures(
    FILE_DIR_.joinpath("static/data/custcode.csv"), "plans.tcustcode"
)
producttype = read_csv_to_fixtures(
    FILE_DIR_.joinpath("static/data/producttype.csv"), "plans.tproducttype"
)
testitem = read_csv_to_fixtures(
    FILE_DIR_.joinpath("static/data/testitem.csv"), "plans.ttestitem"
)

if __name__ == "__main__":
    with open(FILE_DIR_.joinpath("fixtures/customer.json"), "w", encoding="utf-8") as f:
        json.dump(customer, f, ensure_ascii=False, indent=4)
    with open(
        FILE_DIR_.joinpath("fixtures/producttype.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(producttype, f, ensure_ascii=False, indent=4)
    with open(FILE_DIR_.joinpath("fixtures/testitem.json"), "w", encoding="utf-8") as f:
        json.dump(testitem, f, ensure_ascii=False, indent=4)
