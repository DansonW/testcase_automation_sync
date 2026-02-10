# Testcase Automation

這是一個專門用於存放廣告系統（如 SuperDSP, OYM, ERP/OSS）測試案例自動化邏輯與 SOP 的 Github。透過此 Github，您可以將測試專家的思維與生成規則快速同步到 Gemini CLI 中，實現自動化測試案例產出。

## 📁 目錄結構說明

*   `generated_test_cases/`: 存放由 Gemini CLI 根據規格文件自動產出的 CSV 測試案例。
*   `source_files/`: 原始規格文件（PDF/圖片）的參考來源。
*   `GEMINI_SOP.md`: 核心 SOP 文件，定義了測試案例的產出規則、欄位格式與角色定位。
*   `.gemini/`: 包含指令集與長期記憶配置。

## 🚀 快速上手指南

只需簡單四個步驟，即可開始自動化產出專業的測試案例：

### 第一步：安裝 Gemini CLI
請確保您的環境已安裝 Node.js，然後在終端機執行以下指令進行安裝：
'''bash
npm install -g @google/gemini-cli
'''

### 第二步：在專案資料夾中啟動
切換到您的專案路徑（例如 `testcase` 資料夾），直接輸入指令啟動：
'''bash
gemini
'''

### 第三步：指令產生測試案例
在 Gemini CLI 視窗中，利用 `@` 符號引用 `GEMINI_SOP.md` 作為規範，並指定來源文件。
**範例指令：**
> 「請參考 `source_files/PDF/SuperDSP_Pilot.pdf` 產出測試案例 @GEMINI_SOP.md 」

### 第四步：檢視產出結果
產出完成後，您可以在指定路徑下看到產出的 CSV 檔案。
**存放路徑：**
`generated_test_cases/[來源資料夾名稱]/[來源]_test_case_[時間戳記].csv`

---

## 🛠 產出欄位名稱內容

本專案產出的測試案例嚴謹遵循以下欄位結構：

*   **系統**: 測試案例所屬的系統 (e.g. SuperDSP, OYM, ERP/OSS)
*   **權限**: 執行測試所需的使用者具體角色 (e.g. Media Admin, Onead User)
*   **功能 / 頁面**: 測試案例針對的具體功能或頁面名稱
*   **測試功能**: 採 `【標籤】功能名稱` 格式 (e.g. 【正向】使用者登入)
*   **測試情境**: 描述測試的具體場景或使用者意圖
*   **操作步驟**: 執行測試的詳細條列步驟
*   **期望結果**: 測試預期的可驗證結果（條列化顯示）
*   **備註**: 記錄該案例參考的原始規格主文件名稱

---
*Created and maintained by wangdanson.*