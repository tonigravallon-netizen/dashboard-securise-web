/**
 * ARCANA WIKI — wiki.js
 * Gestion des votes, commentaires et recherche dynamique
 */

// ── Votes ──────────────────────────────────────────────────

async function voteArticle(articleId, voteType) {
    try {
        const resp = await fetch('/api/wiki/vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ article_id: articleId, vote_type: voteType }),
        });
        const data = await resp.json();

        if (data.ok) {
            const upEl = document.getElementById('upvote-count');
            const downEl = document.getElementById('downvote-count');
            if (upEl) upEl.textContent = data.upvotes;
            if (downEl) downEl.textContent = data.downvotes;

            // Update button styles
            document.querySelectorAll('.vote-btn').forEach(btn => {
                btn.classList.remove('active-up', 'active-down', 'text-matrix-500', 'text-red-400');
                btn.classList.add('text-gray-500');
            });
            const btns = document.querySelectorAll('.vote-btn');
            if (btns[0] && data.upvotes !== undefined) {
                // Determine current user vote from response
                const prevUp = parseInt(upEl?.dataset.prev || upEl?.textContent || '0');
                // Simple toggle: if counts changed, highlight accordingly
            }
        } else if (resp.status === 401) {
            window.location.href = '/login';
        } else {
            console.error('Vote error:', data.error);
        }
    } catch (e) {
        console.error('Vote fetch error:', e);
    }
}


// ── Commentaires ───────────────────────────────────────────

async function addComment(event, articleId) {
    event.preventDefault();
    const textarea = document.getElementById('comment-text');
    const text = textarea.value.trim();
    if (!text) return;

    try {
        const resp = await fetch('/api/wiki/comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ article_id: articleId, text: text }),
        });
        const data = await resp.json();

        if (data.ok) {
            // Insert new comment in list
            const list = document.getElementById('comments-list');
            const c = data.comment;
            const initial = (c.author_username || 'A').charAt(0).toUpperCase();

            const div = document.createElement('div');
            div.className = 'bg-abyss-800 rounded-xl px-4 py-3 border border-gold-500/5';
            div.innerHTML = `
                <div class="flex items-center gap-2 mb-2">
                    <span class="w-6 h-6 bg-abyss-700 rounded-full flex items-center justify-center text-xs text-gold-500 font-title">${initial}</span>
                    <span class="text-sm text-gray-300">${escapeHtml(c.author_username)}</span>
                    <span class="text-xs text-gray-600">a l'instant</span>
                </div>
                <p class="text-sm text-gray-400 font-article">${escapeHtml(c.text)}</p>
            `;
            list.insertBefore(div, list.firstChild);
            textarea.value = '';
        } else if (resp.status === 401) {
            window.location.href = '/login';
        } else {
            alert(data.error || 'Erreur lors de la publication');
        }
    } catch (e) {
        console.error('Comment fetch error:', e);
    }
}


// ── Recherche dynamique ────────────────────────────────────

let searchTimeout = null;

function initLiveSearch() {
    const inputs = document.querySelectorAll('input[name="q"]');
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            const q = this.value.trim();
            if (q.length < 2) {
                hideLiveResults();
                return;
            }
            searchTimeout = setTimeout(() => liveSearch(q, this), 300);
        });

        // Close on click outside
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.search-results-live') && !e.target.closest('input[name="q"]')) {
                hideLiveResults();
            }
        });
    });
}

async function liveSearch(query, inputEl) {
    try {
        const resp = await fetch(`/api/wiki/search?q=${encodeURIComponent(query)}`);
        const data = await resp.json();

        let container = inputEl.parentElement.querySelector('.search-results-live');
        if (!container) {
            container = document.createElement('div');
            container.className = 'search-results-live absolute top-full left-0 right-0 mt-1 bg-abyss-800 border border-gold-500/15 rounded-lg shadow-xl z-50 max-h-64 overflow-y-auto';
            inputEl.parentElement.style.position = 'relative';
            inputEl.parentElement.appendChild(container);
        }

        if (data.articles && data.articles.length > 0) {
            container.innerHTML = data.articles.map(a => `
                <a href="/wiki/article/${a.slug}" class="block px-4 py-2.5 hover:bg-abyss-700 transition-colors border-b border-gold-500/5 last:border-0">
                    <div class="text-sm text-parchment-100">${escapeHtml(a.title)}</div>
                    <div class="text-xs text-gray-500">${escapeHtml(a.category || '')} ${a.summary ? '— ' + escapeHtml(a.summary) : ''}</div>
                </a>
            `).join('');
            container.classList.remove('hidden');
        } else {
            container.innerHTML = '<div class="px-4 py-3 text-sm text-gray-500">Aucun resultat</div>';
            container.classList.remove('hidden');
        }
    } catch (e) {
        console.error('Search error:', e);
    }
}

function hideLiveResults() {
    document.querySelectorAll('.search-results-live').forEach(el => el.classList.add('hidden'));
}


// ── Sources (ajout par utilisateur) ───────────────────────

function toggleSourceForm() {
    const form = document.getElementById('source-form');
    form.classList.toggle('hidden');
}

async function submitSource(articleId) {
    const title = document.getElementById('source-title').value.trim();
    const url = document.getElementById('source-url').value.trim();
    const type = document.getElementById('source-type').value;
    const feedback = document.getElementById('source-feedback');

    if (!title || !url) {
        feedback.textContent = 'Titre et URL requis.';
        feedback.className = 'text-xs mt-2 text-red-400';
        feedback.classList.remove('hidden');
        return;
    }

    try {
        const resp = await fetch('/api/wiki/add-source', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ article_id: articleId, title, url, type }),
        });
        const data = await resp.json();

        if (data.ok) {
            // Add new source to the list
            const list = document.getElementById('sources-list');
            const noSource = list.querySelector('p');
            if (noSource) noSource.remove();

            const div = document.createElement('div');
            div.className = 'bg-abyss-800 rounded-lg px-4 py-3 border-l-2 border-gold-500/30 text-sm';
            div.innerHTML = `
                <a href="${escapeHtml(url)}" target="_blank" rel="noopener" class="text-gold-500 hover:text-gold-400 transition-colors">${escapeHtml(title)}</a>
                <span class="text-xs text-gray-600 ml-2">[${escapeHtml(type)}]</span>
            `;
            list.appendChild(div);

            // Reset form
            document.getElementById('source-title').value = '';
            document.getElementById('source-url').value = '';
            feedback.textContent = 'Source ajoutee avec succes !';
            feedback.className = 'text-xs mt-2 text-matrix-500';
            feedback.classList.remove('hidden');
            setTimeout(() => feedback.classList.add('hidden'), 3000);
        } else if (resp.status === 401) {
            window.location.href = '/login';
        } else {
            feedback.textContent = data.error || 'Erreur';
            feedback.className = 'text-xs mt-2 text-red-400';
            feedback.classList.remove('hidden');
        }
    } catch (e) {
        console.error('Source submit error:', e);
    }
}


// ── Flash messages auto-dismiss ────────────────────────────

function initFlashDismiss() {
    document.querySelectorAll('.flash-message').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 500);
        }, 4000);
    });
}


// ── Utilitaires ────────────────────────────────────────────

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


// ── Init ───────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function () {
    initLiveSearch();
    initFlashDismiss();
});
