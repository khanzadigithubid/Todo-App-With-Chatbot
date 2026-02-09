# backend/events/kafka_producer.py

import asyncio
import json
from typing import Dict, Any
from aiokafka import AIOKafkaProducer
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class KafkaTaskProducer:
    def __init__(self):
        self.producer = None
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        
    async def start(self):
        """Initialize the Kafka producer"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            await self.producer.start()
            logger.info("Kafka producer started successfully")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            raise
    
    async def stop(self):
        """Stop the Kafka producer"""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")
    
    async def publish_task_event(self, event_type: str, task_data: Dict[str, Any], user_id: str):
        """Publish a task event to the appropriate Kafka topic"""
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return
            
        event = {
            "event_type": event_type,
            "task_data": task_data,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            topic = "task-events"
            await self.producer.send_and_wait(topic, value=event, key=user_id)
            logger.info(f"Published {event_type} event for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            raise
    
    async def publish_reminder_event(self, task_id: str, user_id: str, remind_at: str, title: str):
        """Publish a reminder event to the reminders topic"""
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return
            
        event = {
            "task_id": task_id,
            "user_id": user_id,
            "remind_at": remind_at,
            "title": title,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            topic = "reminders"
            await self.producer.send_and_wait(topic, value=event, key=user_id)
            logger.info(f"Published reminder event for task {task_id}")
        except Exception as e:
            logger.error(f"Failed to publish reminder event: {e}")
            raise

# Global instance
kafka_producer = KafkaTaskProducer()

# Initialize the producer when module is loaded
async def init_kafka_producer():
    await kafka_producer.start()

# Cleanup function
async def close_kafka_producer():
    await kafka_producer.stop()