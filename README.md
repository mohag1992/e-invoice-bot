# e-Invoice Guideline Bot

IRBM（マレーシア内国歳入庁）の **e-Invoice Guideline (Version 4.6)** に基づき、ユーザーの入力言語（英語・日本語）を検出して即座に回答するAIボットです。

An AI bot that answers questions based on the official **IRBM e-Invoice Guideline (v4.6)** and responds in the user's language (English or Japanese).

## Features

- **Language detection**: Detects English or 日本語 from the user's question and responds in the same language.
- **Guideline-based answers**: Uses the structured knowledge extracted from the [e-Invoice Guideline PDF](https://www.hasil.gov.my/media/fzagbaj2/irbm-e-invoice-guideline.pdf).
- **Optional AI**: With `OPENAI_API_KEY` set, uses an LLM for natural, accurate answers. Without it, returns relevant guideline excerpts.

## Quick Start

```bash
cd e-invoice-bot
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

### Optional: Full AI answers

Set your OpenAI API key (or compatible API) for generated answers in the detected language:

```bash
export OPENAI_API_KEY=your-key-here
# Optional: use another model or endpoint
export EINVOICE_BOT_MODEL=gpt-4o-mini
export OPENAI_API_BASE=https://api.openai.com/v1  # or your endpoint
python3 -m streamlit run app.py
```

## Project structure

```
e-invoice-bot/
├── app.py                 # Streamlit web UI
├── bot_engine.py          # Language detection, knowledge load, AI/fallback logic
├── knowledge_base/
│   └── guideline_content.md   # Extracted content from IRBM e-Invoice Guideline v4.6
├── requirements.txt
└── README.md
```

## Reference

- [e-Invoice Guideline (PDF)](https://www.hasil.gov.my/media/fzagbaj2/irbm-e-invoice-guideline.pdf) — IRBM, Version 4.6 (7 Dec 2025)
- [e-Invoice Specific Guideline (PDF)](https://www.hasil.gov.my/media/uwwehxwq/irbm-e-invoice-specific-guideline.pdf) — Additional details (refer to official source)
- [MyTax Portal](https://mytax.hasil.gov.my) — MyInvois Portal login

## License

This project is for reference only. e-Invoice rules and content are from IRBM; always confirm with the official guidelines and IRBM.
# e-invoice-bot
