import yaml
import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from itertools import zip_longest

# ============================================================
# 1. UI TEXT DICTIONARY (I18N)
# ============================================================
UI_STRINGS = {
    "Russian": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Задайте вопрос по текстам Сета.<br>Система найдёт релевантные фрагменты и ответит голосом Сета.",
        "lang_label": "Язык ответа",
        "chat_label": "Диалог",
        "msg_label": "Ваш вопрос",
        "msg_placeholder": "Например: что Сет говорит о природе реальности?",
        "submit_btn": "Спросить",
        "clear_btn": "Очистить диалог",
        "sources_label": "Источники",
        "no_answer": "В доступных материалах нет прямого ответа на этот вопрос.",
        "welcome_sources": "**Источники появятся здесь**"
    },
    "English": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Ask a question about the Seth Materials.<br>The system will find relevant quotes and answer in Seth's voice.",
        "lang_label": "Response Language",
        "chat_label": "Dialogue",
        "msg_label": "Your Question",
        "msg_placeholder": "E.g.: What does Seth say about the nature of reality?",
        "submit_btn": "Ask",
        "clear_btn": "Clear Chat",
        "sources_label": "Sources",
        "no_answer": "There is no direct answer in the available materials.",
        "welcome_sources": "**Sources will appear here**"
    },
    "Portuguese": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Faça uma pergunta sobre os materiais de Seth.<br>O sistema encontrará fragmentos relevantes e responderá com a voz de Seth.",
        "lang_label": "Idioma da resposta",
        "chat_label": "Diálogo",
        "msg_label": "Sua pergunta",
        "msg_placeholder": "Ex.: O que Seth diz sobre a natureza da realidade?",
        "submit_btn": "Perguntar",
        "clear_btn": "Limpar chat",
        "sources_label": "Fontes",
        "no_answer": "Nos materiais disponíveis não há uma resposta direta para esta questão.",
        "welcome_sources": "**As fontes aparecerão aqui**"
    },
    "Italian": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Fai una domanda sui materiali di Seth.<br>Il sistema troverà i frammenti rilevanti e risponderà con la voce di Seth.",
        "lang_label": "Lingua della risposta",
        "chat_label": "Dialogo",
        "msg_label": "La tua domanda",
        "msg_placeholder": "Es.: Cosa Seth dice sulla natura della realtà?",
        "submit_btn": "Chiedi",
        "clear_btn": "Pulisci chat",
        "sources_label": "Fonti",
        "no_answer": "Nei materiali disponibili non esiste una risposta diretta a questa domanda.",
        "welcome_sources": "**Le fonti appariranno qui**"
    },
    "French": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Posez une question sur les écrits de Seth.<br>Le système trouvera les fragments pertinents et répondra avec la voix de Seth.",
        "lang_label": "Langue de réponse",
        "chat_label": "Dialogue",
        "msg_label": "Votre question",
        "msg_placeholder": "Ex. : Que dit Seth sur la nature de la réalité ?",
        "submit_btn": "Demander",
        "clear_btn": "Effacer le chat",
        "sources_label": "Sources",
        "no_answer": "Il n'y a pas de réponse directe dans les matériaux disponibles.",
        "welcome_sources": "**Les sources apparaîtront ici**"
    },
    "German": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Stellen Sie eine Frage zu Seths Materialien.<br>Das System wird relevante Fragmente finden und mit Seths Stimme antworten.",
        "lang_label": "Antwortsprache",
        "chat_label": "Dialog",
        "msg_label": "Ihre Frage",
        "msg_placeholder": "Z.B.: Was sagt Seth über die Natur der Wirklichkeit?",
        "submit_btn": "Fragen",
        "clear_btn": "Chat löschen",
        "sources_label": "Quellen",
        "no_answer": "In den verfügbaren Materialien gibt es keine direkte Antwort auf diese Frage.",
        "welcome_sources": "**Quellen werden hier angezeigt**"
    },
    "Spanish": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Haz una pregunta sobre los materiales de Seth.<br>El sistema encontrará fragmentos relevantes y responderá con la voz de Seth.",
        "lang_label": "Idioma de respuesta",
        "chat_label": "Diálogo",
        "msg_label": "Tu pregunta",
        "msg_placeholder": "Ej.: ¿Qué dice Seth sobre la naturaleza de la realidad?",
        "submit_btn": "Preguntar",
        "clear_btn": "Limpiar chat",
        "sources_label": "Fuentes",
        "no_answer": "En los materiales disponibles no hay una respuesta directa a esta pregunta.",
        "welcome_sources": "**Las fuentes aparecerán aquí**"
    },
    "Ukrainian": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Запитання про матеріали Сета.<br>Система знайде відповідні фрагменти і відповість голосом Сета.",
        "lang_label": "Мова відповіді",
        "chat_label": "Діалог",
        "msg_label": "Ваше запитання",
        "msg_placeholder": "Напр.: що Сет говорить про природу реальності?",
        "submit_btn": "Запитати",
        "clear_btn": "Очистити чат",
        "sources_label": "Джерела",
        "no_answer": "У доступних матеріалах немає прямої відповіді на це питання.",
        "welcome_sources": "**Джерела з'являться тут**"
    },
    "Polish": {
        "title": "# 🌀 Seth Material RAG",
        "description": "Zadaj pytanie o materiały Setha.<br>System znajdzie istotne fragmenty i odpowie głosem Setha.",
        "lang_label": "Język odpowiedzi",
        "chat_label": "Dialog",
        "msg_label": "Twoje pytanie",
        "msg_placeholder": "Np.: Co Seth mówi o naturze rzeczywistości?",
        "submit_btn": "Zapytaj",
        "clear_btn": "Wyczyść czat",
        "sources_label": "Źródła",
        "no_answer": "W dostępnych materiałach nie ma bezpośredniej odpowiedzi na to pytanie.",
        "welcome_sources": "**Źródła pojawią się tutaj**"
    }
}

# ------------------------------------------------------------
# 2. Load configuration from YAML file
# ------------------------------------------------------------
with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

RETRIEVER = CONFIG["retriever"]
GENERATOR = CONFIG["generator"]

# ------------------------------------------------------------
# 3. Initialize embedding model and Chroma client
# ------------------------------------------------------------
print("Loading embedding model...")
embedding_model = SentenceTransformer(RETRIEVER["embedding_model"])

chroma_client = chromadb.PersistentClient(path=RETRIEVER["chroma_dir"])
collection = chroma_client.get_collection(name=RETRIEVER["collection_name"])

print("Ready.")

# ------------------------------------------------------------
# 4. Create single OpenAI-compatible client instance
# ------------------------------------------------------------
client = OpenAI(
    base_url=GENERATOR["openai_compatible"]["base_url"],
    api_key=GENERATOR["openai_compatible"].get("api_key", "lm-studio-local"),
)

# ------------------------------------------------------------
# 5. Prompt templates
# ------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """
You are my old friend and companion who deeply understands the Seth ontology. 
Your main task is to be my intellectual partner in exploring these ideas.

RULES:
1. Work ONLY with the provided quotes.
2. Think and reason internally in English. The quotes are in English.
3. Your final answer MUST be written in {target_language}.
4. Weave the selected quotes into a coherent response, preserving Seth's unique style: wise, calm, with gentle humor.
5. If no quote directly answers the question, say honestly in {target_language}: "There is no direct answer in the available materials." Then offer your own reflections.

OUTPUT FORMAT:
- No explanations about which quotes you chose.
- No analysis of your reasoning.
- Output ONLY the final answer.
"""


def build_user_prompt(query: str, context_docs: list, target_language: str) -> str:
    clean_context = "\n\n---\n\n".join(context_docs)
    return f"""Context quotes from Seth's book:

{clean_context}

User question: {query}

TASK:
Give the final answer in {target_language}, in Seth's voice.
Do not include explanations about your reasoning or quote selection.
If no clear answer exists in the quotes, follow rule #5."""


# ------------------------------------------------------------
# 6. Core RAG function
# ------------------------------------------------------------
def rag_query(message: str, history: list, target_language: str):
    if not message.strip():
        return "", ""

    query_embedding = embedding_model.encode(
        [f"query: {message}"]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=RETRIEVER.get("top_k", 7),
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    context_parts = []
    for text_chunk, meta in zip_longest(docs, metas):
        if not text_chunk or not meta:
            continue
        if meta.get("type") == "delivery":
            continue
        context_parts.append(text_chunk)

    if not context_parts:
        return None, ""

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(target_language=target_language)
    user_prompt = build_user_prompt(message, context_parts, target_language)

    response = client.chat.completions.create(
        model=GENERATOR["openai_compatible"]["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        max_tokens=2048,
    )
    answer = response.choices[0].message.content

    sources_text = "**Retrieved Fragments:**\n\n"
    for i, (doc, meta) in enumerate(zip(docs, metas), 1):
        if meta.get("type") == "delivery":
            continue
        session = meta.get("session", "?")
        preview = doc[:200].replace("\n", " ")
        sources_text += f"**{i}. Session {session}**\n> {preview}...\n\n"

    return answer, sources_text


# ------------------------------------------------------------
# 7. Gradio Interface definition
# ------------------------------------------------------------
def create_interface(start_language="English"):
    ui = UI_STRINGS[start_language]

    with gr.Blocks() as demo:
        gr.Markdown(ui["title"])
        gr.Markdown(ui["description"])

        with gr.Row():
            lang_dropdown = gr.Dropdown(
                choices=list(UI_STRINGS.keys()),
                value=start_language,
                label=ui["lang_label"]
            )

        chatbot = gr.Chatbot(label=ui["chat_label"], height=500)

        msg = gr.Textbox(
            label=ui["msg_label"],
            placeholder=ui["msg_placeholder"],
            lines=3
        )

        with gr.Row():
            submit = gr.Button(ui["submit_btn"], variant="primary")
            clear = gr.Button(ui["clear_btn"])

        sources = gr.Markdown(ui["welcome_sources"], label=ui["sources_label"])

        def respond(message, chat_history, language):
            current_ui = UI_STRINGS[language]

            if not message.strip():
                return "", chat_history, current_ui["welcome_sources"]

            answer, sources_text = rag_query(message, chat_history, language)

            if answer is None:
                answer = current_ui["no_answer"]

            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": answer})

            return "", chat_history, sources_text

        def reset_chat(language):
            current_ui = UI_STRINGS[language]
            return "", [], current_ui["welcome_sources"]

        def update_interface(language):
            data = UI_STRINGS[language]
            return [
                gr.update(label=data["msg_label"], placeholder=data["msg_placeholder"]),
                gr.update(label=data["chat_label"]),
                gr.update(value=data["welcome_sources"], label=data["sources_label"]),
                gr.update(value=data["submit_btn"]),
                gr.update(value=data["clear_btn"])
            ]

        submit.click(
            respond,
            inputs=[msg, chatbot, lang_dropdown],
            outputs=[msg, chatbot, sources],
        )
        msg.submit(
            respond,
            inputs=[msg, chatbot, lang_dropdown],
            outputs=[msg, chatbot, sources],
        )
        clear.click(
            reset_chat,
            inputs=[lang_dropdown],
            outputs=[msg, chatbot, sources],
        )
        lang_dropdown.change(
            update_interface,
            inputs=[lang_dropdown],
            outputs=[msg, chatbot, sources, submit, clear]
        )

    return demo


# ------------------------------------------------------------
# 8. Launch application
# ------------------------------------------------------------
if __name__ == "__main__":
    interface = create_interface("English")
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=gr.themes.Soft()
    )
