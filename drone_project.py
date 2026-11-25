
#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Takumi Yokoyama
# SPDX-License-Identifier: BSD-3-Clause

import json
import sys
import math


def parse_nmea_latlon(lat_str, lat_dir, lon_str, lon_dir):
    """NMEAの度分表記を10進数の緯度経度に変換"""

    lat_deg = float(lat_str[:2])
    lat_min = float(lat_str[2:])

    lon_deg = float(lon_str[:3])
    lon_min = float(lon_str[3:])

    # 度分表記の異常値を確認
    if not (0 <= lat_deg <= 90 and
            0 <= lon_deg <= 180 and
            0 <= lat_min < 60 and
            0 <= lon_min < 60):
        raise ValueError("Invalid latitude or longitude")

    lat = lat_deg + lat_min / 60.0
    lon = lon_deg + lon_min / 60.0

    # 緯度・経度の範囲を確認
    if lat > 90 or lon > 180:
        raise ValueError("Invalid coordinate range")

    # 方角の確認
    if lat_dir not in ("N", "S") or lon_dir not in ("E", "W"):
        raise ValueError("Invalid direction")

    if lat_dir == "S":
        lat = -lat

    if lon_dir == "W":
        lon = -lon

    return lat, lon


def main():
    features = []

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        parts = line.split(",")
        properties = {}

        try:
            # GPGGAの解析
            if parts[0] == "$GPGGA":

                if len(parts) < 11:
                    raise ValueError("Missing GGA fields")

                # GPSの測位状態を確認
                if int(parts[6]) <= 0:
                    raise ValueError("No GPS fix")

                lat, lon = parse_nmea_latlon(
                    parts[2], parts[3], parts[4], parts[5]
                )

                # 平均海面基準の高度を取得
                if parts[9]:
                    alt = float(parts[9])

                    if not math.isfinite(alt) or parts[10] != "M":
                        raise ValueError("Invalid altitude")

                    properties["altitude_msl_m"] = alt

            # GNRMCの解析
            elif parts[0] == "$GNRMC":

                if len(parts) < 10:
                    raise ValueError("Missing RMC fields")

                # GPSの測位状態を確認
                if parts[2] != "A":
                    raise ValueError("Invalid GPS fix")

                lat, lon = parse_nmea_latlon(
                    parts[3], parts[4], parts[5], parts[6]
                )

            # 対応していないデータは無視
            else:
                continue

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat],
                },
                "properties": properties,
            }

            features.append(feature)

        except (ValueError, IndexError) as e:
            sys.stderr.write(f"Error: {e}: {line}\n")

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    print(json.dumps(geojson, indent=2))


if __name__ == "__main__":
    main()
