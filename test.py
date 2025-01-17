from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

model_name = "microsoft/codebert-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=2)

code_snippet='''
def divide(a, b):
    c=5+a
    d=6+b
    print(c+d)
    return c / d  # Potential division by zero
a=5
b=6
print(divide(a,b))'''
inputs = tokenizer(code_snippet, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
print(outputs)
print(logits)
print(predicted_class)