import sys

# Placeholder imports for NLU and automation modules
from nlu import parse_command
from automation import execute_plan

def main():
    print("AI Web Automation Agent (type 'exit' to quit)")
    while True:
        user_input = input("\nEnter command: ")
        if user_input.strip().lower() == 'exit':
            print("Goodbye!")
            break
        plan = parse_command(user_input)
        result = execute_plan(plan)
        # print(result)
        # print("[Stub] Would parse and execute:", user_input)

if __name__ == "__main__":
    main() 