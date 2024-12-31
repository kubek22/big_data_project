import argparse
import subprocess

def create_hdfs_directory(directory_path):
    try:
        subprocess.run(["hadoop", "fs", "-mkdir", "-p", directory_path], check=True)
        print(f"Directory '{directory_path}' created successfully in HDFS.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create directory '{directory_path}' in HDFS. Error: {e}")
    except FileNotFoundError:
        print("Hadoop command not found. Make sure Hadoop is installed and in your PATH.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a directory in HDFS.")
    parser.add_argument(
        "directory_path",
        type=str,
        help="The HDFS directory path to create."
    )
    
    args = parser.parse_args()
    create_hdfs_directory(args.directory_path)
