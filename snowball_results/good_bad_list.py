GOODLIST = [
        #"motion detect",
        #"smoke detector"
        ]

BADLIST = [
        # device detector terms/terms victims would use
        #"find", "detect", "spot", "abusive", "abuser",
        #"block", "confuse", "destroy", "sniffer", "scan",

        # spyware terms
        "app", "apk",
        "instagram", "facebook", "whatsapp", "reddit",
        "text messages", "texts", "messages", "computer",
        "calls", "social media", "messenger", "icloud",
        "pinterest", "laptop", "call history", "hack",
        "tiktok", "snapchat", "roblox", "ipad", "google",
        "spyware", "software","online", "windows",

        # phone terms
        #"android", "ios",
        #" phone",
        #"iphone",

        # asking for adivce
        "illegal", "wrong", "cheat on my", "caught",
        "why", "what", "should", 
        #"through",
        "can my",
        "can someone", "can employer", "legal", "against the law",
        "will", "can i", "cheat again",

        # names of internet influencers
        "gary", 
        #"tim", 
        "morgz",

        # programming frameworks
        "jest", "jasmine",

        #"ex" words, probably don't need all of these now
        "expenses", "express", "excavator", "experience",
        "excel", "export", "expunged", "fedex", "aliexpress",
        "examplify",

        # irrelevant terms
        "novel", "netflix", "fortnite", "fun", "mood",
        "period", "visa", "netflix", "influencer", "get over",
        "snoring", "job interview", "henry viii", "wattpad",
        "fanfic", "twitch", "secret agent", "partner track",
        "wife of a spy", "movie", "meme", "drama", "song",
        "lyrics", "pdf", "south park", "joker", "cast", "storage",
        "sang", "wrote", "ww2", "toddler", "mercury",
        "vinyl", "holder", "alexa", "palin", "stab",
        "music", "putin", "putri", "pants", "rivera", "url",
        "partnership", "belongings", "joke", "buyout","diss track",
        "sponsorship", "ring ideas", "chapter", "read", "download",
        "webtoon", "superhero", "storm", "step tracker", "boss",
        "neighbor", "disney", "gta 5", "proposes", "lego", "carmax",
        "dealership", "record record", "ideas", "record player",
        "world record", "record label", "record store", "satta",
        "implant", "royalty", "autobiographical", "track records",
        "exam", "lens", "siriusxm", "vin", "carfax", "car history",
        "child support", "medaria arradondo", "spies", "cps", "activity",
        "usage", "thieves", "elden ring", "package", "shipment",
        "audiobook","race track","race car",
        "parcel", "other parent", "visitation", "kids","bed bug","gold bug",
        #"truck",
        "track wire",
        "turn on", "turn off", "karmann ghia", "tell", "selina gomez",
        "justin bieber","verizon",

        # other 'tracking' things
        "credit card", "social security", "pension", "issue",
        #"card",
        "claim", "debt", "insurance", "tax",


        # ONLY FOR DETECTOR SNOWBALL
        "key finder",
        ]


def passes_badlist(q):
    for word in BADLIST:
        if word in q:
            return (False, word)

    return (True, None)

def passes_goodlist(q):
    for word in GOODLIST:
        if word in q:
            return (True, word)

    return (False, None)
