from datasets import load_dataset

# Load the dataset
dataset = load_dataset("iamtarun/python_code_instructions_18k_alpaca")

# Check what it looks like
print(dataset)
print(dataset['train'][0])

# Save it locally so you don't need internet later
dataset.save_to_disk("./coding_dataset")
print("Dataset saved successfully!")