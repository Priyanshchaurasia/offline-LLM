content = '''FROM C:/Users/priya/OneDrive/Desktop/ONGC/coding-model.gguf

SYSTEM """You are an expert coding assistant. You only help with programming and software development tasks. You write clean, efficient, well-commented code."""

PARAMETER temperature 0.2
PARAMETER top_p 0.95
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 2048
'''

with open("Modelfile", "w", encoding="utf-8") as f:
    f.write(content)

print("Modelfile created!")

# Verify it
with open("Modelfile", "r") as f:
    print(f.read())