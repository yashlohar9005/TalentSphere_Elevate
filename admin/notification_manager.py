import streamlit as st
from database import db_session, Notification
from notifications.notification_service import broadcast_notification

def render_notification_manager():
    st.subheader("Notification Center")
    
    st.write("### Send Notification")
    with st.form("send_notification_form"):
        target = st.selectbox("Target Group", [
            "All", 
            "High School Student", 
            "College Student", 
            "Working Professional", 
            "Specific User ID"
        ])
        
        specific_id = ""
        if target == "Specific User ID":
            specific_id = st.text_input("Enter User ID")
            
        message = st.text_area("Message content")
        
        if st.form_submit_button("Send Notification"):
            final_target = target if target != "Specific User ID" else f"user_{specific_id}"
            broadcast_notification(final_target, message)
            st.success("Notification successfully queued!")
            st.rerun()
            
    st.write("### Recent Notifications")
    with db_session() as session:
        notifs = session.query(Notification).order_by(Notification.created_at.desc()).limit(10).all()
        for n in notifs:
            st.markdown(f"**To [{n.target_group}]** at {n.created_at.strftime('%Y-%m-%d %H:%M')}")
            st.info(n.message)
