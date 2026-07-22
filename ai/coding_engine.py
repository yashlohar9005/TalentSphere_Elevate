import random

class CodingEngine:
    def get_topics(self) -> list:
        return [
            "Python", "Java", "C", "C++", "SQL", "DBMS", "Data Structures", 
            "Algorithms", "Operating Systems", "Computer Networks", "HTML", 
            "CSS", "JavaScript", "React", "Node.js", "Logical Reasoning", "Aptitude"
        ]
        
    def generate_questions(self, topic: str, num_questions: int = 5) -> list:
        """
        In a real application, this would fetch from a database of questions.
        For now, we generate placeholder questions dynamically based on the topic.
        """
        questions = []
        for i in range(num_questions):
            questions.append({
                "id": i,
                "question": f"Sample advanced {topic} question #{i+1}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": "Option A"
            })
        return questions

    def evaluate_assessment(self, topic: str, answers: dict, total: int) -> dict:
        """
        Evaluates the submitted answers and generates analysis.
        """
        # Simulate evaluation (assumes all submitted answers are "Option A" for simplicity, or just randomize)
        # Actually, let's just calculate based on what was passed.
        correct_count = 0
        for q_id, ans in answers.items():
            if ans == "Option A": # Using the mock correct answer
                correct_count += 1
                
        score = int((correct_count / total) * 100) if total > 0 else 0
        
        # Topic-wise analysis (mocked)
        weak_topics = []
        strong_topics = []
        if score > 75:
            strong_topics.append(f"Core {topic} concepts")
            weak_topics.append(f"Advanced {topic} optimizations")
            ai_suggestions = f"Great job! You have a solid grasp of {topic}. Focus on advanced algorithmic optimizations next."
        else:
            weak_topics.append(f"Basic {topic} syntax and fundamentals")
            strong_topics.append("Theoretical understanding")
            ai_suggestions = f"You need more practice in {topic}. Review the fundamentals and practice basic problems."

        return {
            "topic": topic,
            "score": score,
            "total_questions": total,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "ai_suggestions": ai_suggestions
        }
