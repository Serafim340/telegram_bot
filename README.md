# Telegram Bot

## 📌 Описание | Description

**Telegram Bot** — это Telegram-бот на базе DeepSeek, предназначенный для генерации текстов под любую профессию. Бот легко адаптируется под нужный стиль и тональность — всё зависит от промпта, который вы зададите. Идеален для маркетинга, копирайтинга, инфо-бизнеса и других задач.

**Telegram Bot** is a Telegram bot powered by DeepSeek that generates texts tailored to any profession. You can fully customize its tone and personality using a system prompt — perfect for marketing, copywriting, coaching, and more.

---

## ⚙️ Установка | Setup {#setup}

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/Serafim340/telegram_bot.git
cd telegram_bot
```

2. **Создайте **`.env`** файл с переменными окружения**

```env
TOKEN=ваш_telegram_bot_token
DEEPSEEK_API_KEY=ваш_openrouter_api_key
ALLOWED_USERS=123456789,987654321
```

3. **Создайте файл **`promt.txt`** рядом с **`main.py`** — здесь будет описан ваш системный промпт (вся личность бота).

4. **Установите зависимости**

```bash
pip install -r requirements.txt
```

5. **Запустите бота**

```bash
python main.py
```

---
## 🖥️ Локальный запуск | Run Locally

Этот бот можно запускать не только на сервере, но и локально на вашем компьютере.
1. Убедитесь, что у вас установлен Python 3.10+
2. Выполните шаги из раздела ⚙️ [Установка | Setup](#setup)
3. Запустите файл `main.py`
4. Бот сразу начнёт работать в Telegram

---

## ☁️ Развёртывание на Render | Deploy to Render

- Сделайте репозиторий **приватным** (если хотите держать ключи в `.env`)
- Подключите репозиторий к [Render.com](https://render.com)
- Настройте процесс как `Web Service`
- В `Build Command`: `pip install -r requirements.txt`
- В `Start Command`: `python main.py`
- Установите переменные окружения в панели Render

---

## 🧠 Настройка личности бота | Bot Personality Setup

Системный промпт хранится в **отдельном файле**`promt.txt` — это позволяет держать чувствительную информацию вне GitHub.

**Пример**:

```
Ты — эксперт по путешествиям, пишешь посты для Telegram-канала в стиле лёгких рассказов, с советами, лайфхаками и живым тоном.
```

---

## 🔐 Безопасность | Security

- Доступ к боту ограничен через список `ALLOWED_USERS` в `.env`
- Вы можете добавить несколько ID через запятую

---
## 🧹 Структура проекта

```
📁 telegram_bot/
├── main.py               # Основной код бота
├── prompt.txt            # Системный промт (личность бота)
├── .env                  # Переменные окружения    
├── .env.example          # Пример настройки
├── requirements.txt      # Зависимости Python
├── Procfile              # Для Render
├── .gitignore            # Игнорируемые файлы
└── README.md             # Описание
```

---

## 📬 По вопросам и предложениям — пишите [сюда](https://t.me/@Serafim340)

