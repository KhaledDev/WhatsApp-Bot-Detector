import ollama
import asyncio
import pandas as pd


SYSTEM_PROMPT = """
Generate a set of messages for academic support services, including:
Messages inviting students to join WhatsApp groups for homework help and discussion
Messages offering research paper writing services with plagiarism guarantees
Messages advertising academic writing services, including case studies, reports, and presentations
Messages promoting university-specific groups for students to connect and share resources
Requirements:
Include a mix of Arabic and English messages
Use realistic but fictional WhatsApp links and phone numbers
Mention Turnitin or similar plagiarism detection services
Emphasize the benefits of the services, such as "expert guidance," "high-quality content," and "affordable prices"
Format:
Generate 10-20 messages in total
Each message should be 1-2 sentences long
Include a variety of message types, such as invitations to join WhatsApp groups, offers of research paper writing services, and promotions for academic writing services

Response Format:
only provide the messages, at the end of each message include a ">" character to seperate each item

Example Output:
Here's an example of what the output might look like:
"Need help with your math homework? Join our WhatsApp group for detailed solutions and expert guidance! https://chat.whatsapp.com/LpK83jR9qJg67tH5EzYdFb"
"هل تحتاج إلى مساعدة في كتابة البحث الجامعي؟ كتابنا الخبراء يقدمون محتوى عالي الجودة مع صفر اقتباس. واتساب +971552219876"
"Get professional help with case studies, reports, and presentations. Affordable prices, quick turnaround. Contact 0556273849"
"طلاب جامعة الإمارات! انضموا إلى مجموعتنا لمناقشة مختلف التخصصات، مشاركة الملاحظات، والاستعداد للامتحانات! https://chat.whatsapp.com/KdF8sdf93jdF8sdf"
"""


def generate_synthetic_data() -> str:
    client = ollama.Client()

    response: ollama.GenerateResponse = client.generate(
        model="llama3.2", prompt=SYSTEM_PROMPT
    )

    return response.response


if __name__ == "__main__":
    messages = generate_synthetic_data()
    print(messages)
