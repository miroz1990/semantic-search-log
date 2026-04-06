import re

# -------------------------------
# File paths
# -------------------------------
input_file = "data/Apache.log"
output_file = "data/clean_logs_apache.txt"

# -------------------------------
# Step 1: Parsing function
# -------------------------------
def parse_log(log):
    pattern = r"\[(.*?)\] \[(.*?)\](?: \[client (.*?)\])? (.*)"
    match = re.match(pattern, log)

    if match:
        timestamp, level, client_ip, message = match.groups()
        return level, message
    return None, None

# -------------------------------
# Step 2: Normalize message
# -------------------------------
def normalize_message(message):
    message = message.lower()

    # Replace IP addresses
    message = re.sub(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", "<IP>", message)

    # Replace file paths
    message = re.sub(r"/[^\s]+", " <PATH> ", message)

    # Replace numbers
    message = re.sub(r"\b\d+\b", " <NUM> ", message)

    # Fix "can t" → "cannot"
    message = re.sub(r"\bcan t\b", "cannot", message)

    # Remove punctuation
    message = re.sub(r"[^\w\s<>]", " ", message)

    # Remove duplicate consecutive words
    message = re.sub(r'\b(\w+)( \1\b)+', r'\1', message)

    # Remove repeated phrases (simple heuristic)
    words = message.split()
    seen = []
    for w in words:
        if not seen or seen[-1] != w:
            seen.append(w)
    message = " ".join(seen)

    # Remove extra spaces
    message = re.sub(r"\s+", " ", message).strip()

    return message

# -------------------------------
# Step 3: Process file
# -------------------------------
cleaned_logs = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        level, message = parse_log(line)

        if message:
            normalized_msg = normalize_message(message)
            final_text = f"{level} {normalized_msg}"
            cleaned_logs.append(final_text)

# -------------------------------
# Step 4: Remove duplicates (optional)
# -------------------------------
cleaned_logs = list(set(cleaned_logs))

# -------------------------------
# Step 5: Write to output file
# -------------------------------
with open(output_file, "w", encoding="utf-8") as f:
    for log in cleaned_logs:
        f.write(log + "\n")

print(f"Processed logs saved to {output_file}")