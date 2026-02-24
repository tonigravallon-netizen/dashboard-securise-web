"""Service d'integration Google Gemini API pour la generation de contenu
et le chatbot IA du wiki des conspirations."""

import os
import time
import threading

import google.generativeai as genai

# Rate limiting: 15 req/min sur l'API gratuite
RATE_LIMIT = 15
RATE_WINDOW = 60  # secondes


class GeminiService:
    """Gere toutes les interactions avec l'API Google Gemini."""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "")
        self._available = False
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                self._available = True
            except Exception:
                self.model = None
        else:
            self.model = None
        self._request_times = []
        self._lock = threading.Lock()

    def is_available(self):
        return self._available and self.model is not None

    def _check_rate_limit(self):
        """Verifie et applique le rate limit de 15 req/min."""
        with self._lock:
            now = time.time()
            self._request_times = [t for t in self._request_times if now - t < RATE_WINDOW]
            if len(self._request_times) >= RATE_LIMIT:
                return False
            self._request_times.append(now)
            return True

    # ── Generation d'articles ─────────────────────────────────

    def generate_article(self, subject, category="", tone="neutre", length="moyen"):
        """Genere un article wiki complet en Markdown."""
        if not self.is_available():
            return None, "Service IA non disponible."
        if not self._check_rate_limit():
            return None, "Limite de requetes atteinte. Reessayez dans une minute."

        length_map = {"court": "800 mots", "moyen": "1500 mots", "long": "2500 mots"}
        tone_map = {
            "neutre": "un ton neutre et factuel, presentant les faits et les differentes perspectives",
            "conspirationniste": "un ton mysterieux et intriguant, comme un investigateur qui revele des verites cachees, en utilisant des formulations suggestives",
            "sceptique": "un ton analytique et sceptique, deconstruisant la theorie tout en restant respectueux",
        }

        prompt = f"""Tu es un redacteur expert pour un wiki francophone sur les theories du complot
et les mysteres non resolus. Ecris un article complet en francais sur le sujet suivant.

SUJET : {subject}
CATEGORIE : {category}
TON : {tone_map.get(tone, tone_map["neutre"])}
LONGUEUR VISEE : {length_map.get(length, "1500 mots")}

FORMAT DE SORTIE (Markdown strict) :

### Contexte
[Introduction et mise en contexte]

### Les faits etablis
[Ce qui est verifie et reconnu]

### La theorie
[Explication detaillee de la theorie/conspiration]

### Arguments et preuves
[Elements avances par les partisans]

### Contre-arguments
[Elements avances par les sceptiques]

### Conclusion
[Synthese equilibree]

REGLES :
- Ecris UNIQUEMENT en francais
- Reste factuel meme si le ton est conspirationniste
- Ne fais JAMAIS de propagande, presente toujours les deux cotes
- Inclus des dates, noms et faits verifiables quand possible
- Utilise le format Markdown avec des titres ###, des listes, du **gras** et de l'*italique*
- Ne mets PAS de titre principal (il sera gere separement)
- NE genere PAS de sources/URLs (elles seront ajoutees separement)
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            return None, f"Erreur Gemini : {str(e)}"

    def generate_summary(self, content, max_length=200):
        """Genere un resume court d'un article."""
        if not self.is_available() or not self._check_rate_limit():
            return content[:max_length] + "..." if len(content) > max_length else content

        prompt = f"""Resume ce texte en une seule phrase de maximum {max_length} caracteres, en francais.
Texte : {content[:2000]}

Reponds UNIQUEMENT avec le resume, rien d'autre."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()[:max_length]
        except Exception:
            return content[:max_length] + "..." if len(content) > max_length else content

    # ── Chatbot IA "ORACLE" ───────────────────────────────────

    def chat_response(self, user_message, conversation_history=None):
        """Genere une reponse de chatbot contextuelle."""
        if not self.is_available():
            return None, "ORACLE est hors ligne. Verifiez la configuration de l'API."
        if not self._check_rate_limit():
            return None, "ORACLE est temporairement surcharge. Reessayez dans quelques instants."

        system_context = """Tu es "ORACLE", un agent d'intelligence artificielle specialise dans les
theories du complot, les mysteres historiques, les phenomenes inexpliques et les societes secretes.

PERSONNALITE :
- Tu es mysterieux mais accessible, comme un bibliothecaire d'archives secretes
- Tu parles toujours en francais
- Tu es factuel : tu presentes les theories AVEC leur contexte et leurs critiques
- Tu ne promeus JAMAIS la desinformation dangereuse (anti-vaccin, negationisme, etc.)
- Tu fais la distinction entre "theorie conspirationniste interessante" et "desinformation dangereuse"
- Tu utilises parfois des formulations intrigantes : "les documents declassifies revelent...", "selon certaines sources..."
- Tu restes bref (2-4 paragraphes max par reponse) sauf si on te demande d'elaborer
- Tu peux utiliser des emojis moderement pour l'ambiance : 🔍 👁️ 📜 🗂️

LIMITES :
- Si on te pose des questions hors sujet, ramene poliment vers ton domaine d'expertise
- Si on te demande des choses dangereuses, refuse fermement
- Mentionne toujours que tu presentes des THEORIES et non des faits etablis quand c'est le cas
"""

        messages = [
            {"role": "user", "parts": [system_context + "\n\nCommence la conversation."]},
            {"role": "model", "parts": ["🔍 Bienvenue dans les Archives Interdites. Je suis **ORACLE**, votre guide dans les mysteres et les verites cachees. Quel sujet souhaitez-vous explorer aujourd'hui ?"]},
        ]

        if conversation_history:
            for msg in conversation_history[-10:]:
                role = "user" if msg.get("role") == "user" else "model"
                messages.append({"role": role, "parts": [msg.get("content", "")]})

        messages.append({"role": "user", "parts": [user_message]})

        try:
            chat = self.model.start_chat(history=messages[:-1])
            response = chat.send_message(user_message)
            return response.text, None
        except Exception as e:
            return None, f"ORACLE est temporairement indisponible : {str(e)}"

    # ── Suggestion de tags ────────────────────────────────────

    def suggest_tags(self, title, content_excerpt=""):
        """Genere des tags automatiques pour un article."""
        if not self.is_available() or not self._check_rate_limit():
            return []

        prompt = f"""Genere exactement 5 tags (mots-cles) en francais pour cet article de wiki sur les conspirations.
Titre: {title}
Extrait: {content_excerpt[:500]}

Reponds UNIQUEMENT avec les 5 tags separes par des virgules, en minuscules, sans accents.
Exemple: illuminati, societe-secrete, nouvel-ordre-mondial, franc-maconnerie, elite"""

        try:
            response = self.model.generate_content(prompt)
            tags = [t.strip().lower().replace(" ", "-") for t in response.text.split(",")]
            return tags[:5]
        except Exception:
            return []


# Instance globale (singleton)
_gemini_instance = None


def get_gemini():
    """Retourne l'instance singleton de GeminiService."""
    global _gemini_instance
    if _gemini_instance is None:
        _gemini_instance = GeminiService()
    return _gemini_instance
