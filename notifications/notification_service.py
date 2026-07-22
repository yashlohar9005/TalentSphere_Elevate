from database import db_session, User, UserInbox, Notification

def send_notification(user_id: int, notif_type: str, message: str, session=None):
    """Sends a notification directly to a user's inbox."""
    if session:
        inbox_item = UserInbox(user_id=user_id, notification_type=notif_type, message=message)
        session.add(inbox_item)
    else:
        with db_session() as s:
            inbox_item = UserInbox(user_id=user_id, notification_type=notif_type, message=message)
            s.add(inbox_item)

def broadcast_notification(target_group: str, message: str):
    """Sends a notification to a specific group and adds it to their personal inboxes."""
    with db_session() as session:
        # Save to global notifications list
        global_notif = Notification(target_group=target_group, message=message)
        session.add(global_notif)
        
        # Dispatch to inboxes
        if target_group == "All":
            users = session.query(User).all()
        elif target_group.startswith("user_"):
            try:
                uid = int(target_group.split("_")[1])
                users = session.query(User).filter_by(id=uid).all()
            except ValueError:
                users = []
        else:
            users = session.query(User).filter_by(user_type=target_group).all()
            
        for u in users:
            send_notification(u.id, "Information", f"[Broadcast] {message}", session)
