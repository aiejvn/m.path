# import sys
import numpy as np
# from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import keras
import keras_nlp
# USE KAGGLE - COPY INTO KAGGLE + DOWNLOAD THE GPT-2 MODEL ON THE WEBSITE

# Doesn't make fanfiction + can be hypertuned!
# # EN no CNN_DAILYMAIL does not produce as good of results

gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_cnn_dailymail")
gpt2_lm.compile(sampler="greedy") # Very deterministic/stable
test1 = gpt2_lm.generate("I hate you! I am feeling ", max_length=100)
print(test1)

gpt2_lm.compile(sampler=keras_nlp.samplers.BeamSampler(num_beams=2))
test2 = gpt2_lm.generate("Today was a great day. I am feeling ", max_length=100) 
# Considers 10 possible outcomes and takes most likely one, is also very stable
print(test2)

gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_cnn_dailymail")
gpt2_lm.compile(sampler="random") # Not very deterministic - very unstable
test1 = gpt2_lm.generate("The world hates me. I am feeling ", max_length=1000)
print(test1)

gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_cnn_dailymail")
gpt2_lm.compile(sampler="greedy") # Very deterministic/stable
test1 = gpt2_lm.generate("I hate you! ", max_length=100)
print(test1)

gpt2_lm.compile(sampler=keras_nlp.samplers.BeamSampler(num_beams=2))
test2 = gpt2_lm.generate("Today was a great day. ", max_length=100) 
# Considers 10 possible outcomes and takes most likely one, is also very stable
print(test2)

gpt2_lm = keras_nlp.models.GPT2CausalLM.from_preset("gpt2_base_en_cnn_dailymail")
gpt2_lm.compile(sampler="random") # Not very deterministic - very unstable
test1 = gpt2_lm.generate("The world hates me. ", max_length=1000)
print(test1)

# Negative words (Red):
# including annoyance, which is a weaker form of anger

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
               "SHUT UP",
               "annoyed"
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
             "troubled"
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
                "terrif", 
                "aghast", 
                "terror",
                "oh no"
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
                 "ugh"]

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

negative_words = angry_words + sad_words + scared_words + disgust_words

# Positive words (Green):
# for now, encompasses excitement

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
               "amaz", 
               "good", 
               "ha", 
               "har", 
               "win",
               "yippee",
               "hooray",
               "nice",
               ":)",
               ":D",
               "let's go!",
               "omg",
               "amazing!"
              ]

# The speaker is most likely in a good mood and kidding around! 
amused_words = ["hehe",
                "LOL",
               "XD",
               "LMAO",
               "LMFAO",
               "haha",
               "muahaha",
                ":3",
                ":>",
                "real"
               ]

# Neutral words (Gray):

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
                   "amaz", 
                   "wonder", 
                   "thunder", 
                   "wrinkle", 
                   "huh", 
                   "hell", 
                   "fuck", 
                   "shit", 
                   "bruh"
                  ]

text_split = test1.split()

emotions_likelihood = {
    "negative": 0,
    "angry": 0,
    "sad": 0,
    "scared": 0,
    "disgust": 0,
    "happy": 0,
    "surprised": 0
}

for i in text_split:
    match i:
        case i in negative_words:
            emotions_likelihood["negative"] += 1
            if i in angry_words:
                emotions_likelihood["angry"] += 1
            elif i in sad_words:
                emotions_likelihood["sad"] += 1
            else:
                emotions_likelihood["scared"] += 1
            break
        case i in happy_words:
            emotions_likelihood["happy"] += 1
            break
        case i in surprised_words:
            emotions_likelihood["surprised"] += 1
            break
            
print(emotions_likelihood.keys(), emotions_likelihood.values())
