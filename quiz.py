import os
import time
import json


class Quiz:
    def __init__(self, title, questions):
        """
        Initialize a quiz with a title and list of questions.

        Args:
            title (str): The title/topic of the quiz
            questions (list): List of question dictionaries
        """
        self.title = title
        self.questions = questions
        self.total_questions = len(questions)
        self.correct_answers = 0

    def run_quiz(self):
        """Run the entire quiz and return the final score."""
        clear_screen()
        print(f"=== {self.title} QUIZ ===\n")

        for idx, question in enumerate(self.questions):
            if self.present_question(idx + 1, question):
                self.correct_answers += 1

        self.show_final_score()
        return self.correct_answers, self.total_questions

    def present_question(self, question_number, question_data):
        """
        Present a single question to the user and handle their response.

        Args:
            question_number (int): The current question number
            question_data (dict): The question data

        Returns:
            bool: True if answered correctly, False otherwise
        """
        print(f"Question {question_number}/{self.total_questions}")
        print(f"\n{question_data['question']}\n")

        # Handle different question types
        question_type = question_data.get("type", "multiple_choice")

        if question_type == "true_false":
            # True/False question
            print("1. True")
            print("2. False")
            user_answer = self.get_user_choice(2)

            # Convert user's 1/2 answer to True/False
            user_answer_bool = user_answer == 1
            is_correct = user_answer_bool == question_data["answer"]

            # Display result
            if is_correct:
                print("\n✓ Correct! Well done!\n")
            else:
                correct_text = "True" if question_data["answer"] else "False"
                print(f"\n✗ Incorrect. The correct answer is: {correct_text}\n")
        else:
            # Multiple choice question
            choices = question_data["choices"]
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")

            user_answer = self.get_user_choice(len(choices))
            correct_answer_idx = question_data["answer"] - 1
            is_correct = (user_answer - 1) == correct_answer_idx

            # Display result
            if is_correct:
                print("\n✓ Correct! Well done!\n")
            else:
                correct_text = choices[correct_answer_idx]
                print(
                    f"\n✗ Incorrect. The correct answer is: {question_data['answer']}. {correct_text}\n"
                )

        input("Press Enter to continue...")
        clear_screen()
        return is_correct

    def get_user_choice(self, max_choice):
        """Get and validate user choice."""
        while True:
            try:
                choice = input("\nEnter your answer (number): ")
                choice = int(choice)
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    print(f"Please enter a number between 1 and {max_choice}.")
            except ValueError:
                print("Please enter a valid number.")

    def show_final_score(self):
        """Display the final score."""
        percentage = (self.correct_answers / self.total_questions) * 100
        print(f"=== Quiz Complete: {self.title} ===")
        print(f"You got {self.correct_answers} out of {self.total_questions} correct.")
        print(f"Score: {percentage:.1f}%")

        if percentage >= 90:
            print("Outstanding performance!")
        elif percentage >= 70:
            print("Good job!")
        elif percentage >= 50:
            print("Not bad, keep studying!")
        else:
            print("You might need to review this topic again.")


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def load_quizzes_from_folder(folder_path):
    """
    Load all quiz files from a folder.

    Args:
        folder_path (str): Path to the folder containing quiz files

    Returns:
        list: List of quiz data dictionaries
    """
    quizzes = []

    # Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        except Exception as e:
            print(f"Error creating folder: {str(e)}")
            return quizzes

    # Look for JSON files in the folder
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

        if not files:
            print(f"No quiz files found in {folder_path}. Creating sample quizzes...")
            create_sample_quizzes(folder_path)
            files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

        # Load each quiz file
        for file in files:
            try:
                with open(os.path.join(folder_path, file), "r") as f:
                    quiz_data = json.load(f)
                    if validate_quiz(quiz_data):
                        quizzes.append(quiz_data)
                    else:
                        print(
                            f"Warning: Quiz file '{file}' has invalid format and was skipped."
                        )
            except json.JSONDecodeError:
                print(
                    f"Warning: Quiz file '{file}' contains invalid JSON and was skipped."
                )
            except Exception as e:
                print(f"Warning: Error loading quiz file '{file}': {str(e)}")

    except Exception as e:
        print(f"Error accessing folder: {str(e)}")

    return quizzes


def validate_quiz(quiz_data):
    """
    Validate that quiz data has the required structure.

    Args:
        quiz_data (dict): Quiz data to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(quiz_data, dict):
        return False

    if "title" not in quiz_data or "questions" not in quiz_data:
        return False

    if not isinstance(quiz_data["questions"], list) or not quiz_data["questions"]:
        return False

    for question in quiz_data["questions"]:
        if not isinstance(question, dict):
            return False

        if "question" not in question or "answer" not in question:
            return False

        # Different validation for different question types
        question_type = question.get("type", "multiple_choice")

        if question_type == "true_false":
            # For True/False questions, answer should be a boolean
            if not isinstance(question["answer"], bool):
                return False
        else:
            # For multiple choice questions
            if "choices" not in question:
                return False

            if (
                not isinstance(question["choices"], list)
                or len(question["choices"]) < 2
            ):
                return False

            if (
                not isinstance(question["answer"], int)
                or question["answer"] < 1
                or question["answer"] > len(question["choices"])
            ):
                return False

    return True


def create_sample_quizzes(folder_path):
    """
    Create sample quiz files in the specified folder.

    Args:
        folder_path (str): Path to the folder to create sample quizzes in
    """
    sample_quizzes = [
        {
            "title": "Python Basics",
            "questions": [
                {
                    "question": "What is the correct way to create a function in Python?",
                    "choices": [
                        "function myFunction():",
                        "def myFunction():",
                        "create myFunction():",
                        "func myFunction():",
                    ],
                    "answer": 2,
                    "type": "multiple_choice",
                },
                {
                    "question": "Which of the following is NOT a valid variable name in Python?",
                    "choices": ["my_var", "_count", "2numbers", "camelCase"],
                    "answer": 3,
                    "type": "multiple_choice",
                },
                {
                    "question": "Python is case-sensitive when dealing with identifiers.",
                    "answer": True,
                    "type": "true_false",
                },
            ],
        },
        {
            "title": "World Geography",
            "questions": [
                {
                    "question": "What is the capital of France?",
                    "choices": ["Berlin", "London", "Paris", "Rome"],
                    "answer": 3,
                    "type": "multiple_choice",
                },
                {
                    "question": "The Nile is the longest river in the world.",
                    "answer": True,
                    "type": "true_false",
                },
                {
                    "question": "Australia is both a country and a continent.",
                    "answer": True,
                    "type": "true_false",
                },
            ],
        },
        {
            "title": "Science Quiz",
            "questions": [
                {
                    "question": "Water boils at 100 degrees Celsius at sea level.",
                    "answer": True,
                    "type": "true_false",
                },
                {
                    "question": "Diamonds are made of carbon.",
                    "answer": True,
                    "type": "true_false",
                },
                {
                    "question": "What is the chemical symbol for gold?",
                    "choices": ["Go", "Gd", "Au", "Ag"],
                    "answer": 3,
                    "type": "multiple_choice",
                },
            ],
        },
    ]

    for quiz in sample_quizzes:
        filename = f"{quiz['title'].lower().replace(' ', '_')}.json"
        try:
            with open(os.path.join(folder_path, filename), "w") as f:
                json.dump(quiz, f, indent=4)
            print(f"Created sample quiz: {filename}")
        except Exception as e:
            print(f"Error creating sample quiz {filename}: {str(e)}")


def main():
    # Load quizzes from folder
    quizzes_folder = "quizzes"
    quiz_data = load_quizzes_from_folder(quizzes_folder)

    if not quiz_data:
        print("No valid quiz files found. Please check the 'quizzes' folder.")
        return

    while True:
        clear_screen()
        print("=== QUIZ APPLICATION ===\n")
        print("Available Quiz Topics:")

        # Display available quizzes
        for i, quiz in enumerate(quiz_data, 1):
            print(f"{i}. {quiz['title']}")

        print(f"{len(quiz_data) + 1}. Exit")

        # Get user choice
        choice = 0
        while choice < 1 or choice > len(quiz_data) + 1:
            try:
                choice = int(input("\nSelect a quiz topic (number): "))
                if choice < 1 or choice > len(quiz_data) + 1:
                    print(f"Please enter a number between 1 and {len(quiz_data) + 1}.")
            except ValueError:
                print("Please enter a valid number.")

        if choice == len(quiz_data) + 1:
            clear_screen()
            print("Thank you for using the Quiz Application!")
            break

        # Run the selected quiz
        selected_quiz = quiz_data[choice - 1]
        quiz = Quiz(selected_quiz["title"], selected_quiz["questions"])
        quiz.run_quiz()

        # Ask if user wants to take another quiz
        print("\nWould you like to take another quiz?")
        print("1. Yes")
        print("2. No")

        another = 0
        while another != 1 and another != 2:
            try:
                another = int(input("\nEnter your choice (number): "))
                if another != 1 and another != 2:
                    print("Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")

        if another == 2:
            clear_screen()
            print("Thank you for using the Quiz Application!")
            break


if __name__ == "__main__":
    main()
