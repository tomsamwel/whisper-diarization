import os
import argparse

def transform_srt_to_text(srt_file_path, output_file_path):
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            lines = srt_file.readlines()

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for i in range(len(lines)):
                if '-->' in lines[i]:
                    time_range = lines[i].strip()
                    speaker_text = ' '.join(lines[i+1:i+3]).strip()
                    formatted_line = f"[{time_range}] {speaker_text}\n"
                    output_file.write(formatted_line)

    except Exception as e:
        print(f"Error occurred while processing file '{srt_file_path}': {e}")

def determine_output_path(input_path, output_arg):
    if output_arg:
        is_directory = os.path.isdir(output_arg) or (not os.path.splitext(output_arg)[1])
        if is_directory:
            # Ensure the output directory exists
            os.makedirs(output_arg, exist_ok=True)
            return lambda file_path: os.path.join(output_arg, os.path.basename(os.path.splitext(file_path)[0] + ".txt"))
        else:
            # Output argument is a file path for single file processing
            return lambda _: output_arg
    else:
        # Output in the same directory as the input file, with .txt extension
        return lambda file_path: os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + ".txt")

def convert_srt_files(input_path, output_path_resolver):
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file_name in files:
                if file_name.endswith('.srt'):
                    srt_file_path = os.path.join(root, file_name)
                    output_file_path = output_path_resolver(srt_file_path)
                    transform_srt_to_text(srt_file_path, output_file_path)
                    print(f"Converted '{srt_file_path}' to '{output_file_path}'.")
    elif os.path.isfile(input_path) and input_path.endswith('.srt'):
        output_file_path = output_path_resolver(input_path)
        transform_srt_to_text(input_path, output_file_path)
        print(f"Converted '{input_path}' to '{output_file_path}'.")
    else:
        print("Input file or directory not found or is not a valid .srt file.")

def main():
    parser = argparse.ArgumentParser(description="Convert SRT files to text files.")
    parser.add_argument('input', help="Input file or directory path")
    parser.add_argument('-o', '--output', help="Optional: Output file or directory path", default=None)
    args = parser.parse_args()

    output_path_resolver = determine_output_path(args.input, args.output)
    convert_srt_files(args.input, output_path_resolver)

if __name__ == "__main__":
    main()
