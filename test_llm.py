from src.downloader.llm import generate_answer


response = generate_answer(
    "Explain UAE labour law in one sentence."
)


print(response)