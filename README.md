# AI-API (устаревший проект)

**Проект, которому уже около двух лет. Он сильно устарел и выложен за неактуальностью.**

[Русский](#русский) | [English](#english)

## Русский

Это проект-ретранслятор в реальные API основных AI-моделей (OpenAI, Gemini, Claude, Grok). Работает как стандартный API-слой и по обычным правилам связывается с внешними сервисами.

Для чего это было нужно: чтобы из закрытых стран можно было работать с ИИ через незаблокированные серверы. Клиент обращается к этому ретранслятору, а тот перенаправляет запрос в реальные API от имени сервера, обходя блокировки и ограничения.

Что внутри:
- FastAPI-прокси к реальным API моделей.
- Telegram-боты для выдачи доступа и для общения с ИИ.
- Хранение истории, ключей, статистики и платежей в PostgreSQL.
- Поддержка текста, изображений, голоса (Whisper + TTS).
- Возможность выгружать данные клиентов в JSON.

Запуск:

```
docker-compose up -d --build
```

## English

This is a relay project that forwards requests to the real APIs of major AI models (OpenAI, Gemini, Claude, Grok). It works as a standard API layer and communicates with external services by the usual rules.

Why it was needed: so that from restricted countries one could work with AI through unblocked servers. A client talks to this relay, and the relay forwards the request to the real APIs on behalf of the server, bypassing blocks and restrictions.

What's inside:
- FastAPI proxy to the real model APIs.
- Telegram bots for issuing access and for chatting with AI.
- Storage of history, keys, statistics and payments in PostgreSQL.
- Support for text, images, voice (Whisper + TTS).
- Ability to export client data to JSON.

Run:

```
docker-compose up -d --build
```