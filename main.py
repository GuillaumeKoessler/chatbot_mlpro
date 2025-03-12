from api import chat_openai_langchain as co

print(
    co.transf_phrase_vers(
        "Depuis le temps que nous partageons notre amour sans aucun nuage, je me suis rendu compte à quel point tu comptais pour moi. C'est à tes côtés que je veux construire ma vie, que nous avancions main dans la main."
    )
)
