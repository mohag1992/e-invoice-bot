"""
e-Invoice Guideline Bot Engine
Detects user language and answers based on IRBM e-Invoice Guideline (v4.6).
"""

import re
from pathlib import Path
from typing import List, Optional


def detect_language(text: str) -> str:
    """Detect if input is primarily Japanese or English."""
    if not text or not text.strip():
        return "en"
    # Count Japanese characters (Hiragana, Katakana, CJK)
    jp_pattern = re.compile(
        r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF00-\uFFEF]"
    )
    jp_count = len(jp_pattern.findall(text))
    # Rough threshold: if significant Japanese chars, treat as Japanese
    return "ja" if jp_count >= 2 else "en"


def load_knowledge_base(lang: str = "en") -> str:
    """Load guideline content. Use lang='ja' for 日本語."""
    name = "guideline_content_ja.md" if lang == "ja" else "guideline_content.md"
    kb_path = Path(__file__).parent / "knowledge_base" / name
    if not kb_path.exists():
        return ""
    return kb_path.read_text(encoding="utf-8")


def build_system_prompt(lang: str) -> str:
    """Build system prompt that instructs the model to use the guideline and respond in the correct language."""
    if lang == "ja":
        lang_instruction = (
            "回答は必ず日本語のみで行ってください。敬体（です・ます調）で、分かりやすく簡潔に書いてください。"
        )
    else:
        lang_instruction = "You MUST respond only in English. Use clear, professional English."
    return f"""You are an expert assistant for the Malaysian e-Invoice system (IRBM MyInvois). 
Your answers must be based ONLY on the official e-Invoice Guideline (Version 4.6) content provided below.
If the guideline does not contain enough information to answer, say so and suggest checking the full PDF or IRBM/MyInvois portal.
{lang_instruction}
Keep answers accurate, concise, and cite section numbers (e.g. Section 1.5, Appendix 1) when relevant.
Do not invent details not present in the guideline."""


# Stopwords so we score on meaningful query terms only
_STOP = frozenset(
    "a an the is are was were be been being have has had do does did will would "
    "could should may might must shall can what when where which who how why "
    "e invoice guideline please tell me about".split()
)

# Japanese words/phrases → English terms for matching the English knowledge base
_JA_TO_EN_TERMS = {
    "実施": "implementation",
    "スケジュール": "timeline",
    "時期": "timeline",
    "いつから": "implementation",
    "いつ": "implementation",
    "開始": "implementation",
    "免除": "exemption",
    "対象外": "exemption",
    "例外": "exemption",
    "義務": "mandatory",
    "必須": "required",
    "必要": "required",
    "要件": "required",
    "api": "API",
    "ポータル": "portal",
    "マイインボイス": "MyInvois",
    "クレジットノート": "credit note",
    "デビットノート": "debit note",
    "返金": "refund",
    "還元": "refund",
    "売上": "revenue",
    "収入": "income",
    "経費": "expense",
    "項目": "fields",
    "フィールド": "fields",
    "検証": "validation",
    "バリデーション": "validation",
    "取消": "cancellation",
    "キャンセル": "cancellation",
    "却下": "rejection",
    "年間": "turnover",
    "売上高": "turnover",
    "ターンオーバー": "revenue",
    "新規": "new business",
    "法人": "taxpayer",
    "個人": "individual",
    "申請": "submission",
    "提出": "submission",
    "送信": "submission",
    "手順": "workflow",
    "流れ": "workflow",
    "種類": "types",
    "タイプ": "types",
    "形式": "format",
    "フォーマット": "format",
    "xml": "XML",
    "json": "JSON",
    "電子": "digital",
    "デジタル": "digital",
}


def _japanese_terms_to_english(query: str) -> List[str]:
    """Map Japanese query to English terms so we can match the English KB."""
    added = []
    for ja, en in _JA_TO_EN_TERMS.items():
        if ja in query and en not in added:
            added.append(en)
    return added


def _japanese_query_terms(query: str) -> List[str]:
    """Terms to use when scoring the Japanese KB: Japanese keywords that appear in the query."""
    return [ja for ja in _JA_TO_EN_TERMS if ja in query]


def get_context_for_query(
    query: str, full_kb: str, max_chars: int = 12000, lang: Optional[str] = None
) -> str:
    """Return the portion of the knowledge base most relevant to this specific query."""
    if lang is None:
        lang = detect_language(query)
    query_lower = query.lower().strip()

    if lang == "ja":
        # Scoring Japanese KB: use Japanese keywords that appear in the query
        query_terms = _japanese_query_terms(query)
        # Also add any English words from the query (e.g. "API", "PDF")
        words = set(re.findall(r"[a-zA-Z0-9]+", query_lower))
        query_terms = list(set(query_terms + [w for w in words if len(w) > 1 and w not in _STOP]))
    else:
        words = set(re.findall(r"[a-zA-Z0-9]+", query_lower))
        query_terms = [w for w in words if len(w) > 1 and w not in _STOP]

    sections = re.split(r"\n(?=#{1,3}\s)", full_kb)
    scored = []
    for section in sections:
        section_lower = section.lower()
        # First line is usually the heading – boost score if query terms appear there
        first_line = section.split("\n")[0] if section else ""
        first_line_lower = first_line.lower()
        score = 0
        for term in query_terms:
            if term in section_lower:
                score += 2 if term in first_line_lower else 1
        # Only include sections that actually match this query (or have at least one term)
        if query_terms and score > 0:
            scored.append((score, section))
        elif not query_terms:
            # No meaningful terms (e.g. "??") – don't score, we'll use fallback below
            scored.append((0, section))

    scored.sort(key=lambda x: -x[0])

    result = []
    total = 0
    for _, section in scored:
        if total + len(section) <= max_chars:
            result.append(section)
            total += len(section)
        else:
            break

    if not result:
        # No matches: return implementation timeline + exemptions (most asked)
        timeline_keys = ("implementation timeline", "1.5", "実施スケジュール", "実施日")
        exempt_keys = ("exemption", "1.6", "免除")
        for section in sections:
            sl = section.lower()
            if any(k in sl or k in section for k in timeline_keys):
                result.append(section)
                break
        for section in sections:
            sl = section.lower()
            if any(k in sl or k in section for k in exempt_keys):
                result.append(section)
                break
        if not result:
            result = [s for s in sections[:4] if len(s) > 100]
    if not result:
        return full_kb[:max_chars]

    return "\n\n".join(result)


def build_messages(user_query: str, kb_content: str, lang: Optional[str] = None) -> List[dict]:
    """Build messages for OpenAI-compatible API (system + user with context)."""
    if lang is None:
        lang = detect_language(user_query)
    system = build_system_prompt(lang)
    context = get_context_for_query(user_query, kb_content, lang=lang)
    label = "ユーザーの質問" if lang == "ja" else "User question"
    user_message = f"""## e-Invoice Guideline (excerpt)\n\n{context}\n\n---\n\n## {label}\n{user_query}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]


def answer_fallback(user_query: str) -> str:
    """Return relevant guideline excerpts when no LLM is available. In user's language."""
    lang = detect_language(user_query)
    kb = load_knowledge_base(lang=lang)
    if not kb:
        return "Knowledge base not found." if lang != "ja" else "ナレッジベースが見つかりません。"
    context = get_context_for_query(user_query, kb, max_chars=6000, lang=lang)
    if lang == "ja":
        intro = f"**ご質問:** {user_query}\n\n上記に関連するガイドラインの抜粋です。詳細は公式PDFをご確認ください。\n\n---\n\n"
    else:
        intro = f"**Your question:** {user_query}\n\nRelevant excerpt from the guideline for your question above. Please refer to the official PDF for full details.\n\n---\n\n"
    return intro + context


def answer_with_openai(user_query: str, api_key: Optional[str] = None) -> str:
    """
    Call OpenAI-compatible API to generate answer.
    Set OPENAI_API_KEY or pass api_key. Base URL can be overridden with OPENAI_API_BASE.
    """
    try:
        import os
        from openai import OpenAI

        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            return (
                "Please set OPENAI_API_KEY in environment or pass api_key to use the AI. "
                "You can also use the fallback answers from the knowledge base."
            )
        client = OpenAI(api_key=key, base_url=os.environ.get("OPENAI_API_BASE"))
        lang = detect_language(user_query)
        kb = load_knowledge_base(lang=lang)
        messages = build_messages(user_query, kb, lang=lang)
        resp = client.chat.completions.create(
            model=os.environ.get("EINVOICE_BOT_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.2,
            max_tokens=1500,
        )
        return (resp.choices[0].message.content or "").strip()
    except ImportError:
        return "Install openai: pip install openai"
    except Exception as e:
        return f"Error calling API: {e}"
