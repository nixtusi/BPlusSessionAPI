from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ユーザー情報
number = "2435109t"
password = "XXXXXX"

# Selenium起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://kym22-web.ofc.kobe-u.ac.jp/campusweb")

# ログイン処理
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(number)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "kc-login").click()
print("✅ ログイン成功")

# 「シラバス」タブクリック
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "menu-link-mt-sy"))
).click()
print("📘 シラバスタブクリック")

# 「シラバス参照」リンクをクリック（2段階目）
try:
    print("➡️ 『シラバス参照』をクリックします（JS実行）...")
    syllabus_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "menu-link-mf-118081"))
    )
    driver.execute_script("arguments[0].click();", syllabus_link)
    print("✅ 『シラバス参照』クリック完了（JS実行）")
except Exception as e:
    print("❌ 『シラバス参照』クリックに失敗:", e)
    driver.save_screenshot("error_screenshot.png")
    driver.quit()
    exit()

# 「検索開始」ボタンクリック
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@value=' 検索開始 ']"))
).click()
print("🔍 検索開始ボタンをクリック")

# 科目名リンクをクリック（例として最初のリンクを選択）
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick^='refer']"))
).click()
print("📄 科目リンクをクリック → 詳細ページへ")

# ページ読み込み待機
time.sleep(2)

# BeautifulSoupで詳細情報を取得
soup = BeautifulSoup(driver.page_source, "html.parser")

def get_value_by_label(label_text):
    th = soup.find("th", string=lambda text: text and label_text in text)
    if th:
        td = th.find_next_sibling("td")
        if td:
            return td.get_text(separator="\n", strip=True).replace('\xa0', ' ')
    return ""

# 欲しい項目ラベル一覧
labels = [
    "科目分類", "開講年次", "時間割コード", "開講区分", "開講科目名",
    "曜日・時限等", "成績入力担当", "単位数", "授業形態", "ナンバリングコード",
    "授業のテーマ", "授業の到達目標", "授業の概要と計画", "成績評価方法",
    "成績評価基準", "履修上の注意", "事前・事後学修", "オフィスアワー・連絡先",
    "学生へのメッセージ", "今年度の工夫", "教科書", "参考書・参考資料等",
    "授業における使用言語", "キーワード", "参考URL"
]

# 出力
print("\n📋 シラバス詳細情報：\n")
for label in labels:
    value = get_value_by_label(label)
    print(f"■ {label}:\n{value}\n")

driver.quit()