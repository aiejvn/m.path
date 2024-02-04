import numpy as np
import tensorflow as tf
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from new_nlp_algo import detect_feelings

model_name = "gpt2"

gpt2_lm = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def detect_emotion(sample_message):
    
    # loop for some words, add a random compile word, then continue
    
    expanded_sample = ""
    
    for i in range(2):
    
        input_ids = tokenizer.encode(sample_message, return_tensors="pt") # 1 x 13

        output1 = gpt2_lm.generate(
            input_ids, 
            max_length=input_ids.shape[1]+18, 
            num_beams=5, 
            no_repeat_ngram_size=2, 
            top_k=50, 
            top_p=0.95, 
            temperature=0.7, 
        ) # 1 x 18
        expanded_sample += tokenizer.decode(output1[0], skip_special_tokens=True) # String
        
        output2 = gpt2_lm.generate(
            input_ids, 
            max_length=input_ids.shape[1]+12, # size of max_length must always be greater than the input token size
            num_beams=5, 
            no_repeat_ngram_size=2, 
            top_k=50, 
            top_p=0.95, 
            temperature=1.3, 
        )
        expanded_sample += tokenizer.decode(output2[0], skip_special_tokens=True)
        # to prevent 'i am feel' looping
        
    print(f"Expanded message: {expanded_sample}") # Debug print, comment out in beta
    return detect_feelings(expanded_sample)

if __name__ == "__main__":
    print("---------------------------------------------------------------")
    sample_messages = [
        "Freaking hell mfs acting like THEY are the groundhogs", 
        "Okay this is the least prepared I’ve ever been for a test ever since data management", 
        "harharhar", 
        "Hopefully those kids end up homeless", 
        "BRUHHHH UR GOING TO WALMART JUST TO GET WATER?????", 
        "My marks are fine and I did pass (I did slightly better than I thought I had done actually lol)"
    ]

    for sample_message in sample_messages:
        result = detect_emotion(sample_message.lower()) #  + " . I am feeling" optional
        for i in result:
            print(f"{i}: {result[i]}")
