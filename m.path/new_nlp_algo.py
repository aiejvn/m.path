import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

val_data = pd.read_csv("emotion_data.csv")
train = pd.read_csv("emotion_data.csv")

train_data, test_data, train_labels, test_labels = train_test_split(train['text'], train['label'], test_size=0.5, random_state=42)

# print("Validation data :"+ val_data.shape)
# print("Train data :" + train_data.shape)

# print(train_data.head())
# print(val_data.head())

train_features = tfidf_vectorizer.fit_transform(train_data)

# print(np.array(train_features))

model = MultinomialNB()
model.fit(train_features, train_labels) 

def check_accuracy():
    test_features = tfidf_vectorizer.transform(test_data)
    predictions = model.predict(test_features)
    accuracy = accuracy_score(test_features, predictions)
    print(f'Accuracy: {accuracy:.2f}')


# Split paragraph into sentences, feed into algo + get float outputs


def detect_emotion(message):
    end_punctuation = "!.?"

    for i in end_punctuation:
        message = message.replace(i, " ")

    input_message = message.split()

    input_data = tfidf_vectorizer.transform([message])
    predictions = model.predict(input_data)
    n = len(predictions)

    emotions_likelihood = {
        "negative": 0,
        "positive": 0,
        "anger": 0,
        "sad": 0,
        "fear": 0,
        "joy": 0,
        "love": 0,
        "surprise": 0
    }

    for i in predictions:
        match i:
            case 0:
                emotions_likelihood["negative"] += 1
                emotions_likelihood["sad"] += 1
            case 1:
                emotions_likelihood["positive"] += 1
                emotions_likelihood["joy"] += 1
            case 2:
                emotions_likelihood["positive"] += 1
                emotions_likelihood["love"] += 1
            case 3:
                emotions_likelihood["negative"] += 1
                emotions_likelihood["anger"] += 1
            case 4:
                emotions_likelihood["negative"] += 1
                emotions_likelihood["fear"] += 1
            case 5:
                emotions_likelihood["surprise"] += 1

    max_likelihood = max(emotions_likelihood.values())

    for key in emotions_likelihood:
        emotions_likelihood[key] = (emotions_likelihood[key] / max_likelihood) * 100

    return emotions_likelihood

   
if __name__ == "__main__":
    sample_messages = [
        "Freaking hell mfs acting like THEY are the groundhogs", 
        "Okay this is the least prepared I’ve ever been for a test ever since data management", 
        "harharhar", 
        "Hopefully those kids end up homeless", 
        "BRUHHHH UR GOING TO WALMART JUST TO GET WATER?????", 
        "My marks are fine and I did pass (I did slightly better than I thought I had done actually lol)",
        "Connection Terminated. I'm sorry to interrupt you, Elizabeth. If you still even remember that name." + 
        "But I'm afraid you've been misinformed. You are not here to receive a gift. Nor, have you been called" + 
        "here by the individual you assume. Although, you have indeed been called. You have all been called here." +  
        "Into a labyrinth of sounds and smells, misdirection and misfortune. A labyrinth with no exit. A maze with" + 
        "no prize. You don't even realize that you are trapped. Your lust of blood has driven you in endless circles." + 
        "Chasing the cries of children in some unseen chamber, always seeming so near. It's somehow out of reach." +  
        "But, you will never find them. None of you will. This is where your story ends. And to you, my brave volunteer," + 
        "who somehow found this job listing not intended for you. Although, there was a way out planned for you," + 
        "I have a feeling that's not what you want. I have a feeling that you are right where you want to be." + 
        "I am remaining as well. I am nearby. This place will not be remembered and the memory of everything that started this," + 
        "can finally begin to fade away. As the agony of every tragedy should. And to you monsters trapped in the corridors." + 
        "Be still. And give up your spirits. They don't belong to you. As for most of you, I believe there is peace and perhaps, warm, waiting for you after the smoke clears. Although, for one of you, the darkest pit of Hell has opened to swallow you whole. So, don't keep the Devil waiting, friend. My daughter, if you can hear me, I knew you would return as well. It's in your nature to protect the innocent. I'm sorry that on that day, the day you were shut out and left to die, no one was there to lift you up in their arms, the way you lifted others into yours. And then, what became of you, I should have known, you wouldn't be content to disappear. Not my daughter. I couldn't save you then. So, let me save you now. It's time to rest, for you, and for those you have carried in your arms... This ends. For all of us. End communication."
    ]

    for i in range(len(sample_messages)):
        result = detect_emotion(sample_messages[i])
        print(list(result.keys()), list(result.values()))
