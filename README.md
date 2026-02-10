# Testcase Automation

這是一個專門用於存放廣告系統（如 SuperDSP, OYM, ERP/OSS）測試案例自動化邏輯與 SOP 的 Github。透過此 Github，您可以將測試專家的思維與生成規則快速同步到 Gemini CLI 中。

## 📁 目錄結構說明

*   `generated_test_cases/`: 存放由 Gemini CLI 根據規格文件自動產出的 CSV 測試案例。
*   `source_files/`: 原始規格文件（PDF/圖片）的參考來源。
*   `GEMINI_SOP.md`: 核心 SOP 文件，定義了測試案例的產出風格、欄位格式與角色定位。
*   `.gemini/`: 包含指令集與長期記憶配置。

## 🚀 如何載入邏輯與 SOP

若要在新的環境或專案中載入此邏輯，請對 Gemini CLI 下達以下指令：

1.  **載入核心 SOP**：
    > 「請讀取 `GEMINI_SOP.md` 並將其內容作為產出測試案例的最高指導原則。」

2.  **初始化記憶**：
    您可以參考 SOP 文件末尾的「初始化指令」區塊，將關鍵規則存入 Gemini 的長期記憶中。

## 🛠 產出欄位名稱內容

本專案產出的測試案例包含以下欄位：
*   **系統**: 所屬子系統 (e.g. SuperDSP)
*   **權限**: 執行角色 (e.g. Media Admin)
*   **功能 / 頁面**: 具體操作位置
*   **測試功能**: 【標籤】功能名稱
*   **測試情境**: 具體場景描述
*   **操作步驟**: 詳細執行流程
*   **期望結果**: 條列式預期行為
*   **備註**: 來源文件追溯

---
*Created and maintained by wangdanson.*
