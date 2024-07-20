from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from typing import List
from .models import Notification, EmailNotification, NotificationType, NotificationStatus
from .database import get_session
from .email_service import send_email
from datetime import datetime

router = APIRouter()

@router.post("/notifications/", response_model=Notification)
async def create_notification(notification: Notification, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    session.add(notification)
    session.commit()
    session.refresh(notification)
    
    if notification.notification_type == NotificationType.EMAIL:
        background_tasks.add_task(process_email_notification, notification.id, session)
    
    return notification

@router.get("/notifications/", response_model=List[Notification])
def read_notifications(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    notifications = session.exec(select(Notification).offset(skip).limit(limit)).all()
    return notifications

@router.get("/notifications/{notification_id}", response_model=Notification)
def read_notification(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/notifications/email/", response_model=Notification)
async def send_email_notification(email_notification: EmailNotification, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    notification = Notification(
        user_id=0,  # You might want to add user_id to EmailNotification model
        notification_type=NotificationType.EMAIL,
        content=email_notification.body,
    )
    session.add(notification)
    session.commit()
    session.refresh(notification)
    
    background_tasks.add_task(process_email_notification, notification.id, session, email_notification)
    
    return notification

async def process_email_notification(notification_id: int, session: Session, email_notification: EmailNotification = None):
    with Session(session.engine) as new_session:
        notification = new_session.get(Notification, notification_id)
        if not notification:
            print(f"Notification {notification_id} not found")
            return
        
        if email_notification is None:
            # In a real-world scenario, you'd fetch the email details based on the notification content
            email_notification = EmailNotification(
                to_email="user@example.com",
                subject="Notification",
                body=notification.content
            )
        
        success = await send_email(email_notification.to_email, email_notification.subject, email_notification.body)
        
        if success:
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
        else:
            notification.status = NotificationStatus.FAILED
        
        new_session.add(notification)
        new_session.commit()