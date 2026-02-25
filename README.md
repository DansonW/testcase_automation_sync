# Testcase Automation

本專案旨在透過 **Gemini CLI** 實現廣告系統（SuperDSP, OYM, ERP/OSS）測試案例的自動化產出。透過預設的 **GEMINI_SOP.md**，能將資深測試與 UI/UX 工程師的思維邏輯轉化為精確、可驗證的測試案例。

---

## 📋 專案概覽 (Project Overview)

*   **核心目標**: 將規格文件（PDF/圖片）自動轉化為結構化的 CSV 測試案例，提升測試覆蓋率與效率。
*   **技術基礎**: 利用 Google Gemini CLI 的模型理解能力，結合自定義的系統操作規則。
*   **專業定位**: 結合「資深軟體測試工程師」與「資深 UI/UX 工程師」雙重專業視視角。

## 📁 目錄結構 (Directory Structure)

```text
/
├── README.md                # 專案說明文件與快速上手指南
├── GEMINI_SOP.md            # 核心 SOP，定義產出規則、欄位與角色邏輯
├── GEMINI_ERROR_LOG.md      # 紀錄邏輯錯誤及 test case 產出錯誤紀錄，以避免重複出錯
├── .env                     # [資安] 環境變數設定檔 (已列入 .gitignore)
├── .env.example             # 環境變數設定範例
├── upload_to_sheets.py      # 自動化腳本：將產出的 CSV 上傳至 Google Sheets
├── generated_test_cases/     # 存放自動產出的專業測試案例 (CSV 格式)
│   └── [專案名稱]/           # 依專案來源自動分類存放
├── service_account/         # [資安] 存放服務帳號及憑證資訊 (已列入 .gitignore)
│   └── google_credentials.json # google 服務帳號憑證
├── source_files/             # 原始規格文件參考
│   ├── [專案名稱]/           # 存放該專案相關的 PDF, PNG, CSV 等規格文件
│   └── HTML/                 # 存放測試系統的 HTML 檔案 (供分析頁面結構使用)
└── .gemini/                  # Gemini CLI 配置與指令集
```

## 🚀 快速上手 (Quick Start)

### 0. 複製專案 (Clone Project)
首先，將此專案複製到您的本地電腦：
```bash
git clone https://github.com/wangdanson/testcase_automation.git
cd testcase_automation
```

### 1. 安裝環境 (Environment Setup)
1.  **安裝 Gemini CLI**:
    ```bash
    npm install -g @google/gemini-cli
    ```
2.  **安裝 Python 依賴**:
    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

### 2. 安全性設置 (Security Setup)
本專案採用機密資訊分離原則，請依照以下步驟配置：

#### A. 獲取 Google 服務帳號金鑰 (JSON)
根據 Google Drive API 標準設定流程，請執行以下步驟：

1.  **建立新專案**: 登入 [Google Cloud Console](https://console.cloud.google.com/)，點選「選取專案」並選擇「新增專案」，為專案命名後點擊「建立」。
2.  **啟用 Google Drive API**: 在左側選單點擊「API 和服務」>「啟用 API 和服務」。搜尋「**Google Drive API**」並將其啟用。
3.  **前往憑證頁面**: 在左側選單選擇「API 和服務」>「憑證」。
4.  **建立服務帳號**: 點擊「建立憑證」> 選擇「**服務帳戶**」。
5.  **設定服務帳號詳細資訊**: 輸入服務帳號名稱、ID 與描述，點擊「建立並繼續」。
6.  **授予服務帳號權限**: 選擇角色（建議選取「基本」>「**編輯者**」），完成後點擊「繼續」與「完成」。
7.  **產生並下載 JSON 金鑰**: 
    *   在服務帳戶列表中點擊該帳戶的 Email。
    *   切換至「**金鑰 (Keys)**」頁籤。
    *   點擊「新增金鑰」>「建立新的金鑰」> 選擇「**JSON**」並建立。
    *   系統會自動下載 JSON 檔案，請將其重新命名為 `google_credentials.json` 並放入 `service_account/` 資料夾。

#### B. 共享試算表權限 (關鍵步驟)
1.  **複製服務帳戶 Email**: 格式如 `account-name@project-id.iam.gserviceaccount.com`。
2.  **授予編輯權限**: 開啟目標 Google 試算表，點擊「**共用**」，將該 Email 加入並設為「**編輯者**」。

* 配置環境變數
1.  **配置環境變數**: 將 `.env.example` 複製為 `.env`，並填入您的 `SPREADSHEET_ID`（網址中 `/d/` 後方的一串字元）。
2.  **確認資安**: `.env` 與 `service_account/` 已被加入 `.gitignore`，機密資訊不會被上傳。

### 3. 啟動專案 (Initialization)
切換到專案路徑，並啟動 Gemini CLI：
```bash
gemini
```

### 4. 準備規格文件 (Preparation)
在 `source_files/` 下建立專案資料夾，並放入 PDF、圖片或需求 CSV。

### 5. 自動化產生與上傳 (Automation Step)
在互動介面中，引用 SOP 規範並指定需求。產出後會自動執行 `upload_to_sheets.py` 並將產出的 test case 上傳至指定的 google sheet 中。
> **範例指令：**
> 「@GEMINI_SOP.md 產出 SuperDSP Pilot for AOE (Phase 1) 的 test case」

---

## ⚙️ 產出規範 (Production Standards)

所有產出的測試案例均嚴謹包含以下欄位內容：

| 欄位名稱 | 說明 | 範例 |
| :--- | :--- | :--- |
| **系統** | 測試案例所屬的子系統 | `SuperDSP` |
| **權限** | 執行測試所需的使用者角色 | `Media Admin` |
| **功能 / 頁面** | 測試案例針對的具體位置 | `RTB 底價設定` |
| **測試功能** | 格式為 `【標籤】功能名稱` | `【正向】更新底價` |
| **測試情境** | 描述具體的使用者場景與意圖 | `媒體管理者成功設定並更新底價` |
| **操作步驟** | 條列化詳細步驟 (包裹雙引號以防跑版) | `"1. 登入... 2. 進入..."` |
| **期望結果** | 條列化可驗證結果 (包裹雙引號以防跑版) | `"1. 系統提示儲存成功..."` |
| **備註** | 記錄原始規格主文件名稱 | `主文件：ITO-[Commerce AD]...pdf` |

---

## 🛠 維護與更新 (Maintenance)

*   **邏輯錯誤紀錄**: 發現邏輯偏差時，應更新 `GEMINI_ERROR_LOG.md`，Gemini CLI 產出前會優先檢閱。
*   **資安守則**: 嚴禁在程式碼中硬編碼任何 Key 或 ID，所有配置應透過環境變數管理。
*   **格式保證**: CSV 產出時所有欄位必須加上雙引號包裹，確保 Google Sheets 匯入時不跑版。

---
*Created and maintained by wangdanson.*
