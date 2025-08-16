from audio_question_gui import QuestionGUI
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Audio Question GUI application')
    parser.add_argument('-q', '--questions', required=True, help='Path to file containing questions')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory to store output audio files')
    args = parser.parse_args()

    # Read questions from file
    if not os.path.isfile(args.questions):
        print(f"Questions file {args.questions} not found.")
        return

    with open(args.questions, 'r') as f:
        questions = [line.strip() for line in f if line.strip()]

    # Check or create output directory
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    app = QuestionGUI(questions, args.output_dir)
    app.mainloop()


if __name__ == '__main__':
    main()
