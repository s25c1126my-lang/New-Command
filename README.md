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

```bash
echo '\$GPGGA,083559.00,3541.1493,N,13942.2312,E,1,08,1.0,15.0,M,39.5,M,,*42' | ./drone_nmea.py


BSD 3-Clause License

Copyright (c) 2026, Takumi Yokoyama

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.