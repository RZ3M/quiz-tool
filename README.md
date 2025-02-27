# Quiz Tool

A command-line quiz application built in Python that lets users take various topic-based quizzes with multiple-choice and true/false questions.

## Features

- Dynamic quiz loading from JSON files
- Support for multiple quiz topics
- Multiple choice and true/false questions
- Score tracking and performance feedback
- Clear terminal interface
- Quiz progress tracking
- Input validation

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/quiz-tool.git
```

2. Navigate to the project directory:

```bash
cd quiz-tool
```

### Usage

1. Run the application:

```bash
python quiz.py
```

2. Select a quiz topic from the available options
3. Answer each question by entering the corresponding number
4. View your results at the end of the quiz

## Quiz File Structure

Quizzes are stored as JSON files in the quizzes directory. Each quiz file must follow this format:

```json
{
  "title": "Quiz Title",
  "questions": [
    {
      "question": "Question text",
      "type": "multiple_choice",
      "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
      "answer": 1
    },
    {
      "question": "True/False question text",
      "type": "true_false",
      "answer": true
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
