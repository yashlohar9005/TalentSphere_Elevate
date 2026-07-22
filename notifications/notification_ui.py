import streamlit as st
from database import db_session, UserInbox

def get_unread_count(user_id: int) -> int:
    with db_session() as session:
        return session.query(UserInbox).filter_by(user_id=user_id, is_read=0).count()

def render_notification_center(user_id: int):
    st.header("Notification Center")
    
    with db_session() as session:
        inbox = session.query(UserInbox).filter_by(user_id=user_id).order_by(UserInbox.created_at.desc()).all()
        
        if not inbox:
            st.info("You have no notifications.")
            return
            
        unread = [n for n in inbox if n.is_read == 0]
        read = [n for n in inbox if n.is_read == 1]
        
        tab1, tab2 = st.tabs([f"Unread ({len(unread)})", f"History ({len(read)})"])
        
        with tab1:
            if not unread:
                st.write("You're all caught up!")
            else:
                for n in unread:
                    with st.container():
                        st.markdown(f"**[{n.notification_type}]** - {n.created_at.strftime('%b %d, %H:%M')}")
                        st.info(n.message)
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button("Mark as Read", key=f"read_{n.id}"):
                                n.is_read = 1
                                session.commit()
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"del_{n.id}"):
                                session.delete(n)
                                session.commit()
                                st.rerun()
                        st.markdown("---")
                        
        with tab2:
            if not read:
                st.write("No notification history.")
            else:
                for n in read:
                    st.markdown(f"**[{n.notification_type}]** - {n.created_at.strftime('%b %d, %H:%M')}")
                    st.write(n.message)
                    if st.button("Delete", key=f"del_read_{n.id}"):
                        session.delete(n)
                        session.commit()
                        st.rerun()
                    st.markdown("---")
