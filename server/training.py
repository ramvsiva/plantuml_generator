import os
from transformers import (GPT2LMHeadModel, GPT2Tokenizer,
                          Trainer, TrainingArguments, DataCollatorForLanguageModeling, EarlyStoppingCallback)
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv('hugging_face_token')

model_name = 'gpt2-medium'
repo_name = 'ramvsivakumar/plantumlgenerator'


class PlantUMLDataset(Dataset):
    def __init__(self, descriptions, plantuml_codes, tokenizer, max_length):
        self.inputs = [tokenizer.encode(desc + tokenizer.eos_token, max_length=max_length, truncation=True,
                                        padding="max_length", return_tensors="pt").squeeze(0) for desc in descriptions]
        self.targets = [tokenizer.encode(code + tokenizer.eos_token,
                                         max_length=max_length, truncation=True, padding="max_length",
                                         return_tensors="pt").squeeze(0) for code in plantuml_codes]

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return {"input_ids": self.inputs[idx], "labels": self.targets[idx]}


tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(model_name)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False, return_tensors='pt')

raw_df = pd.read_parquet('plantuml_dataset.parquet')


def extract_data(df):

    text_column_name = 'text'
    results = []
    use_case_id = ''
    use_case_description = ''

    for index, row in df.iterrows():
        text_column = row[text_column_name]

        use_case_id_start_idx = text_column.find('Use Case ID:')
        if use_case_id_start_idx != -1:
            id_start = use_case_id_start_idx + len('Use Case ID:')
            id_end = text_column.find('\n', id_start)
            use_case_id = text_column[id_start:id_end].strip()

        desc_start_idx = text_column.find('Use Case Description:')
        if desc_start_idx != -1:
            description_start = desc_start_idx + len('Use Case Description:')
            description_end = text_column.find('Use Case Actors:', description_start)
            if description_end == -1:
                description_end = text_column.find('\n', description_start)
            use_case_description = text_column[description_start:description_end].strip()

        uml_pattern = re.compile(r"\[/INST\](@startuml.*?@enduml)", re.DOTALL)
        uml_match = uml_pattern.search(text_column)
        uml_diagram = uml_match.group(1).strip() if uml_match else ""

        results.append({
            'Case_ID': use_case_id,
            'Description': use_case_description,
            'PlantUML_Code': uml_diagram
        })

    return pd.DataFrame(results)


df = extract_data(raw_df)
df['Description'] = df['Description'].str.lstrip('-')
df = df[(df['Description'].str.strip() != '') & (df['PlantUML_Code'].str.strip() != '')]


train_df, test_df = train_test_split(df, test_size=0.1)
train_dataset = PlantUMLDataset(train_df['Description'].tolist(), train_df['PlantUML_Code'].tolist(), tokenizer, max_length=512)
test_dataset = PlantUMLDataset(test_df['Description'].tolist(), test_df['PlantUML_Code'].tolist(), tokenizer, max_length=512)


training_args = TrainingArguments(
    output_dir='./models',
    num_train_epochs=30,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=500,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    push_to_hub=True,
    hub_model_id=repo_name,
    hub_token=hf_token
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=5)]
)

trainer.train()

model.push_to_hub(repo_name)
tokenizer.push_to_hub(repo_name)
