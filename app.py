import streamlit as st

st.set_page_config(
    page_title="Détection des erreurs de coordination",
    layout="wide"
)

# ----------------- Données de démonstration -----------------
DEMO_TEXTE_DETECTE = """Le métier de mineur n'est pas sans danger il est très dur physiquement, fatigant il faut supporter la poussière et la chaleur.
***Il y a dans votre phrase plusieurs éléments qui sont coordonnés les uns aux autres (à l'aide d'un mot comme "mais", "ou", "et", "car", "or", d'une formule comme "ainsi que", ou en étant simplement juxtaposés). Pour améliorer la qualité rédactionnelle de votre écrit, il semble que cette coordination mérite d'être revue.***
***Essayer de vérifier la ponctuation (présence ou absence de virgule, de point-virgule, de deux-points ou de point) : il est possible qu'il y ait un problème à ce niveau.***
***Essayer de vérifier la façon dont ces éléments se rattachent les uns aux autres : il semble que l'un d'entre eux soit mal rattaché, ou au moins que l'on ait du mal à choisir entre plusieurs rattachements possibles.

----------------------------------------------------------------------------------------------------
Pour notre projet, nous avons appris à élaborer un protocole et le suivre de façon précise.

***Essayer de vérifier la façon dont ces éléments se rattachent les uns aux autres : il semble que l'un d'entre eux soit mal rattaché, ou au moins que l'on ait du mal à choisir entre plusieurs rattachements possibles.
----------------------------------------------------------------------------------------------------

C'est un moyen efficace pour suivre le planning établi et de connaitre l'avancée du projet en temps réel.
***Il y a dans votre phrase plusieurs éléments qui sont coordonnés les uns aux autres (à l'aide d'un mot comme "mais", "ou", "et", "car", "or", d'une formule comme "ainsi que", ou en étant simplement juxtaposés). Pour améliorer la qualité rédactionnelle de votre écrit, il semble que cette coordination mérite d'être revue.***
***Essayer de vérifier la nature des éléments coordonnés : il semble qu'ils soient trop hétérogènes, sur le plan de la forme voire du contenu.***
""".strip()


# ----------------- Traitement pour l'affichage -----------------
def parser_rapport(texte: str):
    blocs = []
    phrase = None
    messages = []

    def ajouter_bloc():
        nonlocal phrase, messages
        if phrase:
            blocs.append({"phrase": phrase, "messages": messages})
        phrase = None
        messages = []

    for ligne in texte.splitlines():
        s = ligne.strip()
        if not s:
            continue
        if set(s) == {"-"}:
            ajouter_bloc()
            continue
        if s.startswith("***"):
            messages.append(s.strip("*").strip())
        else:
            if phrase is not None:
                ajouter_bloc()
            phrase = s

    ajouter_bloc()
    return blocs


def extraire_original(texte: str) -> str:
    lignes = []
    for ligne in texte.splitlines():
        s = ligne.strip()
        if not s:
            continue
        if s.startswith("***"):
            continue
        if set(s) == {"-"}:
            continue
        lignes.append(s)
    return "\n\n".join(lignes)


# ----------------- Interface -----------------
st.title("Détection automatique des erreurs de coordination")
st.caption("Démonstration de l’interface – aucune analyse réelle n’est effectuée")

st.file_uploader(
    "Importer un fichier (PDF ou TXT)",
    type=["pdf", "txt"],
    help="Dans cette démonstration, le fichier importé n’est pas analysé."
)

rapport = DEMO_TEXTE_DETECTE
blocs = parser_rapport(rapport)
original = extraire_original(rapport)

tab1, tab2 = st.tabs(["Détecté", "Original"])

with tab1:
    st.subheader("Résultat de la détection")

    for i, bloc in enumerate(blocs, start=1):
        with st.container(border=True):
            st.markdown(f"**Phrase {i}**")
            st.write(bloc["phrase"])

            if bloc["messages"]:
                st.markdown("**Observations**")
                for msg in bloc["messages"]:
                    st.warning(msg)
            else:
                st.info("Aucune observation pour cette phrase.")

    st.divider()
    st.text_area(
        "Rapport complet (version texte)",
        value=rapport,
        height=220
    )

with tab2:
    st.subheader("Phrases originales")
    st.markdown("Texte sans commentaires ni messages d’erreur.")
    st.text_area(
        "Texte original",
        value=original,
        height=420
    )

st.download_button(
    label="⬇️ Télécharger le rapport",
    data=rapport.encode("utf-8"),
    file_name="rapport_coordination_demo.txt",
    mime="text/plain",
)
