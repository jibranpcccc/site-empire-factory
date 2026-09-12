import os

site = r"c:\Users\jibra\Desktop\1\20 blogs\developer-coding-hub"
for root, dirs, files in os.walk(site):
    for f in files:
        fp = os.path.join(root, f)
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                if "https://discord.gg/langchain" in content:
                    print(f"Found in {fp}")
        except Exception as e:
            pass
