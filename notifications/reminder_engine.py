from database import db_session, User, ResumeData, Progress, UserInbox
from notifications.notification_service import send_notification

def run_diagnostics(user_id: int, session=None):
    """
    Rule-based scheduler. Runs silently on login or dashboard load.
    Checks user state and drops reminders into their inbox if criteria match.
    """
    def _run(s):
        user = s.query(User).filter_by(id=user_id).first()
        if not user:
            return
            
        # To prevent spam, we check if they already have an unread warning for these specific things
        existing_unread = s.query(UserInbox).filter_by(user_id=user_id, is_read=0).all()
        existing_msgs = [m.message for m in existing_unread]
        
        # 1. Missing Resume
        resume = s.query(ResumeData).filter_by(user_id=user_id).first()
        res_msg = "You haven't built a resume yet! Complete your profile to unlock ATS scoring."
        if not resume and res_msg not in existing_msgs:
            send_notification(user_id, "Warning", res_msg, s)
            
        # 2. Pending Roadmap Tasks
        pending = s.query(Progress).filter(Progress.roadmap.has(user_id=user_id), Progress.is_completed == 0).count()
        task_msg = f"You have {pending} pending tasks in your active roadmap. Keep going!"
        if pending > 0 and task_msg not in existing_msgs:
            send_notification(user_id, "Reminder", task_msg, s)
            
        # 3. Certificates Ready
        completed = s.query(Progress).filter(Progress.roadmap.has(user_id=user_id), Progress.is_completed == 1).count()
        cert_msg = "You have unlocked the Course Completion Certificate! Check the Reports tab."
        if completed >= 5 and cert_msg not in existing_msgs:
            # Check if they have ANY cert message
            has_cert_msg = any("unlocked the Course Completion" in m for m in existing_msgs)
            if not has_cert_msg:
                send_notification(user_id, "Achievement", cert_msg, s)

    if session:
        _run(session)
    else:
        with db_session() as s:
            _run(s)
