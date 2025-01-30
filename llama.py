from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the tokenizer and model
model_path = "P:\\llama"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")


# Set the pad token ID if it's not already set
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Tokenize the input
prompt = "What is the capital of France?"
inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

# Move inputs to the correct device (e.g., GPU)
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# Generate text with attention mask
outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],  # Pass the attention mask
    max_length=100,
    num_return_sequences=1,
    temperature=0.7,
    top_p=0.9,
)

# Decode and print the output
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)

