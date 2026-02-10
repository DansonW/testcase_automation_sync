# SuperDSP CCT (Cross-Channel Targeting) 規格與情境全地圖

此文件旨在彙整 PDF 規格書 (`20250919_CCT.pdf`, `20250926_CCT.pdf`) 中提及的所有關鍵權限、功能點及測試情境，作為測試覆蓋率的驗證基準。

## 1. 權限角色矩陣 (Permission Matrix)
根據規格定義，系統需支持以下角色及其對應的 CCT 操作範圍：

| 角色名稱 | 存取範圍 | 核心職責與限制 |
|---|---|---|
| **OneAD User (Internal OP/PM)** | 全系統 (Global) | 跨廣告主/品牌的全局維護、排除故障、系統級設定。 |
| **Media Admin** | 所屬媒體 (Media) | 管理該媒體下所有廣告主與品牌的 Pixel 資產。 |
| **Agency Admin / User** | 授權代理商品牌 | 同時管理多個授權品牌的 Pixel，具備跨品牌維護能力。 |
| **Client Admin** | 所屬廣告主 (Advertiser) | 管理該廣告主下屬所有品牌的 Pixel 設定。 |
| **Brand Admin** | 單一品牌 (Brand) | 該品牌資產的最高管理者，具備完整的 CRUD 權限。 |
| **Brand User** | 單一品牌 (Brand) | 僅限觀察或基本操作，通常禁止刪除或變更敏感設定。 |
| **Ad Operator** | 授權品牌 | 執行 Insertion Order 與 Ad Group 的日常維護，套用 CCT。 |
| **Readonly User** | 授權視角 | 僅能檢視 Pixel 列表與詳情，所有變更按鈕應隱藏。 |

## 2. 核心功能模組 (Feature Blocks)
### A. Cross Channel Pixel 管理專區
- **列表檢視 (Listing)**：支援按品牌、渠道、建立時間排序與篩選。
- **建立/編輯 (Create/Edit)**：
  - **Channel 選擇**：支援 Meta, LINE, Google Ads 等。
  - **ID 格式校驗**：針對不同渠道 ID 進行格式格式檢查。
  - **Advertising Category & Format**：動態過濾相應的追蹤格式。
  - **Trigger Event**：根據渠道與格式連動顯示事件選項。
- **刪除安全性**：偵測 Pixel 是否被 Ad Group 使用。

### B. 廣告組合 (Ad Group) 整合
- **CCT 主開關**：控制該廣告組合是否啟用跨渠道追蹤。
- **Pixel 選取器**：支援多選，以 Tag / Badge 形式呈現，具備動態搜尋與過濾。
- **規格校驗**：檢查所選 Pixel 是否符合該廣告組合的 Category 限制。

## 3. 測試情境分類 (Scenario Taxonomy)
### 權限與隔離性 (Security)
- [ ] 跨品牌 URL ID 篡改存取測試。
- [ ] 不同角色對應 UI 按鈕（Create/Delete）的顯隱驗證。
- [ ] 代理商端多品牌切換與資料隔離驗證。

### 功能與資料完整性 (Functional)
- [ ] 渠道 (Channel) 與事件 (Event) 的動態連動選單檢查。
- [ ] Pixel Name 名稱重複衝突（同一品牌內）驗證。
- [ ] Pixel Name 超長字串與特殊字元（XSS）防護驗證。
- [ ] 已套用 Pixel 的刪除鎖定保護。

### 系統整合與一致性 (Integration)
- [ ] Ad Group 草稿與正式上刊階段的 CCT 設定同步性。
- [ ] 多像素 (Multiple Pixels) 套用上限與 UI 展示（折行處理）。
- [ ] 後端數據與 UI 狀態（Active/Inactive）的即時同步。

### UI/UX 體驗與健壯性 (User Experience)
- [ ] 非同步載入 (Async Loading) 的骨架屏或 Loading 標誌。
- [ ] API 報錯 (Network Error / 500) 時的 UI 提示與資料備存。
- [ ] 中英對照語法精準度與 Placeholder 引導文字一致性。
- [ ] 響應式佈局 (Responsive Design) 在各螢幕解析度下的兼容性。
- [ ] Status 狀態的視覺警告 (Hover Tooltip) 引導。

---
*註：此地圖將隨規格更新持續迭代，確保所有測試案例均能回溯至此對應點。*
