# backend/events/kafka_consumer.py

import asyncio
import json
from aiokafka import AIOKafkaConsumer
import logging
import os
from typing import Callable, Dict, Any
from sqlmodel import Session
from ..database import get_session
from ..services.recurring_tasks import process_completed_recurring_task
from ..services.reminders import check_and_send_reminders

logger = logging.getLogger(__name__)

class KafkaTaskConsumer:
    def __init__(self):
        self.consumer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.running = False
        
    async def start(self):
        """Initialize and start the Kafka consumer"""
        try:
            self.consumer = AIOKafkaConsumer(
                "task-events",
                "reminders",
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                group_id="todo-app-group"
            )
            await self.consumer.start()
            self.running = True
            logger.info("Kafka consumer started successfully")
            
            # Start consuming messages
            asyncio.create_task(self.consume_messages())
        except Exception as e:
            logger.error(f"Failed to start Kafka consumer: {e}")
            raise
    
    async def stop(self):
        """Stop the Kafka consumer"""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")
    
    async def consume_messages(self):
        """Continuously consume messages from Kafka topics"""
        logger.info("Starting to consume messages...")
        
        try:
            async for msg in self.consumer:
                if not self.running:
                    break
                    
                logger.info(f"Received message: {msg.topic}:{msg.partition}:{msg.offset}: key={msg.key} value={msg.value}")
                
                # Process the message based on topic
                if msg.topic == "task-events":
                    await self.process_task_event(msg.value)
                elif msg.topic == "reminders":
                    await self.process_reminder_event(msg.value)
                    
        except Exception as e:
            logger.error(f"Error in message consumption: {e}")
    
    async def process_task_event(self, event_data: Dict[str, Any]):
        """Process a task event"""
        event_type = event_data.get("event_type")
        task_data = event_data.get("task_data")
        user_id = event_data.get("user_id")
        
        logger.info(f"Processing task event: {event_type} for user {user_id}")
        
        if event_type == "completed":
            # Handle completed task - check if it's recurring
            task_id_str = task_data.get("id")
            if task_id_str:
                from uuid import UUID
                task_id = UUID(task_id_str)
                
                # Process recurring task
                with next(get_session()) as session:
                    next_task = process_completed_recurring_task(session, task_id)
                    if next_task:
                        logger.info(f"Created next occurrence of recurring task: {next_task.id}")
        
        # Additional event processing logic can be added here
    
    async def process_reminder_event(self, event_data: Dict[str, Any]):
        """Process a reminder event"""
        task_id = event_data.get("task_id")
        user_id = event_data.get("user_id")
        title = event_data.get("title")
        
        logger.info(f"Processing reminder for task {task_id}, user {user_id}")
        
        # In a real implementation, this would send a notification to the user
        # For now, we'll just log it
        logger.info(f"Sending reminder notification for task '{title}' (ID: {task_id}) to user {user_id}")

# Global instance
kafka_consumer = KafkaTaskConsumer()

# Initialize the consumer when module is loaded
async def init_kafka_consumer():
    await kafka_consumer.start()

# Cleanup function
async def close_kafka_consumer():
    await kafka_consumer.stop()