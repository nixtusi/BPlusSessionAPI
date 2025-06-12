# BPlusSessionAPI

Flask + Selenium で神戸大学 Beef+ のシングルサインオンを自動突破し、  
ログイン済みセッション付き URL とクッキー情報を返すシンプルな API。

## 🛠️ 前提
- Python 3.8+
- Chrome または Chromium がインストールされていること
- macOS / Linux 環境（ヘッドレス Chrome 動作確認済み）

## 🚀 セットアップ手順
1. リポジトリをクローン  
```bash
git clone https://github.com/nixtusi/BPlusSessionAPI.git
cd BPlusSessionAPI
   
2.	Python 仮想環境を作成・有効化
python3 -m venv venv
source venv/bin/activate

3.	依存パッケージをインストール
pip install -r requirements.txt

4.	環境変数ファイルを用意
.env.example をコピーして .env を作成
cp .env.example .env

.env に以下を記入
BEEFPLUS_USER=あなたの学生番号
BEEFPLUS_PASS=あなたのパスワード

5.	API サーバーを起動
python beefplus_login_api.py
デフォルトで http://0.0.0.0:5001 で待ち受けます。

📡 API エンドポイント
POST /login
	•	Request

{
  "student_number": "2435109t",
  "password":      "SdjTf=8Q"
}


	•	Response (200 OK)

{
  "session_url": "https://beefplus.center.kobe-u.ac.jp/lms/timetable",
  "cookies": [
    {
      "name": "SESSION",
      "value": "...",
      "domain": "beefplus.center.kobe-u.ac.jp",
      "path": "/",
      "httpOnly": true,
      "secure": true
    },
    {
      "name": "ing",
      "value": "...",
      "domain": "beefplus.center.kobe-u.ac.jp",
      "path": "/",
      "httpOnly": true,
      "secure": false
    }
    // …他のクッキー
  ]
}


	•	Status Codes
	•	200：正常終了
	•	400：パラメータ不足
	•	500：内部エラー（Selenium 起動やログイン失敗）

⸻

🔧 iOS (Swift) 側連携例
	1.	NetworkManager.swift で API を呼び出し

NetworkManager.shared.fetchBeefplusSession(
  studentNumber: "2435109t",
  password: "SdjTf=8Q"
) { sessionURL, cookies, error in
  // sessionURL と cookies を WKWebView にセットして表示
}


	2.	WKWebView に HTTPCookie を登録後、load(request:) で表示

let cookieStore = webView.configuration.websiteDataStore.httpCookieStore
for cookie in cookies {
  cookieStore.setCookie(cookie)
}
webView.load(URLRequest(url: sessionURL))



詳細は NetworkManager.swift / BeefplusViewController.swift を参照してください。

⸻

📝 開発メモ
	•	ヘッドレスモードの Chrome 起動には環境に応じたオプション調整が必要な場合があります。
	•	長期運用する場合は Gunicorn＋nginx、Docker 化、ログ/モニタリング設定を検討してください。
	•	環境変数 (.env) の管理には python-dotenv の導入がおすすめです。


