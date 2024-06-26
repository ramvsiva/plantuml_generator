import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class PlantUMLModel:
    def __init__(self, model_name="gpt2-medium"):
        """
        Initializes the PlantUMLModel with a pretrained GPT-2 model and tokenizer.

        Parameters:
            model_name (str): Name of the pretrained GPT-2 model. Default is "gpt2-medium".
        """
        # Load the GPT-2 model and tokenizer from the Hugging Face model repository
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        # Set the tokenizer's padding token to be the same as the end of sequence token
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate(self, input_text, max_new_tokens=1024):
        """
        Generates text continuation for a given input text up to a specified number of new tokens.

        Parameters:
            input_text (str): The input text to generate continuation for.
            max_new_tokens (int): Maximum number of new tokens to generate. Default is 1024.

        Returns:
            str: The generated text continuation.
        """
        
        # Encode the input text using the tokenizer
        inputs = self.tokenizer.encode_plus(input_text, return_tensors="pt", truncation=True, add_special_tokens=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Calculate the maximum length of the model generation
        max_length = input_ids.shape[1] + max_new_tokens

        # Ensure the maximum length does not exceed the model's configuration
        if max_length > self.model.config.max_position_embeddings:
            max_length = self.model.config.max_position_embeddings

        # Generate text using the model, without updating gradients
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

        # Decode the output tokens to a string and return
        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text
