from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import subprocess


def analyze_code(code_snippet):
    feedback = []

    # Load CodeBERT model
    model_name = "microsoft/codebert-base"
    tokenizer = RobertaTokenizer.from_pretrained(model_name)
    model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # Tokenize and analyze code
    inputs = tokenizer(code_snippet, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

    feedback.append("⚠️ Potential defect detected." if predicted_class == 1 else "✅ No critical defects detected.")

    # Run pylint for style analysis
    with open("temp_code.py", "w") as temp_file:
        temp_file.write(code_snippet)
    pylint_result = subprocess.getoutput("pylint temp_code.py --disable=R,C --score=no")
    feedback.append("\n📏 Style Feedback:\n" + pylint_result)

    # Run bandit for security analysis
    bandit_result = subprocess.getoutput("bandit -r temp_code.py")
    feedback.append("\n🔒 Security Feedback:\n" + bandit_result)

    return "\n\n".join(feedback)