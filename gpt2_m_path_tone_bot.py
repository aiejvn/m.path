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
               "bruh"]

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
             "troubled"]

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
                "terror"]

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
                 "invasion", "freak"]

negative_words = angry_words + sad_words + scared_words + disgust_words

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
               "amaz", 
               "good", 
               "ha", 
               "har", 
               "win",
               "fine", 
               "better", 
               "pass"]

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
                   "amaz", 
                   "wonder", 
                   "thunder", 
                   "wrinkle", 
                   "huh", 
                   "hell", 
                   "fuck", 
                   "shit", 
                   "bruh"]

model_name = "gpt2"

gpt2_lm = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def detect_emotion(sample_message):
    
    # loop for some words, add a random compile word, then continue
    
    expanded_sample = ""
    
    # 100 -> 6 minutes
    # 25 -> 47 seconds
    for i in range(25): 
        
        input_ids = tokenizer.encode(sample_message, return_tensors="pt") # 1 x n size (n is # of tokens)

        output1 = gpt2_lm.generate(
            input_ids, 
            max_length=input_ids.shape[1]+9, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            top_k=50, 
            top_p=0.95, 
            temperature=0.7, 
        ) # 1 x 18
        expanded_sample += tokenizer.decode(output1[0], skip_special_tokens=True) # String
        
        output2 = gpt2_lm.generate(
            input_ids, 
            max_length=input_ids.shape[1]+6, # size of max_length must always be greater than the input token size
            num_beams=5, 
            no_repeat_ngram_size=2, 
            top_k=50, 
            top_p=0.95, 
            temperature=1.3, 
        )
        expanded_sample += tokenizer.decode(output2[0], skip_special_tokens=True)
        # to prevent 'i am feel' looping
    
    print("---------------------------------------------------------------")
    print(f"Expanded message: {expanded_sample}") # Debug print, comment out in beta
    print("---------------------------------------------------------------")
    
    text_split = expanded_sample.lower().split()
    n = len(text_split)
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
        if i in negative_words:
            emotions_likelihood["negative"] += 1
            if i in angry_words:
                emotions_likelihood["angry"] += 1
            elif i in sad_words:
                emotions_likelihood["sad"] += 1
            else:
                emotions_likelihood["scared"] += 1
        elif i in happy_words:
            emotions_likelihood["happy"] += 1
        elif i in surprised_words:
            emotions_likelihood["surprised"] += 1
    for key in emotions_likelihood.keys():
        emotions_likelihood[key] = str(emotions_likelihood[key] / n * 100) + "%" 
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
        result = detect_emotion(sample_message.lower().strip("!.,=")) #  + " . I am feeling" optional
        for i in result:
            print(f"{i}: {result[i]}")