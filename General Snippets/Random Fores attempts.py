from transformers import BertForTokenClassification, BertTokenizer, AdamW, BertConfig
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd

# Multi-task model with token classification
class MultiTaskModel(BertForTokenClassification):
    def __init__(self, config, num_main_classes, num_arg_classes):
        super().__init__(config)
        
        # Define two separate heads for the two tasks
        self.main_head = nn.Linear(config.hidden_size, num_main_classes)  # Main task head
        self.arg_head = nn.Linear(config.hidden_size, num_arg_classes)    # Argument task head

    def forward(self, input_ids, attention_mask, token_type_ids=None, labels=None):
        # Get BERT model outputs
        outputs = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask,
                            token_type_ids=token_type_ids,
                            return_dict=True, output_hidden_states=True)
        
        # Extract hidden states (last layer)
        hidden_states = outputs.last_hidden_state  # shape: (batch_size, seq_len, hidden_size)

        # We are interested in the [CLS] token, so extract it (batch_size, hidden_size)
        cls_hidden_state = hidden_states[:, 0, :]  # Take only the [CLS] token's hidden state

        # Compute logits for both tasks
        main_logits = self.main_head(cls_hidden_state)  # Main task logits
        arg_logits = self.arg_head(cls_hidden_state)    # Argument task logits

        loss = None
        if labels is not None:
            # Compute the loss for both tasks
            main_loss = nn.CrossEntropyLoss()(main_logits.view(-1, self.num_labels), labels['main_labels'])
            arg_loss = nn.CrossEntropyLoss()(arg_logits.view(-1, self.num_labels), labels['arg_labels'])
            loss = main_loss + arg_loss

        return {"loss": loss, "main_logits": main_logits, "arg_logits": arg_logits}

# Custom Dataset class
class CommandClassificationDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data.iloc[idx]
        command = item['command']
        main_label = item['main_label']
        arg_label = item['arg_label']

        # Tokenize the input command
        encoding = self.tokenizer(
            command,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        # Prepare input tensors and labels
        input_ids = encoding['input_ids'].squeeze(0)  # Remove extra batch dimension
        attention_mask = encoding['attention_mask'].squeeze(0)
        token_type_ids = encoding.get('token_type_ids', None)

        # Return a dictionary with the labels and input data
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'token_type_ids': token_type_ids,
            'labels': {'main_labels': torch.tensor(main_label, dtype=torch.long),
                       'arg_labels': torch.tensor(arg_label, dtype=torch.long)}
        }

# Sample data (replace with your actual data)
data = pd.DataFrame({
    'command': ['open file', 'close file', 'launch app'],
    'main_label': [0, 1, 0],  # Example main task labels
    'arg_label': [1, 0, 1]    # Example argument task labels
})

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
config = BertConfig.from_pretrained("bert-base-uncased", num_labels=2)  # Two labels for both tasks
model = MultiTaskModel(config=config, num_main_classes=2, num_arg_classes=2)

# Create Dataset and DataLoader
train_dataset = CommandClassificationDataset(data, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# Optimizer
optimizer = AdamW(model.parameters(), lr=2e-5)

# Training Loop (simplified)
for epoch in range(3):
    model.train()
    for batch in train_loader:
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        token_type_ids = batch['token_type_ids']
        labels = batch['labels']
        
        # Forward pass
        outputs = model(input_ids=input_ids,
                        attention_mask=attention_mask,
                        token_type_ids=token_type_ids,
                        labels=labels)
        
        loss = outputs['loss']
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

# Example Inference
model.eval()
example_command = "open file"
encoding = tokenizer(example_command, return_tensors="pt", truncation=True, padding=True, max_length=512)

with torch.no_grad():
    output = model(input_ids=encoding['input_ids'], 
                   attention_mask=encoding['attention_mask'])
    main_logits = output['main_logits']
    arg_logits = output['arg_logits']
    print("Main Task Predictions:", main_logits)
    print("Argument Task Predictions:", arg_logits)
