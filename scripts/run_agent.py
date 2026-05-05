import sys
import os

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
