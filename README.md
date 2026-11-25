
# drone_project

[![test](https://github.com/s25c1126my-lang/New-Command/actions/workflows/test.yml/badge.svg)](https://github.com/s25c1126my-lang/New-Command/actions/workflows/test.yml)

ドローンなどのGPSログ（NMEAフォーマット）を標準入力から受け取り、
GeoJSON形式に変換して標準出力するLinuxコマンドです。

GPSの測位地点や飛行軌跡を地図上に可視化するための
データ変換に利用できます。

## 機能

- NMEAフォーマット（`$GPGGA`, `$GNRMC`）の解析
- 緯度・経度の度分表記から10進数表記への変換
- GeoJSON FeatureCollection形式での出力
- 複数行のGPSログの一括処理
- 無効なGPS測位データの除外
- 不正な座標データの検出
- 平均海面基準の高度情報の取得（GPGGAのみ）
- 飛行軌跡の生成（`--track`）
- エラーメッセージの標準エラー出力（stderr）

## 必要なソフトウェア

- Python 3（3.12.3で動作確認済み）
- Git（リポジトリの取得に使用）

外部Pythonライブラリのインストールは不要です。

## インストール方法

以下のコマンドを順に実行してください。

```bash
$ git clone https://github.com/s25c1126my-lang/New-Command.git
$ cd New-Command
```

## 使い方

### GPSの位置情報を取得する

NMEA形式のGPSデータを標準入力から受け取り、
GeoJSONのPoint形式に変換します。

```bash
$ echo '$GPGGA,123519,3541.1234,N,14001.5678,E,1,08,0.9,25.4,M,46.9,M,,*79' | python3 drone_project.py
```

出力結果：

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
          35.68539
        ]
      },
      "properties": {
        "altitude_msl_m": 25.4
      }
    }
  ]
}
```

座標は経度、緯度の順に出力されます。
GPGGAに高度情報が含まれる場合は、平均海面基準の高度を
メートル単位で `altitude_msl_m` に格納します。

### 飛行軌跡を生成する

`--track` オプションを使用することで、
複数のGPS測位地点を入力順に結び、
GeoJSONのLineString形式で出力できます。

```bash
$ printf '%s\n' \
  '$GPGGA,123519,3541.1234,N,14001.5678,E,1,08,0.9,25.4,M,46.9,M,,*79' \
  '$GPGGA,123520,3541.5678,N,14001.9876,E,1,08,0.9,26.0,M,46.9,M,,*70' \
  | python3 drone_project.py --track
```

出力結果：

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            140.02613,
            35.68539
          ],
          [
            140.03312666666667,
            35.692796666666666
          ]
        ]
      },
      "properties": {
        "point_count": 2
      }
    }
  ]
}
```

`point_count` は飛行軌跡を構成するGPS測位点の数を表します。

なお、上記のGPSデータは動作確認用のサンプルであり、
実際のドローンの飛行記録ではありません。

### GPSログファイルを変換する

NMEA形式のGPSログを保存したファイル（`gps.log`）を用意します。

以下のコマンドを実行することで、
複数行のGPSログを一括してGeoJSON形式に変換できます。

```bash
$ cat gps.log | python3 drone_project.py
```

### GPSの位置情報をファイルに保存する

標準出力をリダイレクトすることで、
変換結果をGeoJSONファイルとして保存できます。

```bash
$ cat gps.log | python3 drone_project.py > points.geojson
```

### 飛行軌跡をファイルに保存する

```bash
$ cat gps.log | python3 drone_project.py --track > flight.geojson
```

### 飛行軌跡を地図上に表示する

生成したGeoJSONファイルは、
geojson.ioなどのGeoJSON対応ツールで地図上に表示できます。

1. `--track` オプションを使用して `flight.geojson` を生成する。
2. [geojson.io](https://geojson.io/) にアクセスする。
3. 生成した `flight.geojson` を読み込む。
4. 地図上に表示された飛行軌跡を確認する。

### ヘルプを表示する

```bash
$ python3 drone_project.py --help
```

## オプション

| オプション | 説明 |
| --- | --- |
| なし | GPS測位地点をPoint形式で出力 |
| `--track` | 飛行軌跡をLineString形式で出力 |
| `--help`, `-h` | 使用方法を表示 |

## エラー処理

以下のようなデータは、変換対象から除外されます。

- GPSの測位状態が無効なデータ
- 必要な項目が不足している対応フォーマットのデータ
- 不正な緯度・経度を含むデータ
- 不正な方角を含むデータ

エラーメッセージは標準エラー出力（stderr）に出力されます。
標準出力には変換結果のみが出力されます。

また、`--track` オプションを使用した際に、
有効なGPS測位点が2点未満の場合は、
エラーメッセージを出力し、終了ステータス1で終了します。

## 注意事項

- 対応するNMEAメッセージは `$GPGGA` と `$GNRMC` です。
- 対応していないメッセージは無視されます。
- 飛行軌跡の生成には2点以上の有効なGPS測位点が必要です。
- 飛行軌跡は入力されたデータの順番に生成されます。
- 飛行軌跡には高度情報を含みません。
- NMEAのチェックサム検証には対応していません。
- GPS測位地点の重複除去には対応していません。
- GPSデータの時刻順への並べ替えには対応していません。

## テスト

以下のコマンドでテストを実行できます。

```bash
$ bash test.bash
```

テストでは以下の項目を確認しています。

- GPGGAの正常な変換
- GNRMCの正常な変換
- 南緯・西経の変換
- GPS測位失敗時の処理
- 不正な座標データの処理
- 空の入力に対する処理
- 複数行のGPSログの処理
- 飛行軌跡の生成
- 飛行軌跡生成時の座標数不足に対する処理
- ヘルプの表示

GitHub Actionsによる自動テストも実施しています。

## テスト環境

- Ubuntu 24.04
- Python 3.12.3

## 参考資料

- [NMEA GPGGA - NovAtel](https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm)
- [NMEA GPRMC - NovAtel](https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm)
- [RFC 7946 - The GeoJSON Format](https://www.rfc-editor.org/rfc/rfc7946.html)
- [Python公式ドキュメント - argparse](https://docs.python.org/ja/3/library/argparse.html)

## ライセンス

このソフトウェアはBSD 3-Clause Licenseの下で公開されています。
詳細は[LICENSE](./LICENSE)を参照してください。

© 2026 Takumi Yokoyama
