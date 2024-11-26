import os
import subprocess

def convert_rtf_to_txt(rtf_file, txt_file):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'txt:Text', rtf_file, '--outdir', os.path.dirname(txt_file)])
        print(f"Converted {rtf_file} to {txt_file}")
    except Exception as e:
        print(f"Failed to convert {rtf_file}: {e}")

def convert_all_rtf_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".rtf"):
            rtf_path = os.path.join(directory, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(directory, txt_filename)
            convert_rtf_to_txt(rtf_path, txt_path) 

if __name__ == "__main__":
    convert_all_rtf_in_directory("/om/user/arjunp/goldTranscripts")