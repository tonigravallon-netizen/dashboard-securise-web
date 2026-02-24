/**
 * ARCANA WIKI — chatbot.js
 * Widget chatbot ORACLE (IA Gemini)
 */

let chatbotOpen = false;

function toggleChatbot() {
    const panel = document.getElementById('chatbot-panel');
    const icon = document.getElementById('chatbot-icon');
    chatbotOpen = !chatbotOpen;

    if (chatbotOpen) {
        panel.classList.remove('hidden');
        panel.style.animation = 'slideUp 0.3s ease';
        icon.textContent = '✕';
        document.getElementById('chatbot-input').focus();
    } else {
        panel.style.animation = 'slideDown 0.3s ease';
        setTimeout(() => panel.classList.add('hidden'), 250);
        icon.textContent = '👁️';
    }
}

async function sendChatMessage(event) {
    event.preventDefault();
    const input = document.getElementById('chatbot-input');
    const text = input.value.trim();
    if (!text) return;

    // Add user message
    appendMessage('user', text);
    input.value = '';
    input.disabled = true;

    // Show typing indicator
    const typingId = showTyping();

    try {
        const resp = await fetch('/api/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }),
        });
        const data = await resp.json();
        removeTyping(typingId);

        if (data.ok) {
            appendMessage('ai', data.response);
        } else {
            appendMessage('ai', data.error || 'ORACLE est temporairement indisponible.');
        }
    } catch (e) {
        removeTyping(typingId);
        appendMessage('ai', 'Erreur de connexion avec ORACLE.');
    }

    input.disabled = false;
    input.focus();
}

function appendMessage(role, text) {
    const container = document.getElementById('chatbot-messages');

    const wrapper = document.createElement('div');
    wrapper.className = 'flex gap-2';

    if (role === 'ai') {
        wrapper.innerHTML = `
            <span class="text-lg flex-shrink-0 mt-1">👁️</span>
            <div class="chat-bubble-ai px-3 py-2 text-sm text-parchment-200">${formatMessage(text)}</div>
        `;
    } else {
        wrapper.innerHTML = `
            <div class="ml-auto chat-bubble-user px-3 py-2 text-sm text-parchment-100">${escapeHtml(text)}</div>
        `;
    }

    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    const container = document.getElementById('chatbot-messages');
    const id = 'typing-' + Date.now();

    const wrapper = document.createElement('div');
    wrapper.id = id;
    wrapper.className = 'flex gap-2';
    wrapper.innerHTML = `
        <span class="text-lg flex-shrink-0 mt-1">👁️</span>
        <div class="chat-bubble-ai px-3 py-2 text-sm text-gray-500">
            <span class="typing-dots">
                <span>.</span><span>.</span><span>.</span>
            </span>
        </div>
    `;
    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function formatMessage(text) {
    // Basic markdown formatting for chat
    let html = escapeHtml(text);
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gold-400">$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/`(.*?)`/g, '<code class="bg-abyss-700 px-1 rounded text-matrix-500 text-xs">$1</code>');
    html = html.replace(/\n/g, '<br>');
    return html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function clearChatHistory() {
    if (!confirm('Effacer l\'historique de conversation ?')) return;

    try {
        await fetch('/api/chat/clear', { method: 'POST' });
    } catch (e) {
        // ignore
    }

    const container = document.getElementById('chatbot-messages');
    container.innerHTML = `
        <div class="flex gap-2">
            <span class="text-lg flex-shrink-0 mt-1">👁️</span>
            <div class="chat-bubble-ai px-3 py-2 text-sm text-parchment-200">
                🔍 Bienvenue dans les <strong class="text-gold-500">Archives Interdites</strong>. Je suis <strong class="text-gold-400">ORACLE</strong>, votre guide dans les mysteres et les verites cachees. Quel sujet souhaitez-vous explorer ?
            </div>
        </div>
    `;
}
