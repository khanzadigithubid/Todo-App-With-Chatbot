from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from ...database import get_session
from sqlmodel import Session
from ...models import Conversation, Message
from ...auth_schemas import get_current_user_id
import os
from openai import OpenAI
from ...tools.registry import tool_registry
from ...tools.add_task import AddTaskTool
from ...tools.list_tasks import ListTasksTool
from ...tools.update_task import UpdateTaskTool
from ...tools.delete_task import DeleteTaskTool
from ...tools.toggle_completion import ToggleTaskCompletionTool
import json
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    tool_calls: Optional[List[Dict[str, Any]]] = []

def get_openai_client():
    """Create and return an OpenAI client, initializing it only when needed."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "":
        raise ValueError("OPENAI_API_KEY environment variable not set or empty")
    return OpenAI(api_key=api_key)

# Get tools from registry
add_task_tool = AddTaskTool()
list_tasks_tool = ListTasksTool()
update_task_tool = UpdateTaskTool()
delete_task_tool = DeleteTaskTool()
toggle_completion_tool = ToggleTaskCompletionTool()

# Define tools schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": add_task_tool.description,
            "parameters": add_task_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": list_tasks_tool.description,
            "parameters": list_tasks_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Marks a task as complete.",
            "parameters": toggle_completion_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": delete_task_tool.description,
            "parameters": delete_task_tool.parameters,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": update_task_tool.description,
            "parameters": update_task_tool.parameters,
        },
    },
]

@router.post("/")
async def chat_endpoint(
    chat_request: ChatRequest,
    user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    try:
        # Validate and get OpenAI client
        try:
            client = get_openai_client()
        except ValueError as ve:
            logger.error(f"OpenAI client configuration error: {str(ve)}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")

        # Create or get conversation
        conversation = None
        if chat_request.conversation_id:
            conversation = session.get(Conversation, chat_request.conversation_id)
            if not conversation or conversation.user_id != str(user_id):
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=str(user_id))
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Create the assistant
        try:
            assistant = client.beta.assistants.create(
                name="Task Manager",
                instructions=f"You are a helpful assistant for managing tasks. You have access to the user's tasks automatically. Do not ask the user for their ID or mention that you're using their ID. Simply perform the requested task operations on their behalf.",
                tools=tools,
                model="gpt-4o",
            )
        except Exception as e:
            logger.error(f"Error creating OpenAI assistant: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize AI assistant: {str(e)}")

        try:
            # Create thread or get existing one from conversation if stored
            thread = client.beta.threads.create()
            
            # Add user message to the thread
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=chat_request.message,
            )
            
            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
        except Exception as e:
            logger.error(f"Error during OpenAI thread/run creation: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error during AI processing: {str(e)}")

        # Track task operations for frontend display
        task_operations = []

        try:
            # Add timeout to prevent infinite loops
            import time
            start_time = time.time()
            timeout = 60  # 60 seconds timeout

            while run.status != "completed":
                # Check for timeout
                if time.time() - start_time > timeout:
                    logger.error("Chat processing timeout exceeded")
                    raise HTTPException(status_code=408, detail="Processing timeout exceeded")

                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []

                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        # For all operations that require a user_id, ensure it's set to the authenticated user ID
                        if function_name in ["add_task", "list_tasks", "update_task", "delete_task", "complete_task", "toggle_task_completion"]:
                            function_args["user_id"] = str(user_id)  # Use the authenticated user ID

                        if function_name == "add_task":
                            # Execute the tool
                            try:
                                output = add_task_tool.execute(**function_args)
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps(output),
                                    }
                                )
                                # Track the added task for frontend display
                                task_operations.append({"type": "add_task", "task": output})
                            except Exception as e:
                                logger.error(f"Error executing add_task tool: {str(e)}")
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps({"error": f"Failed to add task: {str(e)}"}),
                                    }
                                )
                        elif function_name == "list_tasks":
                            try:
                                output = list_tasks_tool.execute(**function_args)
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps(output),
                                    }
                                )
                                # Track the listed tasks for frontend display
                                task_operations.append({"type": "list_tasks", "tasks": output})
                            except Exception as e:
                                logger.error(f"Error executing list_tasks tool: {str(e)}")
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps({"error": f"Failed to list tasks: {str(e)}"}),
                                    }
                                )
                        elif function_name == "complete_task":
                            # For complete_task, we need to toggle the completion status
                            try:
                                output = toggle_completion_tool.execute(**function_args)
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps(output),
                                    }
                                )
                                # Track the completed task for frontend display
                                task_operations.append({"type": "complete_task", "task": output})
                            except Exception as e:
                                logger.error(f"Error executing toggle_task_completion tool: {str(e)}")
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps({"error": f"Failed to complete task: {str(e)}"}),
                                    }
                                )
                        elif function_name == "delete_task":
                            try:
                                output = delete_task_tool.execute(**function_args)
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps(output),
                                    }
                                )
                                # Track the deleted task for frontend display
                                task_operations.append({"type": "delete_task", "task": output})
                            except Exception as e:
                                logger.error(f"Error executing delete_task tool: {str(e)}")
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps({"error": f"Failed to delete task: {str(e)}"}),
                                    }
                                )
                        elif function_name == "update_task":
                            try:
                                output = update_task_tool.execute(**function_args)
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps(output),
                                    }
                                )
                                # Track the updated task for frontend display
                                task_operations.append({"type": "update_task", "task": output})
                            except Exception as e:
                                logger.error(f"Error executing update_task tool: {str(e)}")
                                tool_outputs.append(
                                    {
                                        "tool_call_id": tool_call.id,
                                        "output": json.dumps({"error": f"Failed to update task: {str(e)}"}),
                                    }
                                )

                    try:
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                        )
                    except Exception as e:
                        logger.error(f"Error during tool output submission: {str(e)}")
                        raise HTTPException(status_code=500, detail="Error during AI processing")
        except Exception as e:
            logger.error(f"Error during OpenAI run execution: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error during AI processing: {str(e)}")

        try:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
        except Exception as e:
            logger.error(f"Error retrieving OpenAI messages: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving AI response: {str(e)}")

        # Store user message in database
        user_message = Message(
            user_id=str(user_id),
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message
        )
        session.add(user_message)

        # Get AI response and store in database
        ai_response = messages.data[0].content[0].text.value if messages.data and messages.data[0].content else "I processed your request but couldn't generate a response. Please try again."
        
        ai_message = Message(
            user_id=str(user_id),
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        session.add(ai_message)
        session.commit()

        # Prepare the response
        response_data = {
            "response": ai_response,
            "conversation_id": conversation.id
        }

        # Add task information to the response if any task operations occurred
        if task_operations:
            # Extract tasks from operations for frontend display
            all_tasks = []
            for operation in task_operations:
                if "task" in operation:
                    all_tasks.append(operation["task"])
                elif "tasks" in operation:
                    all_tasks.extend(operation["tasks"])

            if all_tasks:
                response_data["tasks"] = all_tasks

        return response_data
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during processing.")