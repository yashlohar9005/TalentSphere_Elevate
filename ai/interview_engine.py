import random

class InterviewEngine:
    def get_questions(self, interview_type: str) -> list:
        """
        Dynamically generates questions for the mock interview.
        """
        if interview_type == "Technical":
            return [
                "Can you explain the difference between processes and threads?",
                "How would you optimize a slow database query?",
                "Explain the concept of RESTful APIs.",
                "What is polymorphism in Object-Oriented Programming?"
            ]
        elif interview_type == "HR":
            return [
                "Tell me about yourself.",
                "Why do you want to work at this company?",
                "Where do you see yourself in 5 years?",
                "What are your salary expectations?"
            ]
        elif interview_type == "Behavioral":
            return [
                "Tell me about a time you faced a conflict in a team.",
                "Describe a situation where you had to meet a tight deadline.",
                "Give an example of a time you showed leadership.",
                "Tell me about a time you failed and what you learned."
            ]
        return ["Could you elaborate on your experience?"]

    def evaluate_interview(self, interview_type: str, answers: dict) -> dict:
        """
        Evaluates answers (simulated NLP/Speech evaluation for this implementation).
        Calculates Confidence, Communication, Technical Accuracy, Answer Relevance, Problem Solving.
        """
        # In a real environment, this would parse text length, keywords, grammar, etc.
        # We will simulate a score based on response lengths and some randomization.
        
        total_len = sum(len(ans) for ans in answers.values())
        avg_len = total_len / max(len(answers), 1)
        
        base_score = min(50 + (avg_len / 5), 95)
        
        confidence = int(base_score + random.randint(-5, 5))
        communication = int(base_score + random.randint(-5, 5))
        relevance = int(base_score + random.randint(-5, 5))
        
        if interview_type == "Technical":
            tech_acc = int(base_score + random.randint(-10, 5))
            prob_solv = int(base_score + random.randint(-5, 5))
        else:
            tech_acc = 0
            prob_solv = int(base_score + random.randint(-5, 5))
            
        overall = (confidence + communication + relevance + tech_acc + prob_solv) / (5 if interview_type == "Technical" else 4)
        overall = int(overall)
        
        if overall >= 80:
            ai_feedback = f"Excellent {interview_type} interview! You articulated your thoughts clearly."
            suggestions = ["Keep practicing concise answers.", "Maintain this level of detail."]
        elif overall >= 60:
            ai_feedback = f"Good attempt at the {interview_type} interview, but there is room for improvement."
            suggestions = ["Try to use the STAR method for behavioral questions.", "Provide more specific examples."]
        else:
            ai_feedback = f"Your {interview_type} interview needs significant improvement."
            suggestions = ["Your answers are too brief.", "Practice speaking more confidently and elaborating on your points."]
            
        return {
            "confidence": min(confidence, 100),
            "communication": min(communication, 100),
            "technical_accuracy": min(tech_acc, 100),
            "answer_relevance": min(relevance, 100),
            "problem_solving": min(prob_solv, 100),
            "overall_score": overall,
            "ai_feedback": ai_feedback,
            "improvement_suggestions": suggestions
        }
