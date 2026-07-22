import streamlit as st
import json
from database import db_session, Quiz, Question

def render_quiz_manager():
    st.subheader("Quiz Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Create Assessment")
        with st.form("create_quiz_form"):
            title = st.text_input("Assessment Title")
            if st.form_submit_button("Create Assessment"):
                with db_session() as session:
                    new_quiz = Quiz(title=title)
                    session.add(new_quiz)
                st.success(f"Created: {title}")
                st.rerun()
                
        st.write("### Existing Assessments")
        with db_session() as session:
            quizzes = session.query(Quiz).all()
            quiz_options = {q.title: q.id for q in quizzes}
            
    with col2:
        if not quiz_options:
            st.info("No assessments created yet.")
            return
            
        selected_quiz = st.selectbox("Select Assessment to Edit", list(quiz_options.keys()))
        quiz_id = quiz_options[selected_quiz]
        
        with db_session() as session:
            q_obj = session.query(Quiz).filter_by(id=quiz_id).first()
            is_pub = q_obj.is_published == 1
            if st.checkbox("Published", value=is_pub):
                if not is_pub:
                    q_obj.is_published = 1
                    session.commit()
            else:
                if is_pub:
                    q_obj.is_published = 0
                    session.commit()
                    
            st.write("### Add Question")
            with st.form("add_question_form"):
                q_text = st.text_input("Question")
                opts = st.text_area("Options (one per line)")
                ans = st.text_input("Exact Correct Answer")
                
                if st.form_submit_button("Add Question"):
                    opt_list = [o.strip() for o in opts.split("\n") if o.strip()]
                    new_q = Question(quiz_id=quiz_id, question_text=q_text, options=json.dumps(opt_list), correct_answer=ans)
                    session.add(new_q)
                    session.commit()
                    st.success("Added question!")
                    st.rerun()
                    
            st.write("### Questions")
            for q in q_obj.questions:
                st.markdown(f"**Q:** {q.question_text}")
                st.write(f"*Options:* {', '.join(json.loads(q.options))}")
                st.write(f"*Answer:* {q.correct_answer}")
                if st.button("Delete", key=f"del_q_{q.id}"):
                    session.delete(q)
                    session.commit()
                    st.rerun()
                st.markdown("---")
