from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Negative words:
angry_words = ["hate",
               "angry",
               "anger",
               "mad",
               "pissed",
               "WTF",
               "wtf",
               "enraged",
               "motherfucker",
               "mf",
               "BS",
               "bs",
               "bullshit",
               "shit",
               "upset",
               "rage",
               "irritate",
               "outrage",
               "frustrate",
               "irritate",
               "kill yourself",
               "kys",
               "hell",
               "angry",
               "bruh",
               "SHUT UP",
               "annoyed",
               ">:(",
               ">:T",
               "😤",
               "😠",
               "😡",
               "🤬",
               "bruh",
               "what.",
               "NOT"
               ]

sad_words = ["bitter",
             "dismal",
             "heartbroke",
             "sad",
             "depress",
             "blue",
             "unhappy",
             "broke",
             "sorrow",
             "sorry",
             "bereave",
             "deject",
             "despair",
             "despondent",
             "distress",
             "grieve",
             "down",
             "forlorn",
             "gloom",
             "glum",
             "sick",
             "weep",
             "low",
             "unhappy",
             "troubled",
             ":(",
             ":\'(",
             "😥",
             "😓",
             "☹",
             "🙁",
             "😭",
             "😢",
             "😦",
             "crying"
             ]

scared_words = ["afraid",
                "anxious",
                "anxiety",
                "fear",
                "scare",
                "panic",
                "startle",
                "petrif",
                "shake",
                "terrified",
                "aghast",
                "terror",
                "terrify",
                "terrifying",
                "terror",
                "oh no",
                "😱",
                "😰",
                "😨",
                ":\'0"
                ]

disgust_words = ["suck",
                 "appal",
                 "outrage",
                 "tire",
                 "unhappy",
                 "weary",
                 "quease",
                 "abhorr",
                 "displease",
                 "nausea",
                 "repel",
                 "repulse",
                 "revolt",
                 "satiat",
                 "scandal",
                 "sick",
                 "fed up",
                 "gross",
                 "squeam",
                 "indignant",
                 "invasion",
                 "freak",
                 "ugh",
                 "🤢",
                 "🤮"
                 ]

disappointed_words = ["man...",
                      "alright...",
                      "...",
                      "ok...",
                      ":/",
                      ":T",
                      "yeah...",
                      "💀",
                      "😶",
                      "😐",
                      "😑",
                      "🙄",
                      "okay.",
                      "😔",
                      "😞"
                      ]

negative_words = angry_words + sad_words + scared_words + disgust_words + disappointed_words

# Happy words (green):

happy_words = ["cheerful",
               "delight",
               "ecstatic",
               "elate",
               "enrapture",
               "exult",
               "glad",
               "glee",
               "jolly",
               "joy",
               "jubilant",
               "merry",
               "mirth",
               "thrill",
               "up",
               "bless",
               "bliss",
               "content",
               "gratifi",
               "peace",
               "pleas",
               "satisf",
               "spark",
               "sun",
               "tickle",
               "chipper",
               "chirp",
               "gay",
               "perky",
               "live",
               "laugh",
               "pink",
               "amazing",
               "amazed",
               "amaze",
               "good",
               "ha",
               "har",
               "win",
               "fine",
               "better",
               "pass",
               "harhar",
               "harharhar",
               "harharharhar",
               "ha",
               "haha",
               "hahaha",
               "hahahahaha",
               "yippee",
               "hooray",
               "nice",
               ":)",
               ":D",
               "let's go!",
               "omg",
               "amazing!",
               "☺",
               "😊",
               "🤩",
               "😃",
               "😁",
               "😄",
               "smile",
               "smiling",
               "smiled",
               "smiles",
               "grin",
               "grinning",
               "grinned",
               "grins",
               "happy",
               "!",
               "yippee"]

amused_words = ["hehe",
                "LOL",
                "XD",
                "LMAO",
                "LMFAO",
                "haha",
                "muahaha",
                ":3",
                ":>",
                "real",
                ":P",
                "😋",
                "😏",
                "🤭",
                "😛",
                "😝",
                "😜"
                ]

positive_words = happy_words + amused_words

# Neutral words (gray):

surprised_words = ["shock",
                   "blue",
                   "jaw",
                   "drop",
                   "twist",
                   "wow",
                   "what",
                   "who",
                   "why",
                   "kick",
                   "reveal",
                   "bomb",
                   "stun",
                   "amazing",
                   "amazed",
                   "amaze",
                   "wonder",
                   "thunder",
                   "wrinkle",
                   "huh",
                   "hell",
                   "fuck",
                   "shit",
                   "bruh",
                   "what?!",
                   "😲",
                   ":0",
                   "🤯",
                   "😳",
                   "omg",
                   "o",
                   "oh",
                   "oh my",
                   "oh my god"
                   ]

model_name = "gpt2"

gpt2_lm = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def detect_emotion(sample_message):
    """Given some sample user message(s), return the probability
    that the user is feeling some emotion.

    Args:
        sample_message (String): A message/messages a user says.

    Returns:
        dict: A dictionary of emotions and the likelihood that the
        user is experiencing them.
    """
    input_ids = tokenizer.encode(sample_message, return_tensors="pt")  # 1 x n size (n is # of tokens)

    expanded_sample = ""

    # 100 -> 6 minutes
    # 25 -> 47 seconds
    # Current implementation -
    for i in range(2):
        output1 = gpt2_lm.generate(
            input_ids,
            max_length=input_ids.shape[1] + 18,
            num_beams=5,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
        )  # 1 x 18
        expanded_sample += tokenizer.decode(output1[0], skip_special_tokens=True) + " "  # String

        output2 = gpt2_lm.generate(
            input_ids,
            max_length=input_ids.shape[1] + 12,  # size of max_length must always be greater than the input token size
            num_beams=5,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=1.3,
        )
        expanded_sample += tokenizer.decode(output2[0], skip_special_tokens=True) + " "
        # to prevent 'i am feel' looping

    print("---------------------------------------------------------------")
    print(f"Expanded message: {expanded_sample}")  # Debug print, comment out in beta
    print("---------------------------------------------------------------")

    text_split = expanded_sample.lower().split()
    num_emotion_words = 0
    emotions_likelihood = {
        "negative": 0,
        "positive": 0,
        "angry": 0,
        "sad": 0,
        "scared": 0,
        "disgust": 0,
        "disappointed": 0,
        "happy": 0,
        "amused": 0,
        "surprised": 0
    }
    for i in text_split:
        if i in negative_words:
            num_emotion_words += 1

            emotions_likelihood["negative"] += 1
            if i in angry_words:
                emotions_likelihood["angry"] += 1
            elif i in sad_words:
                emotions_likelihood["sad"] += 1
            elif i in disgust_words:
                emotions_likelihood["disgust"] += 1
            elif i in disappointed_words:
                emotions_likelihood["disappointed"] += 1
            else:
                emotions_likelihood["scared"] += 1
        elif i in positive_words:
            num_emotion_words += 1

            emotions_likelihood["positive"] += 1
            if i in happy_words:
                emotions_likelihood["happy"] += 1
            else:
                emotions_likelihood["amused"] += 1
        elif i in surprised_words:
            num_emotion_words += 1

            emotions_likelihood["surprised"] += 1
    for key in emotions_likelihood.keys():
        if num_emotion_words != 0:
            emotions_likelihood[key] = emotions_likelihood[key] / num_emotion_words * 100
    return emotions_likelihood


if __name__ == "__main__":
    sample_messages = [
        "Freaking hell mfs acting like THEY are the groundhogs",
        "Okay this is the least prepared I’ve ever been for a test ever since data management",
        "harharhar",
        "Hopefully those kids end up homeless",
        "BRUHHHH UR GOING TO WALMART JUST TO GET WATER?????",
        "My marks are fine and I did pass (I did slightly better than I thought I had done actually lol)"
    ]

    for sample_message in sample_messages:
        result = detect_emotion(sample_message.lower().strip("!.,="))  # + " . I am feeling" optional
        for i in result:
            print(f"{i}: {result[i]}")
    # result = detect_emotion("bruhhhh bruhhh bruhhh".lower().strip("!.,=")) # dupe letters bug
    # for i in result:
    #     print(f"{i}: {result[i]}")