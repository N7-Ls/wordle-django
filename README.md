# Wordle (Django)

以 Django 重現的每日 Wordle 猜字遊戲。每天依固定起始日期從單字庫中決定當天答案（所有玩家當天答案相同），玩家登入後進行猜字，系統依「完全命中（綠）/字母存在但位置錯（黃）/不存在（灰）」規則評分，並提供當日排行榜（依嘗試次數排序）。

## 技術棧
- Python / Django
- SQLite（本地開發資料庫，未納入版控）
- Bootstrap（前端樣式）

## 主要結構
- `games/models.py`：`User`、`History`（每日遊玩紀錄）、`Guess`（每次猜測紀錄）
- `games/views.py`：登入/註冊、每日答案邏輯、猜字評分、排行榜
- `templates/`：遊戲頁面（`daily.html`、`login.html`、`register.html` 等）

## 資料集
- `valid_words.txt`（5757 字）、`words1.txt`（153 字）：公開的英文五字母單字清單，作為可接受猜測詞與候選答案庫，非程式自行蒐集之資料。

## 執行方式
```bash
pip install django
python manage.py migrate
python manage.py runserver
```
