
#!/bin/bash
# SPDX-FileCopyrightText: 2026 Takumi Yokoyama
# SPDX-License-Identifier: BSD-3-Clause

set -eu

cd "$(dirname "$0")"

python3 - <<'PY'
import json
import math
import subprocess

gga = "$GPGGA,123519,3541.1234,N,14001.5678,E,1,08,0.9,25.4,M,46.9,M,,*79"
gga2 = "$GPGGA,123520,3541.5678,N,14001.9876,E,1,08,0.9,26.0,M,46.9,M,,*70"
rmc = "$GNRMC,123519,A,3541.1234,N,14001.5678,E,0.0,0.0,251126,,,A*6F"


def run(data, *args):
    return subprocess.run(
        ["python3", "drone_project.py", *args],
        input=data,
        text=True,
        capture_output=True
    )


# 1. GPGGAの正常系
result = run(gga)
assert result.returncode == 0

data = json.loads(result.stdout)
assert data["type"] == "FeatureCollection"
assert len(data["features"]) == 1

feature = data["features"][0]
assert feature["type"] == "Feature"
assert feature["geometry"]["type"] == "Point"

lon, lat = feature["geometry"]["coordinates"]
assert math.isclose(lon, 140.02613)
assert math.isclose(lat, 35.68539)
assert feature["properties"]["altitude_msl_m"] == 25.4

print("PASS: GPGGA")


# 2. GNRMCの正常系
result = run(rmc)
assert result.returncode == 0

data = json.loads(result.stdout)
feature = data["features"][0]

lon, lat = feature["geometry"]["coordinates"]
assert math.isclose(lon, 140.02613)
assert math.isclose(lat, 35.68539)
assert feature["properties"] == {}

print("PASS: GNRMC")


# 3. 南緯・西経
result = run(
    gga.replace(",N,", ",S,")
       .replace(",E,", ",W,")
       .split("*")[0]
)

data = json.loads(result.stdout)
lon, lat = data["features"][0]["geometry"]["coordinates"]

assert math.isclose(lon, -140.02613)
assert math.isclose(lat, -35.68539)

print("PASS: South and West")


# 4. GPSの測位失敗
result = run(gga.replace(",1,08,", ",0,08,").split("*")[0])

assert json.loads(result.stdout)["features"] == []
assert "Error:" in result.stderr

print("PASS: No GPS fix")


# 5. 不正な座標
result = run(gga.replace("3541.1234", "abcd").split("*")[0])

assert json.loads(result.stdout)["features"] == []
assert "Error:" in result.stderr

print("PASS: Invalid coordinates")


# 6. 空の入力
result = run("")

assert result.returncode == 0
assert json.loads(result.stdout)["features"] == []

print("PASS: Empty input")


# 7. 複数行の入力
result = run(gga + "\n" + gga2)

assert result.returncode == 0
assert len(json.loads(result.stdout)["features"]) == 2

print("PASS: Multiple input lines")


# 8. 飛行軌跡の生成
result = run(gga + "\n" + gga2, "--track")

assert result.returncode == 0

data = json.loads(result.stdout)
feature = data["features"][0]

assert feature["geometry"]["type"] == "LineString"
assert len(feature["geometry"]["coordinates"]) == 2
assert feature["properties"]["point_count"] == 2

print("PASS: Flight track")


# 9. 飛行軌跡の座標数不足
result = run(gga, "--track")

assert result.returncode == 1
assert "Error:" in result.stderr
assert result.stdout == ""

print("PASS: Insufficient GPS points")


# 10. ヘルプの表示
result = run("", "--help")

assert result.returncode == 0
assert "--track" in result.stdout

print("PASS: Help")

print("All tests passed!")
PY

