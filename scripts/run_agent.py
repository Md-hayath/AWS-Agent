import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

load_dotenv(dotenv_path=ROOT_DIR / ".env")

from workflows.chat_agent import ChatWorkflow


def main():
    print("Welcome to the AWS DevOps AI Agent!")
    print("Type 'exit' or 'quit' to stop.\n")

    try:
        workflow = ChatWorkflow()
    except Exception as e:
        print("Failed to initialize workflow:")
        print(e)
        return

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            if not user_input.strip():
                continue

            response = workflow.run(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception:
            import traceback

            print("\nError while running the agent:")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()
