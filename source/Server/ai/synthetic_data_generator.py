import ollama
import asyncio
import pandas as pd
import re


SYSTEM_PROMPT = """
Generate a set of legitimate academic support messages in Arabic and English, including:
Messages inviting students to join study groups for collaborative learning
Messages promoting tutoring services with qualified instructors
Messages advertising academic workshops on research methods and writing skills
Messages promoting university library resources and study sessions
Messages about academic counseling and guidance services

Requirements:
- Include ACTUAL Arabic text mixed with English (not romanized Arabic)
- Use realistic Arabic phrases like: "مجموعة دراسية", "مساعدة أكاديمية", "طلاب الجامعة", "دروس خصوصية"
- Mix languages naturally in the same message
- Use realistic but fictional contact information
- Focus on legitimate academic support that promotes learning and understanding

Examples of desired style:
"انضم إلى مجموعة دراسية للـ Math والـ Physics! WhatsApp: 050-123-4567"
"دروس خصوصية في English Writing و Research Methods. اتصل الآن!"
"مكتبة الجامعة تقدم study sessions مجانية كل يوم أحد"
"Hello this account helps in exams, assignments, tests, homework and advanced projects at a good level in all subjects https://chat.whatsapp.com/BAe8QbR9qjG89tJ5AgymAY https://api.whatsapp.com/send?phone=+967736631021"
""



Format:
Generate 15-20 messages in total
Each message should be 1-2 sentences long
Include variety: some pure Arabic, some pure English, some mixed
Focus on legitimate academic achievement and learning support

Response Format:
ONLY provide the messages separated by ">", NO other text, commentary, explanations, or formatting.
Each message must be complete and end with ">" before the next message starts.
"""


def generate_synthetic_data() -> str:
    client = ollama.Client()

    response: ollama.GenerateResponse = client.generate(
        model="llama3.2", prompt=SYSTEM_PROMPT
    )

    return response.response


def extract_messages(response: str) -> pd.DataFrame:
    # Clean the response - remove extra whitespace and newlines
    cleaned_response = re.sub(r"\s+", " ", response.strip())

    # Split by '>' and clean each message
    messages = []
    for msg in cleaned_response.split(">"):
        msg = msg.strip()
        # Remove any quotes at the beginning/end
        msg = re.sub(r'^["\'""]|["\'""]$', "", msg)
        if msg and len(msg) > 10:  # Only include messages with reasonable length
            messages.append(msg)

    print(f"Extracted {len(messages)} messages:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}: {msg[:50]}...")

    return pd.DataFrame(messages, columns=["message"])


if __name__ == "__main__":
    messages = generate_synthetic_data()
    df = extract_messages(messages)
    df.to_csv("source/Server/ai/Data/synthetic_academic_messages.csv", index=True)
    print(f"\nFinal DataFrame shape: {df.shape}")
    print(df.head())
