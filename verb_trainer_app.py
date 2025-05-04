
import streamlit as st
import random
import re

# === Setup ===
st.set_page_config(page_title="English Verb Trainer", page_icon="📚")
st.title("📚 English Verb Trainer")

# === Data ===
pronouns = ["I", "you", "we", "they", "he", "she", "it"]
forms_all = ["affirmative", "negative", "question"]

verbs_ordered = ["work", "talk", "call", "live", "play", "use", "watch", "move", "open", "close"]
verb_forms = {
    "work": ("worked", "worked"), "talk": ("talked", "talked"),
    "call": ("called", "called"), "live": ("lived", "lived"),
    "play": ("played", "played"), "use": ("used", "used"),
    "watch": ("watched", "watched"), "move": ("moved", "moved"),
    "open": ("opened", "opened"), "close": ("closed", "closed")
}

verb_constructions_all = [
    "Present Simple", "Past Simple", "Future Simple",
    "Present Continuous", "Past Continuous", "Future Continuous"
]

def capitalize_pronoun(p):
    return "I" if p.lower() == "i" else p.capitalize()

def make_ing(verb):
    if verb.endswith("ie"):
        return verb[:-2] + "ying"
    elif verb.endswith("e") and verb != "be":
        return verb[:-1] + "ing"
    elif len(verb) >= 3 and re.match(r".*[^aeiou][aeiou][^aeiou]$", verb) and verb[-1] not in "wxy":
        return verb + verb[-1] + "ing"
    else:
        return verb + "ing"

def get_aux(pronoun, tense):
    p = pronoun.lower()
    aux_map = {
        "Present Continuous": {"i": "am", "you": "are", "we": "are", "they": "are", "he": "is", "she": "is", "it": "is", "default": "are"},
        "Past Continuous": {"default": "was"},
        "Future Continuous": {"default": "will be"}
    }
    tense_map = aux_map.get(tense, {})
    return tense_map.get(p, tense_map.get("default", ""))

def construct(pronoun, verb, tense, form):
    p = capitalize_pronoun(pronoun)
    v_ing = make_ing(verb)
    past, _ = verb_forms[verb]
    aux = get_aux(pronoun, tense)

    if form == "affirmative":
        if tense == "Present Simple":
            return f"{p} {verb + 's' if pronoun in ['he','she','it'] else verb}"
        elif tense == "Past Simple":
            return f"{p} {past}"
        elif tense == "Future Simple":
            return f"{p} will {verb}"
        elif "Continuous" in tense:
            return f"{p} {aux} {v_ing}"
    return "ERROR"

# === UI ===
st.subheader("Choose your practice settings")
num_verbs = st.slider("How many verbs?", 1, len(verbs_ordered), 5)
selected_constructions = st.multiselect("Tenses:", verb_constructions_all, default=verb_constructions_all)
selected_forms = st.multiselect("Forms:", forms_all, default=forms_all)

if st.button("Generate Task"):
    pronoun = random.choice(pronouns)
    verb = random.choice(verbs_ordered[:num_verbs])
    tense = random.choice(selected_constructions)
    form = random.choice(selected_forms)
    task = f"{capitalize_pronoun(pronoun)}, {verb}, {tense}, {form}"
    st.session_state.task = task
    st.session_state.answer = construct(pronoun, verb, tense, form)

if "task" in st.session_state:
    st.markdown(f"### Task: {st.session_state.task}")
    user_input = st.text_input("Your answer:")
    if user_input:
        correct = st.session_state.answer
        if user_input.strip().lower().rstrip(".!?") == correct.lower():
            st.success("✅ Well done!")
        else:
            st.error(f"❌ Correct answer: {correct}")
