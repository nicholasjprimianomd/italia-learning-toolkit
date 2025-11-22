"""
Reference content used by the Italian Learning Toolkit.

Add new sections by appending dictionaries with ``title`` and ``content`` keys
to the ``REFERENCE_SECTIONS`` list.
"""

from textwrap import dedent


REFERENCE_SECTIONS = [
    {
        "title": "Articles",
        "content": dedent(
            """
            Definite articles change with gender, number, and the sound that begins a noun.

            Singular masculine
            - IL: standard form when the word begins with most consonants. E.g. il gatto, il panino
            - LO: used when the word begins with z or impure s (s + consonant). E.g. lo scaffale, lo zucchero
            - L': used for all singular nouns (masculine or feminine) that begin with a vowel. E.g. l'arancia

            Singular feminine
            - LA: standard form. E.g. la pizza
            - L': vowel-starting words. E.g. l'arancia

            Plural masculine
            - I: plural of il. E.g. i gatti, i panini
            - GLI: plural of lo and l'. E.g. gli scaffali, gli zuccheri

            Plural feminine
            - LE: plural of la and l'. E.g. le pizze, le arancie

            Quick pairings
            - il gatto / i gatti
            - il panino / i panini
            - lo scaffale / gli scaffali
            - lo zucchero / gli zuccheri
            - la pizza / le pizze
            - l'arancia / le arancie
            """
        ).strip(),
    },
    {
        "title": "Essere vs Stare",
        "content": dedent(
            """
            Essere describes identity, traits, and permanent states. Stare expresses how someone is doing,
            ongoing actions, or staying in a place.

            Essere (to be)
            - io sono
            - tu sei
            - lui/lei è
            - noi siamo
            - voi siete
            - loro sono

            Stare (to stay / to be doing)
            - io sto
            - tu stai
            - lui/lei sta
            - noi stiamo
            - voi state
            - loro stanno

            Usage examples
            - Come stai? → sto bene.
            - Io sto dormendo perché sono stanco.
            """
        ).strip(),
    },
    {
        "title": "Avere (To Have)",
        "content": dedent(
            """
            Avere indicates possession and many idiomatic expressions.

            Conjugation
            - io ho
            - tu hai
            - lui/lei ha
            - noi abbiamo
            - voi avete
            - loro hanno

            Remember: the letter H is silent in Italian, so ho, hai, ha sound like "o", "ai", "a".
            """
        ).strip(),
    },
    {
        "title": "Pronunciation Tips",
        "content": dedent(
            """
            - H is always silent.
            - CI sounds like "chee" (formaggio).
            - CE sounds like "cheh" (certo).
            - CA, CO, CU keep a hard C (casa, cosa, cucù).
            - CH produces a hard K sound before E/I (gnocchi, bruschetta).

            G combinations
            - GI sounds like "jee" (jeans).
            - GE sounds like "jeh" (gelato).
            - GA, GO, GU use a hard G.
            - GH before E/I keeps the hard G.

            S + C combinations
            - SCI sounds like "shee" (scimmia).
            - SCE sounds like "sheh" (scelta).

            Double consonants (NN, MM, LL) are held slightly longer. E.g. penne.

            Special blends
            - GN sounds like Spanish ñ (gnocchi).
            - GLI sounds like "ly" (maglietta, foglia, tovaglia).
            """
        ).strip(),
    },
    {
        "title": "Prepositions + Articles",
        "content": dedent(
            """
            Simple prepositions merge with definite articles to form new words.

            Common meanings
            - di: of, from; also used in comparisons.
            - a: to, at.
            - da: from, since, someone's place, by, or functional use.
            - in: in.
            - su: on.

            Examples
            - la macchina della polizia (di + la = della)
            - vado all'aeroporto (a + l' = all')
            - vengo dagli Stati Uniti (da + gli = dagli)
            - dal 1950 (da + il = dal)
            - vado da Mary oggi (to someone's place)
            - occhiali da sole / scarpe da tennis (function)
            - la chiave è nella macchina (in + la = nella)
            - la bottiglia è sul tavolo (su + il = sul)
            """
        ).strip(),
    },
    {
        "title": "Greetings (Saluti)",
        "content": dedent(
            """
            Daily greetings
            - Buongiorno: good morning / good day
            - Ciao: hi / bye
            - Buon pomeriggio: good afternoon (less common)
            - Buonasera: good evening
            - Buona notte: good night
            - Buona serata: have a good evening
            - Buona giornata: have a good day
            - Salve: formal hi
            - Arrivederci: formal goodbye
            - Ci vediamo: see you (informal)

            Meeting people
            - Piacere di conoscerti: nice to meet you (informal)
            - Piacere di conoscerla: nice to meet you (formal)
            - Piacere: neutral, can stand alone
            """
        ).strip(),
    },
    {
        "title": "Numbers & Dates",
        "content": dedent(
            """
            Years are spoken as one continuous number.

            Example
            - 1956 → mille novecento cinquantasei
            - Oggi è l'otto novembre duemila e venticinque
            """
        ).strip(),
    },
    {
        "title": "Telling Time",
        "content": dedent(
            """
            Asking: Che ora è? (Which hour is it?)

            Key phrases
            - È l'una → it's one o'clock
            - È mezzogiorno → it's noon
            - È mezzanotte → it's midnight
            - Sono le due/tre... → it is 2, 3, etc.

            Minutes
            - Sono le cinque e quindici / sono le cinque e un quarto
            - Sono le cinque e trenta / sono le cinque e mezza
            - Sono le cinque e quarantacinque / sono le sei meno un quarto

            Extras
            - meno: minus / less
            - più: plus / more
            - circa: around (sono circa le cinque)
            - in punto: o'clock exactly (sono le cinque in punto)
            - cinque di mattina / cinque di sera (5 AM / 5 PM)
            """
        ).strip(),
    },
    {
        "title": "Weather",
        "content": dedent(
            """
            Questions
            - Com'è il tempo? / Che tempo fa?

            Descriptions
            - C'è il sole / è soleggiato → it's sunny
            - Fa caldo / fa freddo / fa fresco → it's hot, cold, chilly
            - Sta piovendo / sta nevicando / sta grandinando → it's raining / snowing / hailing
            - C'è la nebbia → it's foggy
            - C'è vento → it's windy
            - È nuvoloso → it's cloudy

            Vocabulary
            - la pioggia (rain), la neve (snow), la grandine (hail)
            - la nebbia (fog), il vento (wind), la nuvola (cloud)

            Temperature
            - Quanti gradi ci sono? / Qual è la temperatura?
            - Ci sono X gradi / Ci sono meno tre gradi
            """
        ).strip(),
    },
    {
        "title": "Colors & Agreement",
        "content": dedent(
            """
            Most colors agree with gender and number.

            Standard agreement
            - rosso / rossa / rossi / rosse
            - bianco / bianca / bianchi / bianche
            - nero / nera / neri / nere
            - giallo / gialla / gialli / gialle
            - grigio / grigia / grigi / grigie

            Invariable colors (stay the same)
            - arancione, marrone, verde, blu, viola, rosa

            Examples
            - la macchina rossa, il cappello rosso
            - le macchine rosse, i cappelli rossi
            - la macchina viola, il cappello viola
            - la macchina blu, le macchine blu
            - l'uomo arrabbiato / la donna arrabbiata
            - l'uomo felice / la donna felice
            """
        ).strip(),
    },
    {
        "title": "Clothing Vocabulary",
        "content": dedent(
            """
            - maglietta: T-shirt
            - camicia: button-up shirt
            - giacca: jacket
            - pantaloni: pants
            - mutande: underwear
            - cappello: hat
            - scarpe: shoes
            - calze: socks
            - vestito: dress
            - felpa: sweatshirt, maglione: sweater
            - sciarpa: scarf
            - guanti: gloves
            - cappotto: coat
            - gonna: skirt
            - i jeans: jeans
            - occhiali / occhiali da sole: glasses / sunglasses
            - stivali: boots
            - cravatta: tie

            Combinations
            - gli stivali neri
            - i jeans neri
            - la giacca rossa
            - la camicia bianca
            """
        ).strip(),
    },
    {
        "title": "Days & Months",
        "content": dedent(
            """
            Days of the week
            - lunedì, martedì, mercoledì, giovedì, venerdì, sabato, domenica

            Months of the year
            - gennaio, febbraio, marzo, aprile, maggio, giugno
            - luglio, agosto, settembre, ottobre, novembre, dicembre

            Asking: Che mese è?
            """
        ).strip(),
    },
    {
        "title": "Question Words",
        "content": dedent(
            """
            - Cosa: what / thing (Cosa fai oggi?)
            - Che: which / what kind (Che macchina hai?)
            - Quale: which (Quale gusto preferisce?)
            - Perché: why / because (Perché studi l'italiano?)
            - Come: how (Come stai?)
            - Dove: where (Dov'è? Di dove sei?)
            - Quando: when (Quando è il tuo compleanno?)
            - Quanto / Quanta: how much
            - Quanti / Quante: how many
            - Chi: who (Chi è?)
            """
        ).strip(),
    },
    {
        "title": "Possessive Pronouns",
        "content": dedent(
            """
            In order: M singular / F singular / M plural / F plural

            My
            - il mio / la mia / i miei / le mie

            Your
            - il tuo / la tua / i tuoi / le tue

            His/Her
            - il suo / la sua / i suoi / le sue

            Our
            - il nostro / la nostra / i nostri / le nostre

            Your (plural)
            - il vostro / la vostra / i vostri / le vostre

            Their
            - il loro / la loro / i loro / le loro

            Examples
            - my car → la mia macchina
            - my mother → mia madre
            - my girlfriend → la mia ragazza
            - my wife → mia moglie
            - my boyfriend → il mio ragazzo
            - my husband → mio marito
            - my red car → la mia macchina rossa

            Note: With family members (madre, padre, moglie, marito), the article is often dropped.
            """
        ).strip(),
    },
    {
        "title": "Family (Famiglia)",
        "content": dedent(
            """
            - famiglia: family
            - madre: mother
            - mamma: mom
            - padre: father
            - papà / babbo: dad
            - fratello: brother
            - sorella: sister
            - zio: uncle
            - zia: aunt
            - nonno: grandfather
            - nonna: grandmother
            - nonni: grandparents
            - nonne: grandmothers
            - cugino / cugina: cousin (M/F)
            - nipote: nephew / niece / grandson / granddaughter
            - figlio: son
            - figlia: daughter
            - genitori: parents
            - parenti: relatives
            """
        ).strip(),
    },
    {
        "title": "Piacere (Like) & Mancare (Miss)",
        "content": dedent(
            """
            These verbs use passive construction - the thing you like is the subject.

            Indirect object pronouns
            - mi: to me
            - ti: to you
            - gli: to him
            - le: to her
            - ci: to us
            - vi: to you all
            - gli: to them

            Piacere (to like)
            - I like it → mi piace
            - you like it → ti piace
            - he likes it → gli piace
            - she likes it → le piace
            - we like it → ci piace
            - y'all like it → vi piace
            - they like it → gli piace

            Use piace (singular) or piacciono (plural)
            - mi piace la pizza → I like pizza
            - mi piacciono gli spaghetti → I like spaghetti
            - ti piacciono gli spaghetti? → do you like spaghetti?

            More examples
            - I like them → mi piacciono
            - I like you → mi piaci
            - you like it → ti piace
            - we like them → ci piacciono
            - I like you guys → mi piacete
            - you all like us → vi piacciamo

            Mancare (to miss) - works the same way
            - mi manca → I miss it
            - ti manca → you miss it
            - gli manca → he misses it
            - le manca → she misses it
            - ci manca → we miss it
            - vi manca → you all miss it
            - gli manca → they miss it
            """
        ).strip(),
    },
    {
        "title": "Body Parts (Parti del Corpo)",
        "content": dedent(
            """
            Emergency numbers
            - 112: emergency
            - 118: ambulance
            - 113: police
            - 115: fire department

            Head & Face
            - la testa: head
            - i capelli: hair (on head)
            - gli occhi / l'occhio: eyes / eye
            - il naso: nose
            - la bocca: mouth
            - le orecchie / l'orecchio: ears / ear
            - il mento: chin
            - le guance / la guancia: cheeks / cheek
            - le ciglia: eyelashes
            - le sopracciglia: eyebrows
            - il collo: neck
            - le labbra / il labbro: lips / lip
            - i denti / il dente: teeth / tooth
            - la lingua: tongue / language

            Body
            - le spalle / la spalla: shoulders / shoulder
            - il petto: chest
            - la pancia: belly
            - le braccia / il braccio: arms / arm
            - le mani / la mano: hands / hand
            - le dita / il dito: fingers / finger
            - le gambe / la gamba: legs / leg
            - i piedi / il piede: feet / foot
            - le dita dei piedi: toes
            - le ginocchia / il ginocchio: knees / knee
            - i gomiti / il gomito: elbows / elbow
            - l'ombelico: belly button
            - la schiena: back
            - la pelle: skin / leather
            - i peli: body hair

            Pain expressions
            - mi fa male X (singular): my X hurts
            - mi fanno male X (plural): my X hurts
            - mi fa male la testa: my head hurts
            - mi fanno male i denti: my teeth hurt
            """
        ).strip(),
    },
]

