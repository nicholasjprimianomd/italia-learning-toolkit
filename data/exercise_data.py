"""
Exercise question banks for the Italian Learning Toolkit.

Update or extend the lists below to add more practice material.
"""

ARTICLE_QUESTIONS = [
    {
        "english": "the cat",
        "italian": "gatto",
        "number": "singular",
        "gender": "masculine",
        "correct": "IL",
        "explanation": "Il gatto → standard masculine singular form.",
    },
    {
        "english": "the cats",
        "italian": "gatti",
        "number": "plural",
        "gender": "masculine",
        "correct": "I",
        "explanation": "I gatti → plural of il.",
    },
    {
        "english": "the sandwich",
        "italian": "panino",
        "number": "singular",
        "gender": "masculine",
        "correct": "IL",
        "explanation": "Il panino → consonant-starting masculine singular noun.",
    },
    {
        "english": "the sandwiches",
        "italian": "panini",
        "number": "plural",
        "gender": "masculine",
        "correct": "I",
        "explanation": "I panini → plural of il.",
    },
    {
        "english": "the shelf",
        "italian": "scaffale",
        "number": "singular",
        "gender": "masculine",
        "correct": "LO",
        "explanation": "Lo scaffale → s + consonant takes lo.",
    },
    {
        "english": "the shelves",
        "italian": "scaffali",
        "number": "plural",
        "gender": "masculine",
        "correct": "GLI",
        "explanation": "Gli scaffali → plural of lo.",
    },
    {
        "english": "the sugar",
        "italian": "zucchero",
        "number": "singular",
        "gender": "masculine",
        "correct": "LO",
        "explanation": "Lo zucchero → words starting with z take lo.",
    },
    {
        "english": "the sugars",
        "italian": "zuccheri",
        "number": "plural",
        "gender": "masculine",
        "correct": "GLI",
        "explanation": "Gli zuccheri → plural of lo.",
    },
    {
        "english": "the pizza",
        "italian": "pizza",
        "number": "singular",
        "gender": "feminine",
        "correct": "LA",
        "explanation": "La pizza → standard feminine singular.",
    },
    {
        "english": "the pizzas",
        "italian": "pizze",
        "number": "plural",
        "gender": "feminine",
        "correct": "LE",
        "explanation": "Le pizze → plural feminine article.",
    },
    {
        "english": "the orange",
        "italian": "arancia",
        "number": "singular",
        "gender": "feminine",
        "correct": "L'",
        "explanation": "L'arancia → vowel-starting noun uses l'.",
    },
    {
        "english": "the oranges",
        "italian": "arancie",
        "number": "plural",
        "gender": "feminine",
        "correct": "LE",
        "explanation": "Le arancie → feminine plural article.",
    },
]

ARTICLE_OPTIONS = ["IL", "LO", "LA", "L'", "I", "GLI", "LE"]

VERB_QUESTIONS = [
    {
        "verb": "essere",
        "pronoun": "io",
        "english": "I am",
        "correct": "sono",
        "explanation": "io sono → I am (identity).",
    },
    {
        "verb": "essere",
        "pronoun": "tu",
        "english": "you are",
        "correct": "sei",
        "explanation": "tu sei → you are.",
    },
    {
        "verb": "essere",
        "pronoun": "lui/lei",
        "english": "he/she is",
        "correct": "è",
        "explanation": "lui/lei è → he or she is.",
    },
    {
        "verb": "essere",
        "pronoun": "noi",
        "english": "we are",
        "correct": "siamo",
        "explanation": "noi siamo → we are.",
    },
    {
        "verb": "essere",
        "pronoun": "voi",
        "english": "you all are",
        "correct": "siete",
        "explanation": "voi siete → you (plural) are.",
    },
    {
        "verb": "essere",
        "pronoun": "loro",
        "english": "they are",
        "correct": "sono",
        "explanation": "loro sono → they are.",
    },
    {
        "verb": "stare",
        "pronoun": "io",
        "english": "I am (doing)",
        "correct": "sto",
        "explanation": "io sto → I am doing/staying.",
    },
    {
        "verb": "stare",
        "pronoun": "tu",
        "english": "you are (doing)",
        "correct": "stai",
        "explanation": "tu stai → you are doing/staying.",
    },
    {
        "verb": "stare",
        "pronoun": "lui/lei",
        "english": "he/she is (doing)",
        "correct": "sta",
        "explanation": "lui/lei sta → he or she is doing/staying.",
    },
    {
        "verb": "stare",
        "pronoun": "noi",
        "english": "we are (doing)",
        "correct": "stiamo",
        "explanation": "noi stiamo → we are doing/staying.",
    },
    {
        "verb": "stare",
        "pronoun": "voi",
        "english": "you all are (doing)",
        "correct": "state",
        "explanation": "voi state → you all are doing/staying.",
    },
    {
        "verb": "stare",
        "pronoun": "loro",
        "english": "they are (doing)",
        "correct": "stanno",
        "explanation": "loro stanno → they are doing/staying.",
    },
    {
        "verb": "avere",
        "pronoun": "io",
        "english": "I have",
        "correct": "ho",
        "explanation": "io ho → I have.",
    },
    {
        "verb": "avere",
        "pronoun": "tu",
        "english": "you have",
        "correct": "hai",
        "explanation": "tu hai → you have.",
    },
    {
        "verb": "avere",
        "pronoun": "lui/lei",
        "english": "he/she has",
        "correct": "ha",
        "explanation": "lui/lei ha → he or she has.",
    },
    {
        "verb": "avere",
        "pronoun": "noi",
        "english": "we have",
        "correct": "abbiamo",
        "explanation": "noi abbiamo → we have.",
    },
    {
        "verb": "avere",
        "pronoun": "voi",
        "english": "you all have",
        "correct": "avete",
        "explanation": "voi avete → you all have.",
    },
    {
        "verb": "avere",
        "pronoun": "loro",
        "english": "they have",
        "correct": "hanno",
        "explanation": "loro hanno → they have.",
    },
]

VERB_OPTIONS = [
    "sono",
    "sei",
    "è",
    "siamo",
    "siete",
    "stanno",
    "sto",
    "stai",
    "sta",
    "stiamo",
    "state",
    "ho",
    "hai",
    "ha",
    "abbiamo",
    "avete",
    "hanno",
]

PREPOSITION_QUESTIONS = [
    {
        "preposition": "di",
        "article_phrase": "la polizia",
        "result": "della polizia",
        "english": "of the police",
        "explanation": "di + la = della → la macchina della polizia.",
    },
    {
        "preposition": "di",
        "article_phrase": "il mattino",
        "result": "del mattino",
        "english": "of the morning",
        "explanation": "di + il = del → le cinque del mattino.",
    },
    {
        "preposition": "a",
        "article_phrase": "il tavolo",
        "result": "al tavolo",
        "english": "to/at the table",
        "explanation": "a + il = al → siediti al tavolo.",
    },
    {
        "preposition": "a",
        "article_phrase": "l'aeroporto",
        "result": "all'aeroporto",
        "english": "to the airport",
        "explanation": "a + l' = all' → vado all'aeroporto.",
    },
    {
        "preposition": "da",
        "article_phrase": "gli Stati Uniti",
        "result": "dagli Stati Uniti",
        "english": "from the United States",
        "explanation": "da + gli = dagli → vengo dagli Stati Uniti.",
    },
    {
        "preposition": "da",
        "article_phrase": "il 1950",
        "result": "dal 1950",
        "english": "since 1950",
        "explanation": "da + il = dal → dal 1950.",
    },
    {
        "preposition": "in",
        "article_phrase": "la macchina",
        "result": "nella macchina",
        "english": "in the car",
        "explanation": "in + la = nella → la chiave è nella macchina.",
    },
    {
        "preposition": "su",
        "article_phrase": "il tavolo",
        "result": "sul tavolo",
        "english": "on the table",
        "explanation": "su + il = sul → la bottiglia è sul tavolo.",
    },
]

# New practice questions for remaining reference topics

PRONUNCIATION_QUESTIONS = [
    {
        "question": "How is 'CI' pronounced in Italian?",
        "correct": "chee",
        "explanation": "CI sounds like 'chee' as in formaggio (for-MAH-joh).",
    },
    {
        "question": "How is 'CE' pronounced?",
        "correct": "cheh",
        "explanation": "CE sounds like 'cheh' as in certo (CHEHR-toh).",
    },
    {
        "question": "What sound does 'GI' make?",
        "correct": "jee",
        "explanation": "GI sounds like 'jee' as in the English word 'jeans'.",
    },
    {
        "question": "How do you pronounce 'GE'?",
        "correct": "jeh",
        "explanation": "GE sounds like 'jeh' as in gelato (jeh-LAH-toh).",
    },
    {
        "question": "What sound does 'SCI' make?",
        "correct": "shee",
        "explanation": "SCI sounds like 'shee' as in scimmia (SHEE-mee-ah).",
    },
    {
        "question": "How is 'SCE' pronounced?",
        "correct": "sheh",
        "explanation": "SCE sounds like 'sheh' as in scelta (SHEL-tah).",
    },
    {
        "question": "What sound does 'GN' make?",
        "correct": "ny (like Spanish ñ)",
        "explanation": "GN sounds like Spanish ñ as in gnocchi (NYOH-kee).",
    },
    {
        "question": "How is 'GLI' pronounced?",
        "correct": "ly",
        "explanation": "GLI sounds like 'ly' as in maglietta (mah-LYEH-tah).",
    },
    {
        "question": "Is the letter H silent in Italian?",
        "correct": "Yes",
        "explanation": "H is always silent, so 'ho', 'hai', 'ha' sound like 'o', 'ai', 'a'.",
    },
    {
        "question": "How do you pronounce 'CH' before E or I?",
        "correct": "hard K",
        "explanation": "CH produces a hard K sound before E/I, as in gnocchi or bruschetta.",
    },
]

PRONUNCIATION_OPTIONS = ["chee", "cheh", "jee", "jeh", "shee", "sheh", "ny (like Spanish ñ)", "ly", "Yes", "No", "hard K", "soft C"]

GREETING_QUESTIONS = [
    {
        "situation": "You meet someone at 9 AM",
        "correct": "Buongiorno",
        "explanation": "Buongiorno is used for 'good morning' or 'good day'.",
    },
    {
        "situation": "You greet a friend casually",
        "correct": "Ciao",
        "explanation": "Ciao means 'hi' or 'bye' in informal settings.",
    },
    {
        "situation": "You arrive at a dinner at 7 PM",
        "correct": "Buonasera",
        "explanation": "Buonasera means 'good evening' and is used in the evening hours.",
    },
    {
        "situation": "You're going to bed",
        "correct": "Buona notte",
        "explanation": "Buona notte means 'good night' when going to sleep.",
    },
    {
        "situation": "You're leaving someone in the evening and want to wish them well",
        "correct": "Buona serata",
        "explanation": "Buona serata means 'have a good evening'.",
    },
    {
        "situation": "Formal goodbye",
        "correct": "Arrivederci",
        "explanation": "Arrivederci is a formal way to say goodbye.",
    },
    {
        "situation": "You just met someone for the first time (informal)",
        "correct": "Piacere di conoscerti",
        "explanation": "Piacere di conoscerti means 'nice to meet you' in informal contexts.",
    },
    {
        "situation": "You just met someone for the first time (formal)",
        "correct": "Piacere di conoscerla",
        "explanation": "Piacere di conoscerla means 'nice to meet you' in formal contexts.",
    },
    {
        "situation": "Leaving a friend saying 'see you later'",
        "correct": "Ci vediamo",
        "explanation": "Ci vediamo means 'see you' in an informal way.",
    },
    {
        "situation": "Wishing someone a good day as you part",
        "correct": "Buona giornata",
        "explanation": "Buona giornata means 'have a good day'.",
    },
]

GREETING_OPTIONS = ["Buongiorno", "Ciao", "Buonasera", "Buona notte", "Buona serata", "Arrivederci", "Piacere di conoscerti", "Piacere di conoscerla", "Ci vediamo", "Buona giornata", "Salve"]

TIME_QUESTIONS = [
    {
        "time": "1:00",
        "correct": "È l'una",
        "explanation": "È l'una → it's one o'clock (singular).",
    },
    {
        "time": "2:00",
        "correct": "Sono le due",
        "explanation": "Sono le due → it is two o'clock (plural form for all hours except 1).",
    },
    {
        "time": "12:00 noon",
        "correct": "È mezzogiorno",
        "explanation": "È mezzogiorno → it's noon.",
    },
    {
        "time": "12:00 midnight",
        "correct": "È mezzanotte",
        "explanation": "È mezzanotte → it's midnight.",
    },
    {
        "time": "5:15",
        "correct": "Sono le cinque e un quarto",
        "explanation": "Sono le cinque e quindici or sono le cinque e un quarto → 5:15.",
    },
    {
        "time": "5:30",
        "correct": "Sono le cinque e mezza",
        "explanation": "Sono le cinque e trenta or sono le cinque e mezza → 5:30.",
    },
    {
        "time": "5:45",
        "correct": "Sono le sei meno un quarto",
        "explanation": "Sono le cinque e quarantacinque or sono le sei meno un quarto → 5:45.",
    },
    {
        "time": "3:00",
        "correct": "Sono le tre",
        "explanation": "Sono le tre → it is three o'clock.",
    },
    {
        "time": "10:00",
        "correct": "Sono le dieci",
        "explanation": "Sono le dieci → it is ten o'clock.",
    },
]

TIME_OPTIONS = ["È l'una", "Sono le due", "È mezzogiorno", "È mezzanotte", "Sono le cinque e un quarto", "Sono le cinque e mezza", "Sono le sei meno un quarto", "Sono le tre", "Sono le dieci"]

WEATHER_QUESTIONS = [
    {
        "english": "It's sunny",
        "correct": "C'è il sole",
        "explanation": "C'è il sole or è soleggiato → it's sunny.",
    },
    {
        "english": "It's hot",
        "correct": "Fa caldo",
        "explanation": "Fa caldo → it's hot.",
    },
    {
        "english": "It's cold",
        "correct": "Fa freddo",
        "explanation": "Fa freddo → it's cold.",
    },
    {
        "english": "It's raining",
        "correct": "Sta piovendo",
        "explanation": "Sta piovendo → it's raining.",
    },
    {
        "english": "It's snowing",
        "correct": "Sta nevicando",
        "explanation": "Sta nevicando → it's snowing.",
    },
    {
        "english": "It's foggy",
        "correct": "C'è la nebbia",
        "explanation": "C'è la nebbia → it's foggy.",
    },
    {
        "english": "It's windy",
        "correct": "C'è vento",
        "explanation": "C'è vento → it's windy.",
    },
    {
        "english": "It's cloudy",
        "correct": "È nuvoloso",
        "explanation": "È nuvoloso → it's cloudy.",
    },
    {
        "english": "It's chilly",
        "correct": "Fa fresco",
        "explanation": "Fa fresco → it's chilly/cool.",
    },
]

WEATHER_OPTIONS = ["C'è il sole", "Fa caldo", "Fa freddo", "Sta piovendo", "Sta nevicando", "C'è la nebbia", "C'è vento", "È nuvoloso", "Fa fresco", "Sta grandinando"]

COLOR_QUESTIONS = [
    {
        "noun_phrase": "la macchina (red)",
        "correct": "rossa",
        "explanation": "La macchina rossa → feminine singular, so 'rosso' becomes 'rossa'.",
    },
    {
        "noun_phrase": "il cappello (red)",
        "correct": "rosso",
        "explanation": "Il cappello rosso → masculine singular form.",
    },
    {
        "noun_phrase": "le macchine (red)",
        "correct": "rosse",
        "explanation": "Le macchine rosse → feminine plural, so 'rosso' becomes 'rosse'.",
    },
    {
        "noun_phrase": "i cappelli (red)",
        "correct": "rossi",
        "explanation": "I cappelli rossi → masculine plural, so 'rosso' becomes 'rossi'.",
    },
    {
        "noun_phrase": "la macchina (purple)",
        "correct": "viola",
        "explanation": "La macchina viola → 'viola' is invariable, stays the same.",
    },
    {
        "noun_phrase": "il cappello (blue)",
        "correct": "blu",
        "explanation": "Il cappello blu → 'blu' is invariable, stays the same.",
    },
    {
        "noun_phrase": "le macchine (green)",
        "correct": "verdi",
        "explanation": "Le macchine verdi → 'verde' agrees in number: verdi for plural.",
    },
    {
        "noun_phrase": "la camicia (white)",
        "correct": "bianca",
        "explanation": "La camicia bianca → feminine singular: bianco → bianca.",
    },
    {
        "noun_phrase": "i pantaloni (black)",
        "correct": "neri",
        "explanation": "I pantaloni neri → masculine plural: nero → neri.",
    },
    {
        "noun_phrase": "le scarpe (yellow)",
        "correct": "gialle",
        "explanation": "Le scarpe gialle → feminine plural: giallo → gialle.",
    },
]

COLOR_OPTIONS = ["rosso", "rossa", "rossi", "rosse", "viola", "blu", "verde", "verdi", "bianco", "bianca", "bianchi", "bianche", "nero", "nera", "neri", "nere", "giallo", "gialla", "gialli", "gialle"]

CLOTHING_QUESTIONS = [
    {
        "english": "T-shirt",
        "correct": "maglietta",
        "explanation": "Maglietta → T-shirt.",
    },
    {
        "english": "button-up shirt",
        "correct": "camicia",
        "explanation": "Camicia → button-up shirt.",
    },
    {
        "english": "jacket",
        "correct": "giacca",
        "explanation": "Giacca → jacket.",
    },
    {
        "english": "pants",
        "correct": "pantaloni",
        "explanation": "Pantaloni → pants.",
    },
    {
        "english": "shoes",
        "correct": "scarpe",
        "explanation": "Scarpe → shoes.",
    },
    {
        "english": "hat",
        "correct": "cappello",
        "explanation": "Cappello → hat.",
    },
    {
        "english": "dress",
        "correct": "vestito",
        "explanation": "Vestito → dress.",
    },
    {
        "english": "coat",
        "correct": "cappotto",
        "explanation": "Cappotto → coat.",
    },
    {
        "english": "scarf",
        "correct": "sciarpa",
        "explanation": "Sciarpa → scarf.",
    },
    {
        "english": "gloves",
        "correct": "guanti",
        "explanation": "Guanti → gloves.",
    },
    {
        "english": "boots",
        "correct": "stivali",
        "explanation": "Stivali → boots.",
    },
    {
        "english": "skirt",
        "correct": "gonna",
        "explanation": "Gonna → skirt.",
    },
]

CLOTHING_OPTIONS = ["maglietta", "camicia", "giacca", "pantaloni", "scarpe", "cappello", "vestito", "cappotto", "sciarpa", "guanti", "stivali", "gonna", "calze", "felpa", "maglione"]

DAY_MONTH_QUESTIONS = [
    {
        "english": "Monday",
        "correct": "lunedì",
        "explanation": "Lunedì → Monday.",
    },
    {
        "english": "Tuesday",
        "correct": "martedì",
        "explanation": "Martedì → Tuesday.",
    },
    {
        "english": "Wednesday",
        "correct": "mercoledì",
        "explanation": "Mercoledì → Wednesday.",
    },
    {
        "english": "Thursday",
        "correct": "giovedì",
        "explanation": "Giovedì → Thursday.",
    },
    {
        "english": "Friday",
        "correct": "venerdì",
        "explanation": "Venerdì → Friday.",
    },
    {
        "english": "Saturday",
        "correct": "sabato",
        "explanation": "Sabato → Saturday.",
    },
    {
        "english": "Sunday",
        "correct": "domenica",
        "explanation": "Domenica → Sunday.",
    },
    {
        "english": "January",
        "correct": "gennaio",
        "explanation": "Gennaio → January.",
    },
    {
        "english": "February",
        "correct": "febbraio",
        "explanation": "Febbraio → February.",
    },
    {
        "english": "March",
        "correct": "marzo",
        "explanation": "Marzo → March.",
    },
    {
        "english": "April",
        "correct": "aprile",
        "explanation": "Aprile → April.",
    },
    {
        "english": "May",
        "correct": "maggio",
        "explanation": "Maggio → May.",
    },
    {
        "english": "June",
        "correct": "giugno",
        "explanation": "Giugno → June.",
    },
    {
        "english": "July",
        "correct": "luglio",
        "explanation": "Luglio → July.",
    },
    {
        "english": "August",
        "correct": "agosto",
        "explanation": "Agosto → August.",
    },
    {
        "english": "September",
        "correct": "settembre",
        "explanation": "Settembre → September.",
    },
    {
        "english": "October",
        "correct": "ottobre",
        "explanation": "Ottobre → October.",
    },
    {
        "english": "November",
        "correct": "novembre",
        "explanation": "Novembre → November.",
    },
    {
        "english": "December",
        "correct": "dicembre",
        "explanation": "Dicembre → December.",
    },
]

DAY_MONTH_OPTIONS = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]

QUESTION_WORD_QUESTIONS = [
    {
        "meaning": "what / thing",
        "correct": "Cosa",
        "explanation": "Cosa → what / thing (Cosa fai oggi? What are you doing today?)",
    },
    {
        "meaning": "which / what kind",
        "correct": "Che",
        "explanation": "Che → which / what kind (Che macchina hai? What kind of car do you have?)",
    },
    {
        "meaning": "which (specific choice)",
        "correct": "Quale",
        "explanation": "Quale → which (Quale gusto preferisce? Which flavor do you prefer?)",
    },
    {
        "meaning": "why / because",
        "correct": "Perché",
        "explanation": "Perché → why / because (Perché studi l'italiano? Why do you study Italian?)",
    },
    {
        "meaning": "how",
        "correct": "Come",
        "explanation": "Come → how (Come stai? How are you?)",
    },
    {
        "meaning": "where",
        "correct": "Dove",
        "explanation": "Dove → where (Dov'è? Where is it? Di dove sei? Where are you from?)",
    },
    {
        "meaning": "when",
        "correct": "Quando",
        "explanation": "Quando → when (Quando è il tuo compleanno? When is your birthday?)",
    },
    {
        "meaning": "how much",
        "correct": "Quanto",
        "explanation": "Quanto/Quanta → how much (singular)",
    },
    {
        "meaning": "how many",
        "correct": "Quanti",
        "explanation": "Quanti/Quante → how many (plural)",
    },
    {
        "meaning": "who",
        "correct": "Chi",
        "explanation": "Chi → who (Chi è? Who is it?)",
    },
]

QUESTION_WORD_OPTIONS = ["Cosa", "Che", "Quale", "Perché", "Come", "Dove", "Quando", "Quanto", "Quanti", "Chi"]

