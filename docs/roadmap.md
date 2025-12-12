# 🔥 **【最新版】アジャイル風 × MVP反復 × モダンUI × domain/ モデル設計付き**

---

# 🟦 **スプリント1：domain モデル × データ設計 × バックエンド基盤**

> **アプリの“脳みそ”を作る最重要フェーズ。
> UI は一切やらず、内部ロジックと型を固める。**

## 🧩 ① domain/ モデル設計（★新規追加／最初にやる）

### 🔷 TypedDict（データの構造定義）

- `FoodItem`（食品のP/F/C/価格）

- `ProteinItem`（1日の摂取量・袋の総重量など）

- `PhaseSetting`（bulk/cutのPFC比率）

- その他必要に応じて追加


### 🔷 TypeAlias（意味のある型名にする）

- `Gram = float`

- `KCAL = float`

- `Price = int`

- `Ratio = float`

- `UserID = str`（必要なら）


### 🔷 Enum（ビジネスルールの定数）

- `PhaseEnum = BULK | CUT`


### 🔷 Literal（高精度な固定値の制約）

- `phase: Literal["bulk", "cut"]`

- `unit: Literal["g", "kg"]`（必要なら）


---

## 🧩 ② 固定DBの設計（JSON）

- `foods.json`

- `proteins.json`

- `phase.json`


（domain/ の TypedDict と構造を一致させる）

---

## 🧩 ③ 計算ロジック（services）

- PFC 計算（1食の合計）

- 価格計算

- 月食費計算

- プロテイン消費サイクル

- Phase 補正ロジック


---

## 🧩 ④ バリデーション（validators）

- 食材の存在チェック

- GramやPriceの型/値チェック

- Phaseの正当性チェック


---

## 🧩 ⑤ Config（dataclass）＋ dotenv

- `.env` 読み込み

- APIキー・環境設定など


---

## 🧩 ⑥ テスト（バックエンド）

- TypedDict 形式での入出力保証

- 各 service が正しい値を返すか

- 計算ロジックの境界値テスト


---

## 🎯 **スプリント1成果物（MVP基盤）**

- 完成された domain モデル（型 × Enum × Alias）

- 固定DB

- services（計算と補正の全ロジック）

- Config + dotenv

- バリデーション

- 単体テスト


👉 **UIなしでも動く“完成度の高いコアAPI”がここで出来上がる。**

---

---

# 🟩 **スプリント2：Flask × Jinja2 × Vanilla JS（UI基礎）**

> “計算アプリ”を“Webアプリ”へ昇格させるフェーズ。

### UI でやること

- base.html

- meal_form.html

- meal.js（動的PFC再計算UI）

- Phase切替（色変化・表示切替）


### バックエンド

- ルーティング

- domain → UIに渡す変換

- フォーム入力 → サービスへ連携


---

# 🟧 **スプリント3：モダンUIの強化 × プロテイン × Phase提案**

### UI

- protein_cycle.html（残量管理UI）

- protein.js（残量、警告モーダル）


### ロジック

- phase補正の計算

- 推奨PFCの表示


---

# 🟥 **スプリント4：月間レポート × グラフ（Chart.js）**

### UI

- report.html

- report.js（PFC推移グラフ、支出グラフ）


### API

- 日別の履歴 → 月間レポートへ変換


---

# 🟪 **スプリント5：品質向上 × デプロイ**

### バックエンド

- logging

- pytest（APIテスト）


### インフラ

- Render/Railway デプロイ

- Procfile, gunicorn

- env の本番反映

