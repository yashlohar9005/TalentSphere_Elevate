"""
Coding Basics Module for TalentSphere Elevate — High School.

Beginner-friendly Python lessons covering 10 topics with lesson content,
code examples, mini practice quizzes, progress tracking, and certificates.
"""

import streamlit as st
import json
from datetime import datetime
from database import db_session, CodingProgress


# ──────────────────────────────────────────────────────────────────────────────
# Lesson Content — 10 Python topics
# ──────────────────────────────────────────────────────────────────────────────

CODING_TOPICS: list[dict] = [
    {
        "name": "Python Basics",
        "icon": "🐍",
        "lesson": (
            "Python is a high-level, interpreted programming language known for its simplicity.\n\n"
            "**Key Features:**\n"
            "- Easy to read and write\n"
            "- Dynamically typed\n"
            "- Extensive standard library\n"
            "- Used in web dev, AI, data science, and more\n\n"
            "**Your First Program:**\n"
        ),
        "code": 'print("Hello, World!")\nprint("Welcome to Python!")\n\n# This is a comment\nname = "TalentSphere"\nprint(f"Welcome to {name}")',
        "quiz": [
            {"q": "What function is used to display output in Python?", "options": ["print()", "echo()", "display()", "write()"], "answer": 0},
            {"q": "Python is a __ language.", "options": ["Compiled", "Interpreted", "Assembly", "Machine"], "answer": 1},
            {"q": "Which symbol starts a comment in Python?", "options": ["//", "/*", "#", "--"], "answer": 2},
        ],
    },
    {
        "name": "Variables",
        "icon": "📦",
        "lesson": (
            "Variables are containers for storing data values. Python has no command for declaring a variable — "
            "a variable is created the moment you assign a value to it.\n\n"
            "**Rules:**\n"
            "- Must start with a letter or underscore\n"
            "- Cannot start with a number\n"
            "- Case-sensitive (age ≠ Age)\n"
        ),
        "code": '# Variable assignment\nname = "Alice"\nage = 16\nheight = 5.4\nis_student = True\n\nprint(f"{name} is {age} years old")\nprint(f"Height: {height} ft")\nprint(f"Student: {is_student}")',
        "quiz": [
            {"q": "Which is a valid variable name?", "options": ["2name", "_score", "my-var", "class"], "answer": 1},
            {"q": "Variables in Python are:", "options": ["Statically typed", "Dynamically typed", "Not typed", "Strongly compiled"], "answer": 1},
            {"q": "What does x = 5 do?", "options": ["Compares x to 5", "Assigns 5 to x", "Declares x as int", "None of these"], "answer": 1},
        ],
    },
    {
        "name": "Data Types",
        "icon": "🏷️",
        "lesson": (
            "Python has several built-in data types:\n\n"
            "| Type | Example | Description |\n"
            "|------|---------|-------------|\n"
            "| `int` | `42` | Whole numbers |\n"
            "| `float` | `3.14` | Decimal numbers |\n"
            "| `str` | `\"hello\"` | Text strings |\n"
            "| `bool` | `True` | Boolean values |\n"
            "| `list` | `[1,2,3]` | Ordered collection |\n"
            "| `dict` | `{\"a\": 1}` | Key-value pairs |\n"
        ),
        "code": '# Check types with type()\nprint(type(42))        # <class \'int\'>\nprint(type(3.14))      # <class \'float\'>\nprint(type("hello"))   # <class \'str\'>\nprint(type(True))      # <class \'bool\'>\nprint(type([1,2,3]))   # <class \'list\'>\n\n# Type conversion\nx = int("10")    # str → int\ny = str(42)      # int → str\nz = float("3.14") # str → float',
        "quiz": [
            {"q": "What is the type of 3.14?", "options": ["int", "float", "str", "bool"], "answer": 1},
            {"q": "What does type() return?", "options": ["The value", "The data type", "The variable name", "An error"], "answer": 1},
            {"q": "True and False are of type:", "options": ["int", "str", "bool", "float"], "answer": 2},
        ],
    },
    {
        "name": "Operators",
        "icon": "➕",
        "lesson": (
            "Python supports several types of operators:\n\n"
            "**Arithmetic:** `+`, `-`, `*`, `/`, `//` (floor div), `%` (modulo), `**` (power)\n\n"
            "**Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`\n\n"
            "**Logical:** `and`, `or`, `not`\n\n"
            "**Assignment:** `=`, `+=`, `-=`, `*=`, `/=`\n"
        ),
        "code": '# Arithmetic\nprint(10 + 3)   # 13\nprint(10 - 3)   # 7\nprint(10 * 3)   # 30\nprint(10 / 3)   # 3.333...\nprint(10 // 3)  # 3 (floor division)\nprint(10 % 3)   # 1 (remainder)\nprint(2 ** 3)   # 8 (power)\n\n# Comparison\nprint(5 > 3)    # True\nprint(5 == 5)   # True\n\n# Logical\nprint(True and False)  # False\nprint(True or False)   # True',
        "quiz": [
            {"q": "What does 10 // 3 return?", "options": ["3.33", "3", "4", "1"], "answer": 1},
            {"q": "What does 10 % 3 return?", "options": ["3", "0", "1", "10"], "answer": 2},
            {"q": "What is the result of True and False?", "options": ["True", "False", "None", "Error"], "answer": 1},
        ],
    },
    {
        "name": "Conditions",
        "icon": "🔀",
        "lesson": (
            "Conditional statements let your program make decisions.\n\n"
            "**Syntax:**\n"
            "```text\n"
            "if condition:\n"
            "    # code block\n"
            "elif another_condition:\n"
            "    # code block\n"
            "else:\n"
            "    # code block\n"
            "```\n\n"
            "Python uses **indentation** (4 spaces) to define code blocks.\n"
        ),
        "code": 'age = 16\n\nif age >= 18:\n    print("You can vote!")\nelif age >= 16:\n    print("Almost there!")\nelse:\n    print("Too young to vote.")\n\n# Ternary operator\nstatus = "adult" if age >= 18 else "minor"\nprint(f"Status: {status}")',
        "quiz": [
            {"q": "What keyword is used for 'otherwise if'?", "options": ["else if", "elsif", "elif", "elseif"], "answer": 2},
            {"q": "Python uses __ to define code blocks.", "options": ["Braces {}", "Indentation", "Parentheses", "Keywords"], "answer": 1},
            {"q": "What does 'if 0:' evaluate to?", "options": ["True", "False", "Error", "None"], "answer": 1},
        ],
    },
    {
        "name": "Loops",
        "icon": "🔁",
        "lesson": (
            "Loops let you repeat code multiple times.\n\n"
            "**For Loop:** Iterates over a sequence\n"
            "**While Loop:** Repeats while a condition is True\n\n"
            "**Control:** `break` exits the loop, `continue` skips to next iteration\n"
        ),
        "code": '# For loop\nfor i in range(5):\n    print(f"Count: {i}")\n\n# For loop with list\nfruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print(fruit)\n\n# While loop\ncount = 0\nwhile count < 3:\n    print(f"While: {count}")\n    count += 1\n\n# Break and continue\nfor i in range(10):\n    if i == 3:\n        continue  # Skip 3\n    if i == 7:\n        break     # Stop at 7\n    print(i)',
        "quiz": [
            {"q": "range(5) generates numbers from:", "options": ["1 to 5", "0 to 5", "0 to 4", "1 to 4"], "answer": 2},
            {"q": "Which keyword exits a loop?", "options": ["stop", "exit", "break", "end"], "answer": 2},
            {"q": "A while loop runs while condition is:", "options": ["False", "True", "None", "0"], "answer": 1},
        ],
    },
    {
        "name": "Functions",
        "icon": "⚡",
        "lesson": (
            "Functions are reusable blocks of code that perform a specific task.\n\n"
            "**Benefits:**\n"
            "- Code reusability\n"
            "- Better organization\n"
            "- Easier debugging\n\n"
            "Use `def` to define a function and `return` to send back a value.\n"
        ),
        "code": '# Basic function\ndef greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Alice"))\n\n# Default parameters\ndef power(base, exp=2):\n    return base ** exp\n\nprint(power(3))     # 9\nprint(power(3, 3))  # 27\n\n# Multiple return values\ndef min_max(numbers):\n    return min(numbers), max(numbers)\n\nlow, high = min_max([3, 1, 4, 1, 5])\nprint(f"Min: {low}, Max: {high}")',
        "quiz": [
            {"q": "Which keyword defines a function?", "options": ["func", "function", "def", "define"], "answer": 2},
            {"q": "What does return do?", "options": ["Prints output", "Sends back a value", "Ends the program", "Creates a variable"], "answer": 1},
            {"q": "Can a function have default parameters?", "options": ["Yes", "No", "Only in Python 3", "Only for strings"], "answer": 0},
        ],
    },
    {
        "name": "Lists",
        "icon": "📋",
        "lesson": (
            "Lists are ordered, mutable collections that can hold different data types.\n\n"
            "**Key Operations:**\n"
            "- Access: `list[index]` (0-indexed)\n"
            "- Add: `append()`, `insert()`, `extend()`\n"
            "- Remove: `remove()`, `pop()`, `del`\n"
            "- Slice: `list[start:end]`\n"
        ),
        "code": '# Create a list\nfruits = ["apple", "banana", "cherry"]\n\n# Access elements\nprint(fruits[0])   # apple\nprint(fruits[-1])  # cherry\n\n# Add elements\nfruits.append("date")\nfruits.insert(1, "avocado")\n\n# Remove elements\nfruits.remove("banana")\npopped = fruits.pop()\n\n# Slicing\nnumbers = [0, 1, 2, 3, 4, 5]\nprint(numbers[1:4])   # [1, 2, 3]\nprint(numbers[:3])    # [0, 1, 2]\n\n# List comprehension\nsquares = [x**2 for x in range(5)]\nprint(squares)  # [0, 1, 4, 9, 16]',
        "quiz": [
            {"q": "Lists are 0-indexed. What is [10,20,30][1]?", "options": ["10", "20", "30", "Error"], "answer": 1},
            {"q": "Which method adds to the end of a list?", "options": ["add()", "push()", "append()", "insert()"], "answer": 2},
            {"q": "Are lists mutable?", "options": ["Yes", "No", "Only with numbers", "Only in Python 3"], "answer": 0},
        ],
    },
    {
        "name": "Dictionary",
        "icon": "📖",
        "lesson": (
            "Dictionaries store data as key-value pairs. They are unordered (insertion order preserved since 3.7), "
            "mutable, and keys must be unique.\n\n"
            "**Key Operations:**\n"
            "- Access: `dict[key]` or `dict.get(key)`\n"
            "- Add/Update: `dict[key] = value`\n"
            "- Remove: `del dict[key]`, `dict.pop(key)`\n"
            "- Iterate: `dict.keys()`, `dict.values()`, `dict.items()`\n"
        ),
        "code": '# Create a dictionary\nstudent = {\n    "name": "Alice",\n    "age": 16,\n    "grade": "11th",\n    "subjects": ["Math", "Science"]\n}\n\n# Access\nprint(student["name"])         # Alice\nprint(student.get("gpa", 0))   # 0 (default)\n\n# Add / Update\nstudent["gpa"] = 3.8\nstudent["age"] = 17\n\n# Iterate\nfor key, value in student.items():\n    print(f"{key}: {value}")\n\n# Dictionary comprehension\nsquares = {x: x**2 for x in range(5)}\nprint(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}',
        "quiz": [
            {"q": "Dictionary keys must be:", "options": ["Mutable", "Unique", "Integers", "Strings only"], "answer": 1},
            {"q": "What does .get(key, default) return if key is missing?", "options": ["None", "Error", "The default value", "False"], "answer": 2},
            {"q": "How to add a new key-value pair?", "options": ["dict.add(k,v)", "dict[k] = v", "dict.append(k,v)", "dict.insert(k,v)"], "answer": 1},
        ],
    },
    {
        "name": "Strings",
        "icon": "🔤",
        "lesson": (
            "Strings are sequences of characters enclosed in quotes.\n\n"
            "**Key Methods:**\n"
            "- `upper()`, `lower()`, `title()`, `strip()`\n"
            "- `split()`, `join()`, `replace()`\n"
            "- `find()`, `count()`, `startswith()`, `endswith()`\n"
            "- f-strings: `f\"Hello {name}\"`\n"
        ),
        "code": 'text = "  Hello, World!  "\n\n# Methods\nprint(text.strip())        # "Hello, World!"\nprint(text.lower())        # "  hello, world!  "\nprint(text.upper())        # "  HELLO, WORLD!  "\nprint(text.replace("World", "Python"))\n\n# Split and Join\nwords = "apple,banana,cherry".split(",")\nprint(words)  # [\'apple\', \'banana\', \'cherry\']\njoined = " - ".join(words)\nprint(joined)  # apple - banana - cherry\n\n# f-strings\nname = "Alice"\nage = 16\nprint(f"{name} is {age} years old")\n\n# String slicing\ns = "Python"\nprint(s[0:3])   # Pyt\nprint(s[::-1])   # nohtyP (reversed)',
        "quiz": [
            {"q": "What does 'hello'.upper() return?", "options": ["Hello", "HELLO", "hello", "hELLO"], "answer": 1},
            {"q": "How to reverse a string s?", "options": ["s.reverse()", "reversed(s)", "s[::-1]", "s[-1:0]"], "answer": 2},
            {"q": "f-strings are available in Python:", "options": ["2.7+", "3.0+", "3.6+", "All versions"], "answer": 2},
        ],
    },
]


def render_coding_basics(user_id: int) -> None:
    """Renders the Coding Basics page."""
    st.header("💻 Coding Basics — Python")
    st.write("Learn Python step by step with lessons, code examples, and mini quizzes.")

    # ── Load progress ──
    with db_session() as session:
        progress_records = session.query(CodingProgress).filter_by(user_id=user_id).all()
        progress_map: dict[str, dict] = {}
        for p in progress_records:
            progress_map[p.topic] = {
                "lesson_completed": p.lesson_completed,
                "quiz_score": p.quiz_score,
            }

    # ── Overall Progress ──
    total_topics = len(CODING_TOPICS)
    completed_lessons = sum(1 for t in CODING_TOPICS if progress_map.get(t["name"], {}).get("lesson_completed", 0))
    completed_quizzes = sum(1 for t in CODING_TOPICS if progress_map.get(t["name"], {}).get("quiz_score") is not None)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Topics", f"{completed_lessons}/{total_topics}")
    with col2:
        st.metric("Quizzes Passed", f"{completed_quizzes}/{total_topics}")
    with col3:
        pct = int((completed_lessons + completed_quizzes) / (total_topics * 2) * 100)
        st.metric("Overall Progress", f"{pct}%")

    st.progress(pct / 100)

    # ── Certificate ──
    if completed_lessons == total_topics and completed_quizzes == total_topics:
        st.success("🎉 Congratulations! You've completed all Python Basics lessons and quizzes!")
        st.balloons()
        with st.container(border=True):
            st.markdown("### 🏆 Certificate of Completion")
            st.markdown("**Python Coding Basics** — TalentSphere Elevate")
            st.markdown(f"Awarded to **User #{user_id}** for completing all 10 Python topics.")

    st.markdown("---")

    # ── Topic Cards ──
    for i, topic in enumerate(CODING_TOPICS):
        tp = progress_map.get(topic["name"], {})
        lesson_done = tp.get("lesson_completed", 0)
        quiz_score = tp.get("quiz_score")

        status = "✅" if lesson_done and quiz_score is not None else "📖"
        with st.expander(f"{status} {topic['icon']} {topic['name']}", expanded=(i == 0 and not lesson_done)):
            # Lesson tab and Quiz tab
            tab_lesson, tab_quiz = st.tabs(["📖 Lesson", "📝 Quiz"])

            with tab_lesson:
                st.markdown(topic["lesson"])
                st.text(topic["code"])

                if not lesson_done:
                    if st.button(f"✅ Mark as Read", key=f"lesson_done_{topic['name']}"):
                        with db_session() as session:
                            existing = session.query(CodingProgress).filter_by(
                                user_id=user_id, topic=topic["name"]
                            ).first()
                            if existing:
                                existing.lesson_completed = 1
                                existing.completed_at = datetime.utcnow()
                            else:
                                session.add(CodingProgress(
                                    user_id=user_id, topic=topic["name"],
                                    lesson_completed=1, completed_at=datetime.utcnow(),
                                ))
                        st.rerun()
                else:
                    st.success("Lesson completed! ✅")

            with tab_quiz:
                if quiz_score is not None:
                    st.success(f"Quiz completed! Score: {quiz_score}%")
                elif not lesson_done:
                    st.info("Complete the lesson first to unlock the quiz.")
                else:
                    _render_quiz(user_id, topic)


def _render_quiz(user_id: int, topic: dict) -> None:
    """Renders the mini practice quiz for a topic."""
    questions = topic["quiz"]
    with st.form(f"quiz_form_{topic['name']}"):
        answers: list[int] = []
        for j, q in enumerate(questions):
            st.markdown(f"**Q{j + 1}.** {q['q']}")
            ans = st.radio("Select:", q["options"], key=f"cq_{topic['name']}_{j}", horizontal=True, label_visibility="collapsed")
            answers.append(q["options"].index(ans))

        if st.form_submit_button("Submit Quiz"):
            correct = sum(1 for j, a in enumerate(answers) if a == questions[j]["answer"])
            score = int(correct / len(questions) * 100)

            with db_session() as session:
                existing = session.query(CodingProgress).filter_by(
                    user_id=user_id, topic=topic["name"]
                ).first()
                if existing:
                    existing.quiz_score = score
                    existing.completed_at = datetime.utcnow()
                else:
                    session.add(CodingProgress(
                        user_id=user_id, topic=topic["name"],
                        lesson_completed=1, quiz_score=score,
                        completed_at=datetime.utcnow(),
                    ))

            if score >= 70:
                st.success(f"🎉 Passed! Score: {score}% ({correct}/{len(questions)})")
            else:
                st.warning(f"Score: {score}% ({correct}/{len(questions)}). Review the lesson and try again!")

            # Show answers
            for j, q in enumerate(questions):
                correct_ans = q["options"][q["answer"]]
                user_ans = q["options"][answers[j]]
                if answers[j] == q["answer"]:
                    st.markdown(f"✅ Q{j + 1}: {correct_ans}")
                else:
                    st.markdown(f"❌ Q{j + 1}: Your answer: {user_ans} → Correct: {correct_ans}")
            st.rerun()
