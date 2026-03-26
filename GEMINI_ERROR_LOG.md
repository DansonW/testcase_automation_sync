# Gemini CLI 錯誤學習紀錄 (Error Log)

> **自動化守門員狀態**: ✅ **Active** (`validate_csv.py`)
> 此檔案紀錄歷史錯誤與修正邏輯，用於產出前的自我預檢 (Self-Correction)。

## 1. 🛑 [Critical] 系統邏輯與權限 (Logic & Permissions)
> **影響層級**：高。違反此類規則將導致功能無法運作、權限漏洞或嚴重業務邏輯錯誤。

| 模組 (Module) | 規則描述 (Rule Description) | 避坑指南 (Guideline) | 來源/案例 |
|---|---|---|---|
| **Identity** | **果實夥伴 (Agency ID 571) 專屬功能邊界** | 本階段 (Pilot for AOE) 所有進階功能**僅限**於此 Agency 下的關聯帳號：<br>1. **[Campaign] 產業類別 (OneAd Category)**：僅此 Agency 可見並**必填**。其他 Agency **不可見**。<br>2. **[Ad Group] 進階投放設定**：<br>   * **廣告格式 (Ad Format)**：僅此 Agency 可進行格式選擇與切換 (ITP-2911)。<br>   * **黑白名單 (Black/White List)**：僅此 Agency 可設定 (ITP-2907)。<br>   * **時段/地區 (Hours/Cities)**：僅此 Agency 使用新版參數。<br>3. **[Material] 免審核流程**：僅此 Agency 上傳素材包後**自動通過 (Passed)**，且**不需**設定「OneAD 廣告類別」。 | ITP-2902<br>ITP-2904<br>ITP-2907<br>ITP-2911 |
| **Campaign** | **生命週期狀態鎖定** | 廣告活動一旦進入「上刊/執行中 (Active)」狀態，關鍵欄位（如產業類別、版位、走期起始日）必須轉為**唯讀 (Read-only)**，不可編輯。 | ITP-2904 |
| **Budget** | **超跑顯示與預算回收 (Pilot 1 核心邏輯)** | 1. **花費上限移除**：移除「花費不可超過預算」限制，UI 需顯示實際投放金額 (ITP-2877)。<br>2. **狀態釋放邏輯**：除 `CLOSED` 外，廣告群組為 `ABORTED` 狀態時也必須釋放剩餘預算回 Campaign (ITP-2921)。 | ITP-2877<br>ITP-2921 |
| **Admin** | **權限自動連動** | Admin 建立新廣告主帳號時，應**自動加入**對應權限，而非依賴手動配置。 | Phase 1.3.2 |
| **Integration** | **跨系統狀態同步** | 在 SuperDSP 免審核通過的素材，於 ODM/OSS 系統中必須自動標記為「審核通過」，不需人工介入。 | System Integration |

## 2. ⚠️ [Major] 資料整合與 UI 連動 (Integration & UX)
> **影響層級**：中。違反此類規則將導致資料不一致、操作流程中斷或使用者困惑。

| 模組 (Module) | 規則描述 (Rule Description) | 避坑指南 (Guideline) | 來源/案例 |
|---|---|---|---|
| **AdGroup** | **欄位連動清空** | 當上層欄位（如：廣告格式）變更時，相依的下層欄位（如：指定素材包）必須**自動清空**，防止資料格式不匹配。 | Phase 1.0.1 |
| **Report** | **Pilot 1 報表命名與格式** | 1. **Sheet 命名**：廣告組合分頁改為 `Ad Group + ${id}` (如 `Ad Group 12345`)。<br>2. **欄位移除**：移除 `pricing_unit`、`average_price`、`average_freq` 等冗餘欄位。<br>3. **數值格式**：確保金額與數量在 Excel 中為「數值」格式，支援自動加總 (ITP-2881)。 | ITP-2881 |
| **Audience** | **受眾洞察報告匯出限制放寬** | 開放廣告開始「當天 (D+0)」即可進行數據查詢與匯出，並移除「數據截取至昨天」的提示 (ITP-2882)。 | ITP-2882 |
| **Common** | **選擇邏輯明確化** | 必須釐清選擇器行為是「單選替換 (Replace)」還是「多選累加 (Append)」。 | UX Rule |
| **Search** | **搜尋防呆機制** | 搜尋框輸入無效字元 (如 `!@#$`) 時，應顯示「找不到資料」提示，並提供「清除條件 (X)」按鈕。 | Test 1 |
| **L10n** | **繁中語系標籤修正** | 修正「姓氏」與「名字」標籤顯示顛倒的問題，確保 `lastName` 對應姓，`firstName` 對應名。 | Pilot Phase 1 |

## 3. 🎨 [Style] 格式與排版 (Formatting & Syntax)
> **影響層級**：低。影響閱讀體驗或自動化解析。
> **注意**：標記為 ✅ 的項目已由 `validate_csv.py` 強制執行。

| 項目 | 規則描述 | 自動驗證 | 修正方案 |
|---|---|---|---|
| **CSV** | **實體換行 (Actual Line Breaks)**<br>嚴禁使用字面上的 `\n` 或 HTML `<br>`。必須使用雙引號包裹的實體換行。 | ✅ Yes | 產出時直接按 Enter 換行，並確保被雙引號包裹。 |
| **CSV** | **雙引號包裹 (Full Quoting)**<br>所有欄位內容建議使用雙引號包裹，防止特殊字元導致跑版。 | ⚠️ Partial | `csv` 模組通常會自動處理，但需注意原始字串中不要手動添加 `\"`。 |
| **Content** | **結尾無句號**<br>在 `測試情境`、`操作步驟`、`期望結果` 的行末不需加上句號 `。`。 | ✅ Yes | Regex 檢查行末 `。` 並移除。 |
| **Syntax** | **引號清理**<br>內容中不應包含多餘的轉義引號 (如 `\"`)。 | ✅ Yes | 使用標準 CSV 格式 `""` 代表引號，而非反斜線。 |

---

### 📝 歷史修正日誌 (Revision History)
*   **2026-03-20**: 引入 `validate_csv.py` 自動化驗證，將格式錯誤降級為 Style，並結構化 Error Log。
*   **2026-03-18**: 修正 CSV 跑版問題，強制規範實體換行與雙引號。
