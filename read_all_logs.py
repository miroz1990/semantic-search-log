# -------------------------------
# Step 1: Define file paths for log sources
# -------------------------------
files = [
    "data/clean_logs_apache.txt",
    "data/clean_logs_hdfs.txt",
    "data/clean_logs_linux.txt"
]

# -------------------------------
# Step 2: Reading and combining logs with source metadata
# -------------------------------
all_logs = []

def read_Logs():
    for file in files:
        # 🔹 Detect source from filename
        if "hdfs" in file.lower():
            source = "HDFS"
        elif "linux" in file.lower():
            source = "Linux"
        elif "apache" in file.lower():
            source = "Apache"
        else:
            source = "Unknown"

        # 🔹 Read file
        with open(file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        # 🔹 Add logs with metadata
        for log in lines:
            all_logs.append({
                "text": log,
                "source": source
            })

    print("Total logs before deduplication:", len(all_logs))

    return all_logs
    # -------------------------------
    # Step 3: Deduplicate logs based on text content
    # -------------------------------
def deduplicate_logs(all_logs):
    seen = set()
    unique_logs = []

    for item in all_logs:
        if item["text"] not in seen:
            seen.add(item["text"])
            unique_logs.append(item)

    print("Total logs after deduplication:", len(unique_logs))
    return unique_logs