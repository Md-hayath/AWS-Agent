"""import sys
import os
from dotenv import load_dotenv
load_dotenv()
# Add the root directory to PYTHONPATH so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.chat_agent import ChatWorkflow
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Welcome to the AWS DevOps AI Agent!")
    print("Type 'exit' or 'quit' to stop.\n")
    
    workflow = ChatWorkflow()
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
                
            if not user_input.strip():
                continue
                
            response = workflow.run(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()
"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# ---- Fix 1: Properly resolve project root ----
ROOT_DIR = Path(__file__).resolve().parent.parent

# ---- Fix 2: Add root to PYTHONPATH ----
sys.path.append(str(ROOT_DIR))

# ---- Fix 3: Load .env explicitly from root ----
env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# ---- Debug (remove later if it hurts your feelings) ----
print("DEBUG: AWS_ACCESS_KEY_ID =", os.getenv("AWS_ACCESS_KEY_ID"))
print("DEBUG: AWS_DEFAULT_REGION =", os.getenv("AWS_DEFAULT_REGION"))

# ---- Import AFTER env is loaded ----
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

            # ---- Run agent ----
            response = workflow.run(user_input)

            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break

        except Exception as e:
            import traceback
            print("\n🔥 REAL ERROR (not your agent's fantasy version):")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()