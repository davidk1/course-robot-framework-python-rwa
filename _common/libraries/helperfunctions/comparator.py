from deepdiff import DeepDiff


def compare_results(actual, expected, exclude_paths=None):
    """Metoda vraci vysledek komparace dvou objektu jako python slovnik.

    :param actual: aktualni objekt [jakykoliv python objekt]
    :param expected: ocekavany objekt [jakykoliv python objekt]
    :param exclude_paths: mnozina prvku objektu, ktere nebudou zahrnuty do porovnani
    :return: vraci python slovnik, kde klic 'bool' predstavuje vysledek porovnani (True = Pass / False = Fail) a
    klic 'detail' vraci slovnik s detaily porovnani obou objektu (prazdny slovnik znamena, ze jsou aktualni a
    ocekavane objekty totozne"
    """
    result = DeepDiff(actual, expected, exclude_paths=exclude_paths)
    return {'bool': result == {}, 'detail': result}
