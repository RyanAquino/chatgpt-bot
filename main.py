import os
from dotenv import load_dotenv
import openai


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAPI_API_KEY")
    model_engine = "text-davinci-003"
    print("Ctr+C to exit")

    try:
        while True:
            msg = input("message: ")
            response = openai.Completion.create(
                model=model_engine,
                prompt=msg,
                temperature=0.6
            )
            print(f"ChatGPT: {response.choices[0].text.strip()}")
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
