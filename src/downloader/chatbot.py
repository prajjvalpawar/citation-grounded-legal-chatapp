from retriever import retrieve_documents
from llm import generate_answer
from prompt import SYSTEM_PROMPT


def chatbot(question, history=None):

    documents, metadata = retrieve_documents(question)

    context = ""

    for i, doc in enumerate(documents):

        context += f"""

Document:
{metadata[i].get('title')}

Source:
{metadata[i].get('source')}

Content:
{doc}

-------------------

"""

    # -----------------------
    # Conversation Memory
    # -----------------------

    conversation = ""

    if history:

        # Keep only last 6 messages
        for message in history[-6:]:

            role = message["role"].capitalize()

            conversation += f"{role}: {message['content']}\n"

    prompt = f"""
You are a helpful UAE Legal Information Assistant.

Use the legal context below to answer the user's question.

If the current question depends on previous conversation,
use the conversation history for understanding the context.

Never make up legal information.

If the answer is not available in the provided legal context,
reply:

"I could not find this information in the provided legal documents."

----------------------------------------

Conversation History:

{conversation}

----------------------------------------

Legal Context:

{context}

----------------------------------------

Current Question:

{question}

Answer:
"""

    answer = generate_answer(prompt)

    return answer


if __name__ == "__main__":

    print("UAE Legal Chatbot Started")

    history = []

    while True:

        question = input("\nAsk your legal question: ")

        if question.lower() == "exit":
            break

        answer = chatbot(question, history)

        print("\nAnswer:\n")
        print(answer)

        history.append(
            {
                "role": "user",
                "content": question
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )