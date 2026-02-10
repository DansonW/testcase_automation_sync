# Testcase Automation

本專案旨在透過 **Gemini CLI** 實現廣告系統（SuperDSP, OYM, ERP/OSS）測試案例的自動化產出。透過預設的 **GEMINI_SOP.md**，能將資深測試與 UI/UX 工程師的思維邏輯轉化為精確、可驗證的測試案例。

---

## 📋 專案概覽 (Project Overview)

*   **核心目標**: 將規格文件（PDF/圖片）自動轉化為結構化的 CSV 測試案例，提升測試覆蓋率與效率。
*   **技術基礎**: 利用 Google Gemini CLI 的模型理解能力，結合自定義的系統操作規則。
*   **專業定位**: 結合「資深軟體測試工程師」與「資深 UI/UX 工程師」雙重專業視角。

## 📁 目錄結構 (Directory Structure)

```text
/
├── README.md                # 專案說明文件與快速上手指南
├── GEMINI_SOP.md            # 核心 SOP，定義產出規則、欄位與角色邏輯
├── generated_test_cases/     # 自動產出的專業測試案例 (CSV 格式)
│   └── [來源專案名稱]/       # 依專案來源自動分類存放
├── source_files/             # 原始規格文件參考 (PDF, PNG, CSV 等)
└── .gemini/                  # Gemini CLI 配置與指令集
```

## 🚀 快速上手 (Quick Start)

只需簡單四個步驟，即可開始自動化產出專業的測試案例：

### 1. 安裝環境 (Environment Setup)
在終端機視窗中執行以下指令，從 NPM 註冊表下載並安裝 Gemini CLI：
```bash
npm install -g @google/gemini-cli
```

### 2. 啟動專案 (Initialization)
切換到您的專案路徑，並在終端機視窗中執行 CLI：
```bash
gemini
```

### 3. 自動化產生 (Automation Step)
在互動介面中，引用 SOP 規範並指定您的需求：
> **範例指令：**
> 「@GEMINI_SOP.md 產出 Superdsp phase XXX 的 test case」

### 4. 驗收成果 (Review Results)
產出的 CSV 檔案將會自動儲存在以下路徑：
```
generated_test_cases/[來源資料夾名稱]/[來源]_test_case_[時間戳記].csv
```

## ⚙️ 產出規範 (Production Standards)

所有產出的測試案例均嚴謹包含以下欄位內容：

| 欄位名稱 | 說明 | 範例 |
| :--- | :--- | :--- |
| **系統** | 測試案例所屬的子系統 | `SuperDSP` |
| **權限** | 執行測試所需的使用者角色 | `Media Admin` |
| **功能 / 頁面** | 測試案例針對的具體位置 | `RTB 底價設定` |
| **測試功能** | 格式為 `【標籤】功能名稱` | `【正向】更新底價` |
| **測試情境** | 描述具體的使用者場景與意圖 | `媒體管理者成功設定並更新底價` |
| **操作步驟** | 詳細、可重複執行的步驟 | `1. 登入... 2. 進入...` |
| **期望結果** | 條列化的可驗證結果 | `1. 系統提示儲存成功...` |
| **備註** | 記錄原始規格主文件名稱 | `主文件：ITO-[Commerce AD]...pdf` |

---

## 🛠 維護與更新 (Maintenance)

*   **更新 SOP**: 若需修改產出邏輯，請直接調整 `GEMINI_SOP.md` 並告知 Gemini CLI。
*   **同步 Github**: 每次產出重要更新後，請務必 Commit 並 Push 到此 Github 以利共用。

---
*Created and maintained by wangdanson.*