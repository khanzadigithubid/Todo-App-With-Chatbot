from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from openai._exceptions import APIConnectionError, AuthenticationError, RateLimitError
from ...tools.registry import tool_registry
from ...database import get_session # Import get_session
from sqlmodel import Session # Import Session
from uuid import UUID
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def get_current_user_id(request: Request) -> UUID:
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UUID(user_id)

def get_openai_client():
    """Create and return an OpenAI client, initializing it only when needed."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "":
        raise ValueError("OPENAI_API_KEY environment variable not set or empty")
    return OpenAI(api_key=api_key)

# Get tools from registry
add_task_tool = tool_registry.get_tool_instance("add_task")
list_tasks_tool = tool_registry.get_tool_instance("list_tasks")
update_task_tool = tool_registry.get_tool_instance("update_task")
delete_task_tool = tool_registry.get_tool_instance("delete_task")
toggle_completion_tool = tool_registry.get_tool_instance("toggle_task_completion")

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

class ChatRequest(BaseModel):
    message: str
    locale: str = "en"

@router.post("/")
def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id)
):
    try:
        # Validate and get OpenAI client
        try:
            client = get_openai_client()
        except ValueError as ve:
            logger.error(f"OpenAI client configuration error: {str(ve)}")
            raise HTTPException(status_code=500, detail=f"Configuration error: {str(ve)}")

        # Create the assistant inside the function
        # Use the locale from the request, defaulting to English
        language_instruction = "Please respond in English." if request.locale == "en" else f"Please respond in {request.locale}."

        try:
            assistant = client.beta.assistants.create(
                name="Task Manager",
                instructions=f"You are a helpful assistant for managing tasks. {language_instruction} You have access to the user's tasks automatically. Do not ask the user for their ID or mention that you're using their ID. Simply perform the requested task operations on their behalf.",
                tools=tools,
                model="gpt-4o",
            )
        except AuthenticationError:
            logger.error("OpenAI authentication failed - invalid API key")
            raise HTTPException(status_code=401, detail="Authentication failed: Invalid OpenAI API key")
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error: {str(e)}")
            raise HTTPException(status_code=502, detail="Failed to connect to OpenAI service. Please check your network connection and API key.")
        except RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded. Please try again later.")
        except Exception as e:
            logger.error(f"Error creating OpenAI assistant: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize AI assistant: {str(e)}")

        try:
            thread = client.beta.threads.create()
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=request.message,
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error during thread creation: {str(e)}")
            raise HTTPException(status_code=502, detail="Failed to connect to OpenAI service during processing.")
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
                            # Execute the tool using the synchronous method
                            try:
                                output = tool_registry.execute_tool("add_task", **function_args)
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
                                output = tool_registry.execute_tool("list_tasks", **function_args)
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
                                output = tool_registry.execute_tool("toggle_task_completion", **function_args)
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
                                output = tool_registry.execute_tool("delete_task", **function_args)
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
                                output = tool_registry.execute_tool("update_task", **function_args)
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
                    except APIConnectionError as e:
                        logger.error(f"OpenAI connection error during tool output submission: {str(e)}")
                        raise HTTPException(status_code=502, detail="Failed to connect to OpenAI service during processing.")
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error during run execution: {str(e)}")
            raise HTTPException(status_code=502, detail="Failed to connect to OpenAI service during processing.")
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            logger.error(f"Error during OpenAI run execution: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error during AI processing: {str(e)}")

        try:
            messages = client.beta.threads.messages.list(thread_id=thread.id)
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error during message retrieval: {str(e)}")
            raise HTTPException(status_code=502, detail="Failed to connect to OpenAI service during response retrieval.")
        except Exception as e:
            logger.error(f"Error retrieving OpenAI messages: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving AI response: {str(e)}")

        # Prepare the response
        response_data = {
            "response": messages.data[0].content[0].text.value if messages.data and messages.data[0].content else "I processed your request but couldn't generate a response. Please try again."
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
