import os
import time
import json
import random


class Quiz:
    def __init__(self, title, questions, randomize=False):
        """
        Initialize a quiz with a title and list of questions.

        Args:
            title (str): The title/topic of the quiz
            questions (list): List of question dictionaries
            randomize (bool): Whether to randomize the question order
        """
        self.title = title
        self.questions = questions
        self.total_questions = len(questions)
        self.correct_answers = 0
        self.user_answers = []  # Store user answers for reporting

        # Randomize questions if flag is set
        if randomize:
            random.shuffle(self.questions)

    def run_quiz(self):
        """Run the entire quiz and return the final score."""
        clear_screen()
        print(f"=== {self.title} QUIZ ===\n")
        print("Type 'q' as your answer to quit the quiz at any time.\n")

        for idx, question in enumerate(self.questions):
            result = self.present_question(idx + 1, question)
            if result == "q":
                print("\nExiting quiz...\n")
                time.sleep(0.25)
                return None  # User chose to exit
            elif result:  # Answer was correct
                self.correct_answers += 1

        self.show_final_score()
        self.show_quiz_report()
        return self.correct_answers, self.total_questions

    def present_question(self, question_number, question_data):
        """
        Present a single question to the user and handle their response.

        Args:
            question_number (int): The current question number
            question_data (dict): The question data

        Returns:
            bool or str: True if answered correctly, False if incorrect, "q" if user wants to quit
        """
        print(
            f"Question {question_number}/{self.total_questions} - {self.title}")
        print(f"\n{question_data['question']}\n")

        # Handle different question types
        question_type = question_data.get("type", "multiple_choice")
        user_answer_data = {
            "question": question_data["question"], "correct": False}

        if question_type == "true_false":
            # True/False question
            print("1. True")
            print("2. False")
            user_input = input(
                "\nEnter your answer (number or 'q'): ").strip().lower()

            if user_input == "q":
                return "q"

            try:
                user_answer = int(user_input)
                if user_answer < 1 or user_answer > 2:
                    print(f"Please enter a number between 1 and 2.")
                    return self.present_question(question_number, question_data)

                # Convert user's 1/2 answer to True/False
                user_answer_bool = user_answer == 1
                is_correct = user_answer_bool == question_data["answer"]

                # Save user answer for report
                user_answer_data["user_answer"] = (
                    "True" if user_answer_bool else "False"
                )
                user_answer_data["correct_answer"] = (
                    "True" if question_data["answer"] else "False"
                )
                user_answer_data["correct"] = is_correct

                # Display result
                if is_correct:
                    print("\n✓ Correct! Well done!\n")
                else:
                    correct_text = "True" if question_data["answer"] else "False"
                    print(
                        f"\n✗ Incorrect. The correct answer is: {correct_text}\n")
            except ValueError:
                print("Please enter a valid number or 'q'.")
                return self.present_question(question_number, question_data)

        else:
            # Multiple choice question
            choices = question_data["choices"]
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")

            user_input = input(
                "\nEnter your answer (number or 'q'): ").strip().lower()

            if user_input == "q":
                return "q"

            try:
                user_answer = int(user_input)
                if user_answer < 1 or user_answer > len(choices):
                    print(
                        f"Please enter a number between 1 and {len(choices)}.")
                    return self.present_question(question_number, question_data)

                correct_answer_idx = question_data["answer"] - 1
                is_correct = (user_answer - 1) == correct_answer_idx

                # Save user answer for report
                user_answer_data["user_answer"] = choices[user_answer - 1]
                user_answer_data["correct_answer"] = choices[correct_answer_idx]
                user_answer_data["correct"] = is_correct

                # Display result
                if is_correct:
                    print("\n✓ Correct! Well done!\n")
                else:
                    correct_text = choices[correct_answer_idx]
                    print(
                        f"\n✗ Incorrect. The correct answer is: {question_data['answer']}. {correct_text}\n"
                    )
            except ValueError:
                print("Please enter a valid number or 'exit'.")
                return self.present_question(question_number, question_data)

        # Store the answer data for reporting
        self.user_answers.append(user_answer_data)

        input("Press Enter to continue...")
        clear_screen()
        return is_correct

    def show_final_score(self):
        """Display the final score."""
        percentage = (
            (self.correct_answers / self.total_questions) * 100
            if self.total_questions > 0
            else 0
        )
        print(f"=== Quiz Complete: {self.title} ===")
        print(
            f"You got {self.correct_answers} out of {self.total_questions} correct.")
        print(f"Score: {percentage:.1f}%")

        if percentage >= 90:
            print("Outstanding performance!")
        elif percentage >= 70:
            print("Good job!")
        elif percentage >= 50:
            print("Not bad, keep studying!")
        else:
            print("You might need to review this topic again.")

    def show_quiz_report(self):
        """Display a detailed report of the quiz results."""
        print("\n=== QUIZ REPORT ===")
        if not self.user_answers:
            print("No questions were answered.")
            return

        print("Questions you got wrong:\n")
        wrong_answers = [a for a in self.user_answers if not a["correct"]]

        if not wrong_answers:
            print("Congratulations! You got all questions correct!")
        else:
            for i, answer in enumerate(wrong_answers, 1):
                print(f"{i}. {answer['question']}")
                print(f"   Your answer: {answer['user_answer']}")
                print(f"   Correct answer: {answer['correct_answer']}")
                print()


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
            print(f"No quiz files found in {folder_path}.")
            return quizzes

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


def create_combined_quiz(quiz_data_list, randomize=True):
    """
    Create a combined quiz from multiple quizzes.

    Args:
        quiz_data_list (list): List of quiz data dictionaries to combine
        randomize (bool): Whether to randomize the questions

    Returns:
        dict: Combined quiz data
    """
    if not quiz_data_list:
        return None

    # Create combined title from selected quizzes
    titles = [quiz["title"] for quiz in quiz_data_list]
    combined_title = "Combined Quiz: " + ", ".join(titles)

    # Gather all questions
    combined_questions = []
    for quiz in quiz_data_list:
        # Add source quiz info to each question for reporting
        for question in quiz["questions"]:
            question_copy = question.copy()
            question_copy["source_quiz"] = quiz["title"]
            combined_questions.append(question_copy)

    # Randomize if requested
    if randomize:
        random.shuffle(combined_questions)

    return {"title": combined_title, "questions": combined_questions}


def main():
    # Load quizzes from folder
    quizzes_folder = "quizzes"
    quiz_data = load_quizzes_from_folder(quizzes_folder)

    if not quiz_data:
        print("No valid quiz files found. Please check the 'quizzes' folder.")
        input("\nPress Enter to exit...")
        return

    # Sort quizzes alphabetically by title
    quiz_data.sort(key=lambda quiz: quiz["title"])

    while True:
        clear_screen()
        print("=== QUIZ APPLICATION ===\n")
        print("Available Options:")
        print("1. Take individual quiz")
        print("2. Take combined quiz")
        print("3. Exit")

        choice = get_numeric_input("\nSelect an option (number): ", 1, 3)

        if choice == 3:  # Exit
            clear_screen()
            print("Thank you for using the Quiz Application!")
            break

        if choice == 1:  # Take individual quiz
            take_individual_quiz(quiz_data)
        elif choice == 2:  # Take combined quiz
            take_combined_quiz(quiz_data)


def take_individual_quiz(quiz_data):
    """Handle the individual quiz selection and execution."""
    while True:
        clear_screen()
        print("=== INDIVIDUAL QUIZ SELECTION ===\n")
        print("Available Quiz Topics:")

        # Display available quizzes
        for i, quiz in enumerate(quiz_data, 1):
            # Add a space for single-digit numbers
            print(f"{i:2}. {quiz['title']}")

        # Align "Back to main menu"
        print(f"{len(quiz_data) + 1:2}. Back to main menu")

        # Get user choice
        choice = get_numeric_input(
            "\nSelect a quiz topic (number): ", 1, len(quiz_data) + 1
        )

        if choice == len(quiz_data) + 1:
            return  # Back to main menu

        # Ask about randomization
        clear_screen()
        print(f"Selected Quiz: {quiz_data[choice - 1]['title']}")
        randomize = get_yes_no_input(
            "Would you like to randomize the questions? (y/n): "
        )

        # Run the selected quiz
        selected_quiz = quiz_data[choice - 1]
        quiz = Quiz(selected_quiz["title"],
                    selected_quiz["questions"], randomize)
        result = quiz.run_quiz()

        if result is None:  # User exited the quiz
            return  # Go back to main menu

        # Ask if user wants to take another quiz
        another = get_yes_no_input(
            "\nWould you like to take another quiz? (y/n): ")
        if not another:
            return  # Go back to main menu


def take_combined_quiz(quiz_data):
    """Handle the combined quiz selection and execution."""
    if len(quiz_data) < 2:
        clear_screen()
        print("You need at least 2 quizzes to create a combined quiz.")
        input("\nPress Enter to continue...")
        return

    clear_screen()
    print("=== COMBINED QUIZ CREATION ===\n")
    print("Select quizzes to combine (enter the numbers separated by commas):")

    # Display available quizzes
    for i, quiz in enumerate(quiz_data, 1):
        print(f"{i:2}. {quiz['title']} ({len(quiz['questions'])} questions)")

    # Get user selections
    valid_selection = False
    selected_indices = []

    while not valid_selection:
        try:
            selection = input(
                "\nEnter quiz numbers (e.g., 1,3,4) or 'all' for all quizzes: "
            ).strip()

            if selection.lower() == "all":
                selected_indices = list(range(len(quiz_data)))
                valid_selection = True
            else:
                # Parse comma-separated values
                selections = [int(x.strip()) for x in selection.split(",")]

                # Validate all entries
                valid = all(1 <= s <= len(quiz_data) for s in selections)
                if not valid:
                    print(
                        f"Please enter valid numbers between 1 and {len(quiz_data)}.")
                    continue

                # Convert to 0-based indices
                selected_indices = [s - 1 for s in selections]

                if len(selected_indices) < 1:
                    print("Please select at least one quiz.")
                else:
                    valid_selection = True

        except ValueError:
            print("Please enter valid numbers separated by commas.")

    # Create selected quizzes list
    selected_quizzes = [quiz_data[i] for i in selected_indices]

    # Ask about randomization
    randomize = get_yes_no_input(
        "Would you like to randomize the questions? (y/n): ")

    # Create and run the combined quiz
    combined_quiz_data = create_combined_quiz(selected_quizzes, randomize)

    if combined_quiz_data:
        quiz = Quiz(combined_quiz_data["title"],
                    combined_quiz_data["questions"])
        quiz.run_quiz()
    else:
        print("Failed to create combined quiz.")

    input("\nPress Enter to continue...")


def get_numeric_input(prompt, min_val, max_val):
    """Get a numeric input within a range."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(
                    f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")


def get_yes_no_input(prompt):
    """Get a yes/no input and return as boolean."""
    while True:
        response = input(prompt).strip().lower()
        if response == "y" or response == "yes":
            return True
        elif response == "n" or response == "no":
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    main()
