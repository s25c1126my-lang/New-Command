# New-Command
Drone-Related Commands
# drone_project

ドローン等のGPSログ（NMEAフォーマット）を標準入力から受け取り、GeoJSONフォーマットに変換して標準出力するLinuxコマンドです。

## 機能
- NMEAフォーマット（`$GPGGA`, `$GNRMC`）のテキスト入力を解析
- 緯度・経度を10進数に変換し、GeoJSON FeatureCollection形式で出力
- エラー行は標準エラー出力（stderr）に出力

## 必要な環境
- Python 3.x

## 使い方
標準入力（パイプ）からテキストを渡して実行します。

```bash
echo '\$GPGGA,083559.00,3541.1493,N,13942.2312,E,1,08,1.0,15.0,M,39.5,M,,*42' | ./drone_nmea.py