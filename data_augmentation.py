from deep_translator import GoogleTranslator

def back_translate(text: str, source_lang: str = "fr", target_lang: str = "en") -> str:
    """
    Réalise une back translation (Aller-Retour).
    """
    try:
        # Traduction Aller
        translator_forward = GoogleTranslator(source=source_lang, target=target_lang)
        intermediate_text = translator_forward.translate(text)
        
        # Traduction Retour
        translator_backward = GoogleTranslator(source=target_lang, target=source_lang)
        final_text = translator_backward.translate(intermediate_text)
        
        return final_text
    except Exception as e:
        print(f"Erreur lors de la traduction : {e}")
        return text

