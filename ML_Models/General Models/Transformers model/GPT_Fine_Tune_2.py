import pandas as pd
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv(r"E:\Projects\VoxSys\Models Creating\Transformers model\generated_dataset_50000_rows.csv")  # Update with your dataset's path

# Combine input and output for fine-tuning
df['formatted'] = df['natural_language_command'] + " -> " + df['main_command'] + "," + df['argument']

# Split dataset into training and validation sets
train_data, val_data = train_test_split(df['formatted'], test_size=0.2, random_state=42)

# Save to text files
with open("train.txt", "w") as train_file:
    train_file.write("\n".join(train_data.tolist()))

with open("val.txt", "w") as val_file:
    val_file.write("\n".join(val_data.tolist()))
    
#------------------------------------------------------------------------------

from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset

# Load pre-trained GPT2 tokenizer and model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add padding token if not defined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained(model_name)

# Load dataset
train_dataset = load_dataset("text", data_files={"train": "train.txt", "validation": "val.txt"})

# Tokenize dataset
def tokenize_function(examples):
    tokenized = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)
    # Set labels as the same as input_ids
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_datasets = train_dataset.map(tokenize_function, batched=True)
tokenized_datasets = tokenized_datasets.remove_columns(["text"])
tokenized_datasets.set_format("torch")

# Prepare training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_gpt",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=2,
    weight_decay=0.01,
    fp16=True,
    save_total_limit=2,
    save_steps=500,
    logging_dir="./logs",
    logging_steps=10,
    report_to="none",
)


# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Train the model
trainer.train()
