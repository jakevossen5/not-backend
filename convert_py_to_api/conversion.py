from typing import List
import sys


def main() -> None:
    input_file: str = str(sys.argv[1])
    output_file: str = str(sys.argv[2])

    output_lines: List[str] = []

    output_lines.append("from flask import Flask")
    output_lines.append("app = Flask(__name__)")

    with open(input_file) as f:
        input_file_lines = f.readlines()

    for line in input_file_lines:
        # dealing with a function, we need to add a flask decorator
        if line.startswith('def'):
            decorator: str = get_flask_decorator(line)
            output_lines.append(decorator)
        output_lines.append(line)

    output_lines.append("if __name__ == '__main__':")
    output_lines.append("    app.run(debug=True, host='0.0.0.0')")

    print("printing output lines")
    output_file = open(output_file, 'w')
    for line in output_lines:
        output_file.write(line + '\n' if len(line) > 0 else '')


def get_flask_decorator(line: str):
    # should probably do this with a regex but hackathon am i right
    func_name = line.split('(')[0].split(' ')[1]
    return "@app.route('/" + func_name + "')"


main()
