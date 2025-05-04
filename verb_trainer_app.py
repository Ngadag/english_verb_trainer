
import streamlit as st
import random
import re

st.set_page_config(page_title="English Verb Trainer", page_icon="📚")
st.title("📚 English Verb Trainer")

# === Data ===
pronouns = ["I", "you", "we", "they", "he", "she", "it"]
forms_all = ["affirmative", "negative", "question"]

excluded_verbs = {"like", "love", "need", "be", "know", "want", "mean", "believe",
                  "understand", "remember", "can", "would", "may", "should", "will"}

verbs_ordered = [
    verb for verb in [
        "work", "talk", "call", "live", "play", "use", "watch", "move", "open",
        "close", "stay", "clean", "cook", "help", "laugh", "look", "start", "turn",
        "have", "do", "say", "go", "get", "make", "think", "take", "see", "come",
        "find", "give", "tell", "feel", "become", "leave", "put", "keep", "let", "begin",
        "seem", "show", "hear", "run", "bring", "happen", "write", "provide", "sit", "stand",
        "lose", "pay", "meet", "include", "continue", "set", "learn", "change", "lead",
        "follow", "stop", "create", "speak", "read", "allow", "add", "spend", "grow",
        "walk", "win", "offer", "ask", "try"
    ] if verb not in excluded_verbs
]

verb_forms = {v: (v + "ed", v + "ed") for v in verbs_ordered}
verb_forms.update({
    "have": ("had", "had"), "do": ("did", "done"), "say": ("said", "said"),
    "go": ("went", "gone"), "get": ("got", "gotten"), "make": ("made", "made"),
    "think": ("thought", "thought"), "take": ("took", "taken"), "see": ("saw", "seen"),
    "come": ("came", "come"), "find": ("found", "found"), "give": ("gave", "given"),
    "tell": ("told", "told"), "feel": ("felt", "felt"), "become": ("became", "become"),
    "leave": ("left", "left"), "put": ("put", "put"), "keep": ("kept", "kept"),
    "let": ("let", "let"), "begin": ("began", "begun"), "show": ("showed", "shown"),
    "hear": ("heard", "heard"), "run": ("ran", "run"), "bring": ("brought", "brought"),
    "write": ("wrote", "written"), "sit": ("sat", "sat"), "stand": ("stood", "stood"),
    "lose": ("lost", "lost"), "pay": ("paid", "paid"), "meet": ("met", "met"),
    "lead": ("led", "led"), "read": ("read", "read"), "spend": ("spent", "spent"),
    "grow": ("grew", "grown"), "win": ("won", "won"), "speak": ("spoke", "spoken")
})

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
    past, past_part = verb_forms.get(verb, (verb + "ed", verb + "ed"))
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

    if form == "negative":
        if tense == "Present Simple":
            return f"{p} {'doesn’t' if pronoun in ['he','she','it'] else 'don’t'} {verb}"
        elif tense == "Past Simple":
            return f"{p} didn’t {verb}"
        elif tense == "Future Simple":
            return f"{p} will not {verb}"
        elif "Continuous" in tense:
            return f"{p} {aux.split()[0]} not {' '.join(aux.split()[1:])} {v_ing}" if " " in aux else f"{p} {aux} not {v_ing}"

    if form == "question":
        if tense == "Present Simple":
            return f"{'Does' if pronoun in ['he','she','it'] else 'Do'} {p} {verb}?"
        elif tense == "Past Simple":
            return f"Did {p} {verb}?"
        elif tense == "Future Simple":
            return f"Will {p} {verb}?"
        elif "Continuous" in tense:
            return f"{aux.split()[0].capitalize()} {p} {' '.join(aux.split()[1:])} {v_ing}?" if " " in aux else f"{aux.capitalize()} {p} {v_ing}?"

    return "ERROR"

# === UI ===
st.subheader("Choose your practice settings")
num_verbs = st.slider("How many verbs?", 1, len(verbs_ordered), 10)
selected_constructions = st.multiselect("Tenses:", verb_constructions_all, default=verb_constructions_all)
selected_forms = st.multiselect("Forms:", forms_all, default=forms_all)

if st.button("Generate Task"):
    pronoun = random.choice(pronouns)
    verb = random.choice(verbs_ordered[:num_verbs])
    tense = random.choice(selected_constructions)
    form = random.choice(selected_forms)
    task = f"{capitalize_pronoun(pronoun)}, {verb}, {tense}, {form}"
    st.session_state.task = (pronoun, verb, tense, form)
    st.session_state.answer = construct(pronoun, verb, tense, form)

if "task" in st.session_state:
    pronoun, verb, tense, form = st.session_state.task
    st.markdown(f"### Task: {capitalize_pronoun(pronoun)}, *{verb}*, {tense}, {form.capitalize()}")
    user_input = st.text_input("Your answer:")
    if user_input:
        def normalize(text):
            return " ".join(text.strip().rstrip(".!?").split()).lower()
        if normalize(user_input) == normalize(st.session_state.answer):
            st.success("✅ Well done!")
        else:
            st.error(f"❌ Correct answer: {st.session_state.answer}")
