
import re
import csv
import os
import datetime
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=False) # Keep headless=False for now for debugging
    context = browser.new_context()
    page = context.new_page()

    base_url = "https://staging-oss.onead.tw/users/sign_in" # Updated base_url
    username = "dansonwang@onead.com.tw" # Using the email from the payload
    password = "Gsp123456" # Using the password from the payload

    test_results = []

    try:
        # --- UI Login ---
        print("--- 執行 UI 登入 ---")
        page.goto(base_url)
        page.fill("input[placeholder='Email Address']", username)
        page.fill("input[placeholder='Password']", password)
        page.click("input#submit", force=True) # Use the precise selector for the login button
        page.wait_for_timeout(5000) # Give some time for login to process
        page.wait_for_selector("text=媒體管理", timeout=30000) # Wait for a dashboard element to appear
        print("登入成功！")

        # --- Test Case 1: 【權限】建立 RTB 合約 ---
        # PAD 人員具有建立 RTB 浮動價格合約的權限
        print("\n--- 執行測試案例: 【權限】建立 RTB 合約 ---")
        # 1. 進入媒體管理頁面，選擇一個媒體
        page.click("text=媒體管理") # Click on "媒體管理" navigation item
        page.click("text=媒體列表") # Click on "媒體列表" sub-item

        # 2. 點擊「新增合約(RTB)」按鈕
        page.click("text=新增合約(RTB)") # Click on "新增合約(RTB)" button

        # 期望結果 1: 系統應顯示「新增合約(RTB)」按鈕 (already checked by clicking it)
        # 期望結果 2: 點擊按鈕後，系統應能成功開啟合約建立表單
        page.wait_for_selector(".contract-form-modal", state='visible') # Placeholder for contract form modal
        print("期望結果 2: 點擊按鈕後，系統應能成功開啟合約建立表單 - 通過")

        test_results.append(["【權限】建立 RTB 合約", "通過"])

    except Exception as e:
        print(f"--- 執行失敗 ---")
        print(f"腳本執行時發生錯誤：{e}")
        screenshot_path = f"oss_pad_user_api_login_test_error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        print(f"已將當前頁面截圖儲存至：{screenshot_path}")
        test_results.append(["【權限】建立 RTB 合約", "失敗", str(e)])

    finally:
        browser.close()

    # Save test results to a CSV file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "/Users/danson/testcase/generated_test_cases/Superdsp phase 1.7.0 (commerce ad phase 3)/"
    output_filename_prefix = "Superdsp_phase_1.7.0_(commerce_ad_phase_3)_oss_pad_user_api_login_test_results"

    # Get existing reports
    existing_reports = [f for f in os.listdir(output_dir) if f.startswith(output_filename_prefix) and f.endswith(".csv")]
    existing_reports.sort() # Sort to get the oldest

    # Determine filename for the new report
    if len(existing_reports) >= 2:
        # Overwrite the oldest report
        oldest_report_path = os.path.join(output_dir, existing_reports[0])
        os.remove(oldest_report_path)
        print(f"已覆蓋最舊的測試報告：{oldest_report_path}")
        report_filename = os.path.join(output_dir, f"{output_filename_prefix}_{timestamp}.csv")
    else:
        # Create a new report
        report_filename = os.path.join(output_dir, f"{output_filename_prefix}_{timestamp}.csv")

    with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["測試功能", "結果", "錯誤詳情"])
        csv_writer.writerows(test_results)
    print(f"\n測試結果已儲存至：{report_filename}")

with sync_playwright() as playwright:
    run(playwright)
