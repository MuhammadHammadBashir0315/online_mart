from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    notification_type: NotificationType
    content: str
    status: NotificationStatus = Field(default=NotificationStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))
    sent_at: Optional[datetime] = None

class EmailNotification(SQLModel):
    to_email: str
    subject: str
    body: str