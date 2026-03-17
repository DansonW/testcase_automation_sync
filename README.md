# Testcase Automation

本專案旨在透過 **Gemini CLI** 實現廣告系統（SuperDSP, OYM, ERP/OSS）測試案例的自動化產出。透過預設的 **GEMINI_SOP.md**，能將資深測試與 UI/UX 工程師的思維邏輯轉化為精確、可驗證的測試案例。

---

## 📋 專案概覽 (Project Overview)

*   **核心目標**: 將規格文件（PDF/圖片）自動轉化為結構化的 CSV 測試案例，提升測試覆蓋率與效率。
*   **技術基礎**: 利用 Google Gemini CLI 的模型理解能力，結合自定義的系統操作規則。
*   **專業定位**: 結合「資深軟體測試工程師」與「資深 UI/UX 工程師」雙重專業視視角。
*   **自動化流程**: 產出測試案例後，自動分類儲存至本地目錄，並同步上傳至 Google Sheets。

## 📁 目錄結構 (Directory Structure)

```text
/
├── README.md                # 專案說明文件與快速上手指南
├── requirements.txt         # Python 環境相依套件清單 (pandas, google-api-python-client 等)
├── package.json             # 專案配置文件，包含一鍵安裝指令 (npm run setup)
├── GEMINI_SOP.md            # [已存檔] 歷史 SOP，內容已轉移至 Skill 檔案
├── GEMINI_ERROR_LOG.md      # 邏輯錯誤與 test case 產出錯誤紀錄，用於避免重複出錯
├── .env                     # [資安] 環境變數設定檔 (已列入 .gitignore)
├── .env.example             # 環境變數設定範例
├── upload_to_sheets.py      # 自動化腳本：將產出的 CSV 上傳至 Google Sheets
├── sync_from_sheets.py      # [新增] 反向同步腳本：將雲端變更同步回本地 CSV
├── service_account/         # [資安] 存放 Google 服務帳號憑證 (已列入 .gitignore)
│   └── google_credentials.json # Google 服務帳號憑證金鑰
├── source_files/            # 原始規格文件參考
│   ├── [專案名稱]/           # 存放該專案相關的 PDF, PNG, CSV 等規格文件
│   ├── HTML/                # 存放系統 HTML 檔案 (供分析 UI 結構使用)
│   └── user_manual/         # [核心] 各系統操作手冊、架構與 UI 流程
│       ├── ODM/             # OneAD Delivery Manager 相關文件
│       ├── OSS/             # (待新增) ERP/OSS 相關文件
│       └── SuperDSP/        # (待新增) SuperDSP 相關文件
├── generated_test_cases/    # 產出的測試案例儲存區
│   └── [專案名稱]/           # 依來源專案分類存放產出的 CSV 檔案
└── .gemini/                 # Gemini CLI 配置資料夾
    └── skills/              # 存放核心 SOP 與專家技能 (如 test-case-automation-expert)
```


## 🚀 快速上手 (Quick Start)

### 0. 複製專案 (Clone Project)
首先，將此專案複製到您的本地電腦：
```bash
git clone https://github.com/wangdanson/testcase_automation.git
cd testcase_automation
```

### 1. 安裝環境 (Environment Setup)

在開始使用前，請確保您的開發環境已安裝基礎組件 (Node.js 與 Python)，然後執行一鍵安裝指令。

#### A. 系統基礎環境 (System Prerequisites)
*   **Node.js**: 建議版本 v18.0.0 以上 ([下載連結](https://nodejs.org/))。
*   **Python**: 建議版本 v3.9 以上 ([下載連結](https://www.python.org/))。

#### B. 一鍵安裝所有套件 (Quick Setup)
在專案根目錄執行以下指令，系統將自動安裝 **Gemini CLI** (Node.js 套件) 與 **Python 相依套件**：
```bash
npm run setup
```
*(此指令會執行：`npm install -g @google/gemini-cli` 以及 `pip install -r requirements.txt`)*

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

#### C. 設定環境變數
1.  將 `.env.example` 複製為 `.env`。
2.  填入您的 `SPREADSHEET_ID`（網址中 `/d/` 後方的一串字元）。
3.  **確認資安**: `.env` 與 `service_account/` 已被加入 `.gitignore`，機密資訊不會被上傳。


### 3. 自動化產生測試案例 (Automation Workflow)

啟動 Gemini CLI 並下達指令：
```bash
gemini
```

**範例指令：**
> 「幫我產生 [來源資料夾名稱] 的 test case」

**Gemini 將自動執行以下流程：**
1.  **分析**：讀取 `source_files/[來源資料夾名稱]` 下的規格文件與 `GEMINI_ERROR_LOG.md`。
2.  **建立目錄**：在 `generated_test_cases/` 下建立一個與來源同名的子目錄。
3.  **產出與備份**：生成帶有時間戳記的 CSV 檔案，並將其儲存至該子目錄中。
4.  **同步上傳**：自動呼叫 `upload_to_sheets.py` 將該 CSV 檔案同步上傳至 Google Sheets，並在試算表中建立同名的工作表。

### 🔄 4. 反向同步 (Reverse Sync)

若您在 **Google Sheets** 上直接修改了測試案例內容，並希望將這些變更更新回本地端的 CSV 檔案，可以使用反向同步功能。

**與 Gemini CLI 對話的快速指令：**
您可以直接在對話框中對我下達以下指令，我會自動為您執行同步腳本：

1.  **指定專案名稱**：
    > 「Sync [專案名稱]」
    > *(例如：`Sync Phase 2`，我會自動去 `generated_test_cases` 下找對應的最新檔案執行。)*

2.  **直接貼上檔案路徑或檔名**：
    > 「同步這個檔案：[檔名].csv」

3.  **針對剛產出的檔案**：
    > 「同步剛剛產出的 test case」

---

**手動執行腳本指令：**
若需手動執行，請在終端機輸入：
```bash
python3 sync_from_sheets.py "generated_test_cases/[專案路徑]/[檔名].csv"
```

**功能特色：**
*   **自動匹配**：腳本會根據 CSV 檔名自動尋找 Google Sheets 中同名的工作表。
*   **完整覆蓋**：從雲端抓取最新資料並覆蓋本地 CSV。
*   **格式保證**：維持 `utf-8-sig` 編碼與 CSV 引用規範，確保 Excel 開啟不亂碼。

---

## ⚙️ 產出規範 (Production Standards)

| 欄位名稱 | 說明 | 範例內容 |
| :--- | :--- | :--- |
| **系統** | 測試案例所屬系統 (SuperDSP, OYM, ERP/OSS) | `SuperDSP` |
| **權限** | 執行測試所需的使用者權限 | `Media Admin` |
| **功能 / 頁面** | 測試案例針對的具體功能 (不含系統前綴) | `RTB 底價設定` |
| **測試功能** | 格式：`【標籤】功能名稱` (遵循標籤排序規則) | `【正向】更新底價` |
| **測試情境** | 描述具體的使用者場景或意圖 | `媒體管理者成功設定並更新底價` |
| **操作步驟** | 詳細步驟 (使用實際換行，並以雙引號包裹) | `"1. 登入... 2. 進入..."` |
| **期望結果** | 條列化預期結果 (使用實際換行，並以雙引號包裹) | `"1. 系統提示成功... 2. 數據更新"` |
| **備註** | 僅記錄參考之原始規格主文件名稱 | `主文件：ITO-[Commerce AD]...pdf` |

---

## 🛠 維護與持續改進 (Maintenance)

*   **預防犯錯**：每次產出前，Gemini 會檢閱 `GEMINI_ERROR_LOG.md` 以避免重複邏輯錯誤（如：特定帳號權限、狀態鎖定等）。
*   **資安防護**：嚴禁硬編碼 API Key 或 ID。`.env` 與 `service_account/` 目錄已列入 `.gitignore` 以確保安全性。
*   **資料完整性**：CSV 產出時所有欄位強制加上雙引號包裹，確保 Google Sheets 匯入時排版精確。

---
*Created and maintained by wangdanson.*
