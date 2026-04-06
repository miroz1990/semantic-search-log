import re

input_file = "data/Linux.log"
output_file = "data/clean_logs_linux.txt"

clean_logs = set()

with open(input_file, encoding="utf-8", errors="ignore") as f:
    for line in f:
    # 1. Remove timestamp + hostname
        line = re.sub(r"^\w{3}\s+\d+\s+\d+:\d+:\d+\s+\S+\s+", "", line)

    # 2. Remove numbers, versions, sizes
        line = re.sub(r"0x[a-fA-F0-0]+", "hex", line)
        line = re.sub(r"\b\d+(\.\d+)?\b", "", line)   # numbers
        line = re.sub(r"\b\w*\d+\w*\b", "", line)     # words with numbers

    # 3. Lowercase
        line = line.lower()

    # 4. Remove punctuation
        line = re.sub(r"[^\w\s]", " ", line)

    # 5. Remove extra spaces
        line = re.sub(r"\s+", " ", line).strip()


        if len(line) > 10:
            clean_logs.add(line)



with open(output_file, "w") as f:
    for log in clean_logs:
        f.write(log + "\n")

print("Clean logs:", len(clean_logs))

# with open("data/clean_logs_linux.txt") as f:
#     logs = [line.strip() for line in f]

print("Saved successfully!")
