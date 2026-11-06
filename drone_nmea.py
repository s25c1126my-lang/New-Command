#!/usr/bin/env python3
import json
import sys


def parse_nmea_latlon(lat_str, lat_dir, lon_str, lon_dir):
    """NMEAの度分表記(DDMM.MMMM / DDDMM.MMMM)を10進数の緯度経度に変換"""
    lat_deg = float(lat_str[:2])
    lat_min = float(lat_str[2:])
    lat = lat_deg + (lat_min / 60.0)
    if lat_dir == "S":
        lat = -lat

    lon_deg = float(lon_str[:3])
    lon_min = float(lon_str[3:])
    lon = lon_deg + (lon_min / 60.0)
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

        # $GPGGA または $GNRMC のGPS位置情報行を解析
        if parts[0] in ["$GPGGA", "$GNRMC"] and len(parts) >= 6:
            try:
                lat, lon = parse_nmea_latlon(
                    parts[2], parts[3], parts[4], parts[5]
                )
                alt = float(parts[9]) if len(parts) > 9 and parts[9] else 0.0

                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat, alt],
                    },
                    "properties": {},
                }
                features.append(feature)
            except (ValueError, IndexError):
                # エラーメッセージは標準エラー出力（sys.stderr）へ[cite: 1]
                sys.stderr.write(f"Error: Invalid NMEA format: {line}\n")

    geojson = {"type": "FeatureCollection", "features": features}
    # 結果のみを標準出力（sys.stdout）へ出力[cite: 1]
    print(json.dumps(geojson, indent=2))


if __name__ == "__main__":
    main()