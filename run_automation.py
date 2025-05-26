import sys
import json
from nlu import parse_command
from automation import execute_plan
from automation import IS_CLOUD

def get_assistant_response(plan, history):
    # Example: Use last user message for context-aware reply
    if plan.get('site', '').lower() == 'youtube' and plan.get('action', '') == 'play':
        video = plan.get('item', 'your video')
        # If previous message was also a play command, acknowledge follow-up
        if len(history) > 1 and history[-2]['role'] == 'user':
            prev = history[-2]['content']
            if 'another' in plan.get('item', '').lower() or 'next' in plan.get('item', '').lower():
                return f"Playing another video on YouTube."
        return f"Playing '{video}' on YouTube."
    return "Sorry, I can only help with YouTube commands right now."

if __name__ == "__main__":
    command = sys.argv[1]
    history = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
    plan = parse_command(command)
    print(f"[NLU] {plan}")
    print(f"[History] {history}")
    try:
        if IS_CLOUD:
            print("[Assistant] Browser automation is not supported in this environment. Please run locally for full functionality.")
            sys.exit(0)
        response = get_assistant_response(plan, history)
        print(f"[Assistant] {response}")
        execute_plan(plan)
        # Wait for all browser windows to close before exiting
        from automation import browser
        while True:
            if not browser.contexts:
                break
        # Optionally, print a message
        print("[Automation] All browser windows closed. Exiting.")
    except Exception as e:
        print(f"[Error] {e}") 