#fetch_beefplus.sh
# Description: This script logs into the Beefplus API, retrieves session information, and fetches a page using the session cookies.
#!/usr/bin/env bash
set -euo pipefail

# 1) ログインAPIにPOSTしてJSONを受け取る
resp="$(curl -s \
  -H "Content-Type: application/json" \
  -d '{"student_number":"2435109t","password":"SdjTf=8Q"}' \
  http://127.0.0.1:5001/login)"

# 2) session_url と cookies を jq で抽出
session_url="$(echo "$resp" | jq -r '.session_url')"
# cookie文字列 "NAME1=VAL1; NAME2=VAL2; …" の形式に整形
cookie_str="$(echo "$resp" \
  | jq -r '.cookies[] | "\(.name)=\(.value)"' \
  | paste -sd '; ' - )"

# 3) 取得した cookie をつけて実際のページを取得
curl -s \
  --cookie "$cookie_str" \
  "$session_url"