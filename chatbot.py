import random

class Chatbot:
    def __init__(self):
        self.greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! Ready to tackle some tasks?",
            "Hey! How can I help you with your tasks?"
        ]
        
        self.commands_help = {
            "add task": "To add a task, type 'add task' or 'add'",
            "show tasks": "To view all tasks, type 'show tasks' or 'list'",
            "complete task": "To mark a task as completed, type 'complete task' or 'done'",
            "delete task": "To delete a task, type 'delete task' or 'remove task'",
            "exit": "To exit the app, type 'exit' or 'quit'"
        }
        
        self.responses = [
            "That sounds like a good plan!",
            "I understand. Let me help you with that.",
            "Thanks for letting me know!",
            "I'm here to assist you with your tasks.",
            "Got it! How else can I help?"
        ]
        
        # Print initial greeting
        print(random.choice(self.greetings))
        self.show_menu()

    def show_menu(self):
        """Display the menu of available commands."""
        print("\nMenu Options:")
        print("1. Add a task - Type: 'add task' or 'add'")
        print("2. Show tasks - Type: 'show tasks' or 'list'")
        print("3. Mark task as completed - Type: 'complete task' or 'done'")
        print("4. Delete a task - Type: 'delete task' or 'remove task'")
        print("5. Exit - Type: 'exit' or 'quit'")
        print("\nWhat would you like to do?")

    def get_user_input(self):
        """Get input from the user."""
        return input("\nEnter your command: ").strip()

    def respond(self, user_input):
        """Generate a response based on user input."""
        user_input_lower = user_input.lower()
        
        # Check for keywords in user input to provide helpful responses
        if any(keyword in user_input_lower for keyword in ["help", "what", "how", "menu"]):
            self.show_menu()
            return "Here's the menu again. How can I assist you?"
        
        elif any(keyword in user_input_lower for keyword in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greetings)
        
        elif any(keyword in user_input_lower for keyword in ["thank", "thanks"]):
            return "You're welcome! Is there anything else I can help with?"
        
        elif any(keyword in user_input_lower for keyword in ["goodbye", "bye", "see you"]):
            return "Goodbye! Feel free to come back anytime."
        
        elif "task" in user_input_lower:
            # Provide specific help based on task-related commands
            if any(keyword in user_input_lower for keyword in ["add", "create", "new"]):
                return "To add a task, type 'add task' and then enter your task description."
            elif any(keyword in user_input_lower for keyword in ["show", "view", "list"]):
                return "To view tasks, type 'show tasks' or 'list'."
            elif any(keyword in user_input_lower for keyword in ["complete", "done", "finish"]):
                return "To mark a task as completed, type 'complete task' and enter the task ID."
            elif any(keyword in user_input_lower for keyword in ["delete", "remove"]):
                return "To delete a task, type 'delete task' and enter the task ID."
        
        # Default response
        return random.choice(self.responses)