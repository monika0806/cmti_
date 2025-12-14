def correct_text(text: str) -> str:
    """
    Applies basic spell correction and cleanup.
    """

    from symspellpy import SymSpell, Verbosity  # lazy import
    import pkg_resources

    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    dictionary_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt"
    )

    sym_spell.load_dictionary(dictionary_path, 0, 1)

    corrected_words = []

    for word in text.split():
        suggestions = sym_spell.lookup(
            word,
            Verbosity.CLOSEST,
            max_edit_distance=2
        )
        if suggestions:
            corrected_words.append(suggestions[0].term)
        else:
            corrected_words.append(word)

    return " ".join(corrected_words)