import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class PlantUMLModel:
    def __init__(self, model_name="gpt2-medium"):
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate(self, input_text, max_new_tokens=1024):
        inputs = self.tokenizer.encode_plus(input_text, return_tensors="pt", truncation=True, add_special_tokens=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        max_length = input_ids.shape[1] + max_new_tokens

        if max_length > self.model.config.max_position_embeddings:
            max_length = self.model.config.max_position_embeddings

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=max_length,
                no_repeat_ngram_size=2,
                temperature=0.9,
                top_p=0.92,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1
            )

        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text
