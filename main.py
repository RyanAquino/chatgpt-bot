import openai

openai.api_key = "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"


def main():
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
            print(f"ChatGPT: {response}")
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
