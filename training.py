import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Load your CSV data into a Pandas DataFrame
df = pd.read_csv("data.csv")  # Update with your CSV file name

# Assuming your text data is in a column named "text"
text_data = df["text"].tolist()[:25]

# Concatenate all text data into a single string
corpus = "\n".join(text_data)

with open("data.txt", "w") as f:
    f.write(corpus)

# Initialize GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_lm = GPT2LMHeadModel.from_pretrained("gpt2")

# Tokenize the text data
input_ids = tokenizer.encode(corpus, return_tensors="pt")

# Create a dataset using TextDataset
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path="data.csv",  # You can provide a file path if your data is saved in a file
    block_size=128,
    overwrite_cache=True,
)

# Initialize data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./gpt2_lm",
    overwrite_output_dir=True,
    num_train_epochs=1,  # You can adjust the number of epochs
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

# Initialize Trainer
trainer = Trainer(
    model=gpt2_lm,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Start training
# trainer.train()
