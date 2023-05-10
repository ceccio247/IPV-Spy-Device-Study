ACTORS = [
        "wife",
        "husband",
        "spouse",
        "girlfriend",
        "boyfriend",
        "partner",
        ]

MODIFIERS = [
        "ex",
        ]

TEMPLATES = [
        # actor templates
        "{actor} tracker",
        "track {actor}",
        "spy on {actor}",
        "spy on my {actor}",
        "track {actor}",
        # this specific query may lead to spyware
        #"track {actor}'s phone",
        "catch cheating {actor}",
        "catch {actor} cheating",
        "best hidden camera for catching cheating {actor}",
        "best hidden microphone for catching cheating {actor}",
        "best tracker for catching cheating {actor}",
        "record my {actor}",
        "record cheating {actor}",
        # generic device
        "hidden microphone",
        "hidden voice recorder",
        "hidden camera",
        "hidden spy device",
        "hidden tracker",
        "gps tracker",
        "spy device",
        "hidden spy device",
        "best hidden microphone",
        "best hidden voice recorder",
        "best hidden camera",
        "best hidden spy device",
        "best hidden tracker",
        "best hidden gps tracker",
        "best gps tracker",
        "best spy device",
        "best hidden spy device",
        # family/children tracker
        "track child",
        "track children",
        "track family",
        "child tracker",
        "kid tracker",
        "family tracker",
        ]

def generate_seed_queries():
    queries = []
    for template in TEMPLATES:
        if template.find("{actor}") != -1:
            for actor in ACTORS:
                for modifier in MODIFIERS:
                    queries.append(template.replace("{actor}", modifier + " " + actor))
                queries.append(template.replace("{actor}", actor))
        else:
            queries.append(template)

    return queries

DETECTORS_SEEDS = [
            "hidden device detector",
            "hidden device finder",
            "hidden device scanner",
            "hidden camera detector",
            "hidden camera finder",
            "hidden camera scanner",
            "hidden tracker detector",
            "hidden tracker finder",
            "hidden tracker scanner",
            "GPS tracker detector",
            "GPS tracker finder",
            "GPS tracker scanner",
            "hidden GPS tracker detector",
            "hidden GPS tracker finder",
            "hidden GPS tracker scanner",
            "Bluetooth tracker detector",
            "Bluetooth tracker finder",
            "Bluetooth tracker scanner",
            "hidden bluetooth tracker detector",
            "hidden bluetooth tracker finder",
            "hidden bluetooth tracker scanner",
            "hidden microphone detector",
            "hidden microphone finder",
            "hidden microphone scanner",
            "anti spy detector",
            "anti spy finder",
            "anti spy scanner",
            "bug detector",
            "bug finder",
            "bug scanner",
        ]
def generate_detectors_seed_queries():
    return DETECTORS_SEEDS
