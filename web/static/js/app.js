/**
 * Dashboard Securise - Polling global & badges de notification
 */

(function() {
    const POLL_INTERVAL = 5000; // 5 secondes

    function updateBadge(id, count) {
        const el = document.getElementById(id);
        if (!el) return;
        if (count > 0) {
            el.textContent = count > 99 ? '99+' : count;
            el.classList.remove('hidden');
            el.classList.add('badge-pulse');
            setTimeout(() => el.classList.remove('badge-pulse'), 300);
        } else {
            el.classList.add('hidden');
        }
    }

    async function pollUpdates() {
        try {
            const res = await fetch('/api/poll');
            if (!res.ok) return;
            const data = await res.json();

            // Badges amis (desktop + mobile)
            updateBadge('badge-friends-desktop', data.pending_requests || 0);
            updateBadge('badge-friends-mobile', data.pending_requests || 0);

            // Badges messages
            updateBadge('badge-messages-desktop', data.unread_messages || 0);
            updateBadge('badge-messages-mobile', data.unread_messages || 0);

            // Badges RDV
            updateBadge('badge-rdv-desktop', data.pending_appointments || 0);
            updateBadge('badge-rdv-mobile', data.pending_appointments || 0);

            // Mettre a jour le titre de la page
            const total = (data.unread_messages || 0) + (data.pending_requests || 0) + (data.pending_appointments || 0);
            const baseTitle = document.title.replace(/^\(\d+\)\s*/, '');
            document.title = total > 0 ? `(${total}) ${baseTitle}` : baseTitle;

        } catch(e) {
            // Silencieux en cas d'erreur reseau
        }
    }

    // Premier poll immediat, puis toutes les 5s
    pollUpdates();
    setInterval(pollUpdates, POLL_INTERVAL);
})();
