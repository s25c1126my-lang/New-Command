
# New-Command

## drone_project

ドローンなどのGPSログ（NMEAフォーマット）を標準入力から受け取り、
GeoJSON形式に変換して標準出力するLinuxコマンドです。

GPSの位置情報を地図上に表示するためのデータ変換などに利用できます。

## 機能

- NMEAフォーマット（`$GPGGA`）のテキストデータを解析
- 緯度・経度を度分表記から10進数表記に変換
- GPSの位置情報をGeoJSON FeatureCollection形式で出力
- 複数行のGPSログを一括処理
- 解析時のエラーメッセージを標準エラー出力（stderr）に出力

## インストール方法

以下のコマンドを順に実行してください。

```bash
$ git clone https://github.com/ユーザー名/New-Command.git
$ cd New-Command
$ chmod +x drone_project.py
```

## 使い方

### GPSデータを直接入力する場合

```bash
$ echo '$GPGGA,123519,3541.1234,N,14001.5678,E,1,08,0.9,25.4,M,46.9,M,,*79' | ./drone_project.py
```

### 出力結果

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          140.02613,
          35.68539,
          25.4
        ]
      },
      "properties": {}
    }
  ]
}
```

座標は経度、緯度、高度の順に出力されます。
現在の高度はGPGGAに含まれる平均海面基準の値です。

### GPSログファイルを読み込む場合

```bash
$ cat gps.log | ./drone_project.py
```

### 変換結果をファイルに保存する場合

```bash
$ cat gps.log | ./drone_project.py > flight.geojson
```

## 必要なソフトウェア

- Python 3

## 動作環境

- OS：テスト環境を記載
- Python：テストしたバージョンを記載

## 参考資料

- [NMEA GPGGA仕様](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm)
- [GeoJSON仕様（RFC 7946）](https://www.rfc-editor.org/rfc/rfc7946.html)

## ライセンス

このソフトウェアはBSD 3-Clause Licenseの下で公開されています。
詳細はLICENSEファイルを参照してください。

© 2026 Takumi Yokoyama
