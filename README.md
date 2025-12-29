# Flask Trainer Budget


## 🌐 Live Demo
https://flask-trainer-budget.onrender.com
※ 無料枠のため初回アクセス時は数秒待つ場合があります


## ✨ Features

- 食材カテゴリ → 食材の2段階選択
- グラム指定によるリアルタイムPFC / kcal / 価格計算
- フェーズ（bulk / cut）× 食事タイミング対応
- サーバー側での推奨PFC算出と差分判定（low / ok / high）
- 月間コストの簡易レポート表示(現在はダミーデータを固定表示。将来的に食事履歴と連動させる設計を想定)


## 💡 Motivation

既存の食事管理アプリはダイエット用途が中心で、
トレーニーを想定した場合、以下の点に課題を感じました。

- グラム単位での管理がしづらい
- PFCの「推奨」と「実測との差分」が分かりにくい
- 食事内容とコストを同時に把握しづらい

本アプリは、増量期（bulk）・減量期（cut）といった
フェーズごとの目的に応じて、
「考えながら食事を選べる」体験を提供することを目指しています。
将来的には、より細かなフェーズやユーザー設定にも対応できる構造を想定しています。


## 🛠 Tech Stack

- Python 3.x
- Flask
- Jinja2 / Vanilla JS
- pytest
- mypy (strict)
- gunicorn
- Render


## 🧩 Architecture

- TypedDict を用いた明示的なデータ構造
- domain / services / config の責務分離
- meal_service と recommendation_service の独立
- 将来的なDB導入を想定した設計


## 🧠 Recommendation Logic

- target_kcal × フェーズ設定から推奨PFCを算出
- 実測値との差分を計算
- low / ok / high の3段階で判定
- 判定ロジックは meal_service から独立
※ 現在の推奨PFCは「1日の目標カロリーを前提とした簡易モデル」に基づいており、
　1食あたりの吸収量や個人差（体重・身長・活動量など）は考慮していません。


## 🔐 Validation & Error Handling

- services 層での入力検証（型・値域）
- 不正な入力は早期に弾く設計
- ビジネスロジックとUI層の責務分離


## 🧭 Design Philosophy

- 将来のDB導入・Django移行を前提とした構造
- app.py を薄く保ち、services を中心に設計


## 🧪 Testing

- Services layer test coverage: 94%
- pytest によるビジネスロジック中心のテスト


## ▶️ Run Locally

```bash
pip install -r requirements.txt
python app.py
```


## 📌 Notes

- 現在はログイン機能・ユーザー管理は未実装
- 月間レポートはダミーデータ表示
- 推奨PFCと差分表示は簡易的なロジックに基づくものであり、
  厳密な栄養指導や個別最適化を目的としたものではありません
- UI / UX は今後も改善予定


## 🚀 Future Improvements

- ユーザー設定（体重・目標kcal）
- 1日PFCと1食PFCを分離した推奨ロジック
- 食事履歴の永続化
- Django版への拡張
