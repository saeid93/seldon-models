import base64
import json


payload = {
    "meta": {"tags": {"some": "tag"}},
    "data": {"names": ["a", "b", "c"], "ndarray": [[1, 2, 3]]},
}

cmd = {
    "method": "POST",
    "header": {"Content-Type": ["application/json"]},
    "url": "http://localhost:9000/api/v1.0/predictions",
    "body": base64.b64encode(bytes(json.dumps(payload), "utf-8")).decode("utf-8"),
}

with open("vegeta-target.json", mode="w") as file:
    json.dump(cmd, file)
    file.write("\n\n")
