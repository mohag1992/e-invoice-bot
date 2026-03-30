import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const mdComponents = {
  a: ({ node: _n, ...props }) => (
    <a {...props} target="_blank" rel="noopener noreferrer" />
  ),
};

function chatApiUrl() {
  const raw = import.meta.env.VITE_API_URL?.trim();
  if (raw) return `${raw.replace(/\/$/, '')}/api/chat`;
  return `${window.location.origin}/api/chat`;
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
    </svg>
  );
}

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [input]);

  function addMessage(role, content, lang) {
    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role, content, lang },
    ]);
  }

  async function sendMessage() {
    const message = input.trim();
    if (!message || loading) return;
    setInput('');
    addMessage('user', message);
    setError('');
    setLoading(true);
    try {
      const res = await fetch(chatApiUrl(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const raw = await res.text();
      let data = {};
      try {
        data = raw ? JSON.parse(raw) : {};
      } catch {
        data = {};
      }
      if (!res.ok) {
        const hint =
          data.error ||
          (raw && !raw.trim().startsWith('{')
            ? `HTTP ${res.status}: API に接続できません（.env.development の VITE_API_URL を確認）`
            : `HTTP ${res.status}`);
        setError(hint);
        addMessage('assistant', data.answer || 'エラーが発生しました。');
        return;
      }
      const answer = data.answer || '';
      const lang = data.lang || 'en';
      if (answer) addMessage('assistant', answer, lang);
    } catch (err) {
      setError(err.message || 'Network error');
      addMessage(
        'assistant',
        '申し訳ありません。接続エラーです。 / Connection error.'
      );
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(e) {
    e.preventDefault();
    sendMessage();
  }

  function onKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app">
      <header className="chat-header">
        <div className="chat-header-inner">
          <div className="chat-brand">
            <div className="chat-logo" aria-hidden="true">
              <span className="chat-logo-mark">📄</span>
            </div>
            <div className="chat-brand-text">
              <h1 className="chat-title">e-Invoice Guideline Bot</h1>
              <p className="chat-tagline">
                IRBM Guideline v4.6 · 英語 / 日本語
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="chat-main">
        <div className="chat-scroll">
          {messages.length === 0 && !loading ? (
            <div className="empty-state">
              <div className="empty-state-card">
                <h2 className="empty-state-title">マレーシア e-Invoice について質問してください</h2>
                <p className="empty-state-desc">
                  IRBM の公式ガイドラインに基づいて回答します。英語でも日本語でもどうぞ。
                </p>
                <ul className="empty-state-hints">
                  <li>実施スケジュールや免除対象は？</li>
                  <li>What are the e-invoice submission requirements?</li>
                </ul>
              </div>
            </div>
          ) : null}

          {messages.map((m) => (
            <article
              key={m.id}
              className={`turn turn-${m.role}`}
              aria-label={m.role === 'user' ? 'Your message' : 'Assistant'}
            >
              <div
                className={`turn-avatar ${m.role === 'assistant' ? 'turn-avatar--assistant' : 'turn-avatar--user'}`}
                aria-hidden="true"
              >
                {m.role === 'assistant' ? '🤖' : '👤'}
              </div>
              <div className="turn-body">
                {m.role === 'assistant' ? (
                  <div className="msg-content">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={mdComponents}
                    >
                      {m.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <div className="msg-plain">{m.content}</div>
                )}
                {m.lang ? (
                  <span className="lang-pill">
                    {m.lang === 'ja' ? '日本語' : 'English'}
                  </span>
                ) : null}
              </div>
            </article>
          ))}

          {loading ? (
            <div className="turn turn-assistant turn-typing" aria-live="polite">
              <div className="turn-avatar turn-avatar--assistant" aria-hidden="true">
                🤖
              </div>
              <div className="turn-body">
                <div className="typing-dots" aria-label="応答を生成しています">
                  <span />
                  <span />
                  <span />
                </div>
                <span className="typing-label">ガイドラインを参照しています…</span>
              </div>
            </div>
          ) : null}

          <div ref={messagesEndRef} className="scroll-anchor" aria-hidden="true" />
        </div>
      </main>

      <div className="composer-shell">
        <div className="composer-inner">
          {error ? (
            <div className="error-banner" role="alert">
              {error}
            </div>
          ) : null}
          <form className="composer-form" onSubmit={onSubmit}>
            <div className="composer-box">
              <textarea
                ref={textareaRef}
                className="composer-input"
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={onKeyDown}
                placeholder="メッセージを入力…（Enter で送信、Shift+Enter で改行）"
                autoComplete="off"
                disabled={loading}
              />
              <button
                type="submit"
                className="composer-send"
                disabled={loading || !input.trim()}
                aria-label="送信"
              >
                <SendIcon />
              </button>
            </div>
          </form>
          <footer className="chat-footer">
            <span className="footer-meta">
              Based on{' '}
              <a
                href="https://www.hasil.gov.my/media/fzagbaj2/irbm-e-invoice-guideline.pdf"
                target="_blank"
                rel="noopener noreferrer"
              >
                IRBM e-Invoice Guideline (v4.6)
              </a>
              {' · '}
              <a href="https://mytax.hasil.gov.my" target="_blank" rel="noopener noreferrer">
                MyTax
              </a>
            </span>
          </footer>
        </div>
      </div>
    </div>
  );
}
