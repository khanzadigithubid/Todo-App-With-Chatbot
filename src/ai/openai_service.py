import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenAIService:
    """
    Service class to handle OpenAI API interactions for the Todo App.
    """
    
    def __init__(self):
        # Get the API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_task_suggestions(self, current_tasks: list) -> str:
        """
        Generate task suggestions based on current tasks using OpenAI.
        
        Args:
            current_tasks: List of current tasks in the user's list
            
        Returns:
            A string containing task suggestions
        """
        if not current_tasks:
            task_context = "The user has no tasks yet."
        else:
            task_titles = [task.title for task in current_tasks]
            task_context = f"The user currently has these tasks: {', '.join(task_titles)}"
        
        prompt = f"""
        Based on the following context, suggest 3 new tasks that would be helpful for the user to add to their todo list:
        {task_context}
        
        Format your response as a numbered list with brief task titles only.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that suggests productive tasks for a todo list. Respond with a numbered list of 3 task suggestions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error generating suggestions: {str(e)}"
    
    def categorize_task(self, task_title: str) -> str:
        """
        Categorize a task based on its title using OpenAI.
        
        Args:
            task_title: The title of the task to categorize
            
        Returns:
            A string containing the category
        """
        prompt = f"""
        Categorize the following task into one of these categories: 
        Work, Personal, Health, Learning, Finance, Home, Other
        
        Task: {task_title}
        
        Just respond with the category name.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that categorizes tasks. Respond with just the category name from this list: Work, Personal, Health, Learning, Finance, Home, Other"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error categorizing task: {str(e)}"
    
    def prioritize_tasks(self, tasks: list) -> str:
        """
        Suggest a priority order for the provided tasks using OpenAI.
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            A string containing prioritized task list
        """
        if not tasks:
            return "No tasks to prioritize."
        
        task_list = "\n".join([f"- {task.title}" for task in tasks])
        
        prompt = f"""
        Based on the following tasks, suggest the order in which they should be completed, considering urgency and importance:
        
        {task_list}
        
        Respond with a numbered list in the recommended order.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that helps prioritize tasks. Respond with a numbered list in the recommended order."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error prioritizing tasks: {str(e)}"