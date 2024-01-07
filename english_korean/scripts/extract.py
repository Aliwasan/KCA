import os
import argparse
import re

def extract_content_from_text(txt_folder_path, txt_output_folder):
    os.makedirs(txt_output_folder, exist_ok=True)

    # Regex pour extraire le texte entre les balises <p> à l'intérieur des balises <text>
    pattern_text = re.compile(r'<text\b[^>]*>(.*?)</text>', re.DOTALL)
    pattern_p = re.compile(r'<p.*?>(.*?)</p>', re.DOTALL)
    pattern_s = re.compile(r'<s.*?>(.*?)</s>', re.DOTALL)

    for txt_file in os.listdir(txt_folder_path):
        if txt_file.endswith('.txt'):
            txt_file_path = os.path.join(txt_folder_path, txt_file)

            try:
                with open(txt_file_path, 'r', encoding='utf-8') as file:
                    txt_content = file.read()

                # Utilisation du regex pour extraire le texte entre les balises <text>
                matches_text = pattern_text.findall(txt_content)

                # Si des correspondances sont trouvées, rechercher les balises <p> à l'intérieur de chaque balise <text>
                if matches_text:
                    txt_output_file_path = os.path.join(txt_output_folder, os.path.splitext(txt_file)[0] + '_content.txt')
                    with open(txt_output_file_path, 'a', encoding='utf-8') as txt_output_file:
                        for match_text in matches_text:
                            matches_p = pattern_p.findall(match_text)
                            for match_p in matches_p:
                                # Rechercher les balises <s> à l'intérieur de chaque balise <p>
                                matches_s = pattern_s.findall(match_p)
                                for match_s in matches_s:
                                    txt_output_file.write(match_s.strip() + '\n')

                    print(f"Processed file: {txt_file}")
                    print(f"Extracted content from <s> tags within <p>: {matches_s}")

            except Exception as e:
                print(f"Error processing file {txt_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract content from text files within <p> tags within <text>.')
    parser.add_argument('txt_folder_path', help='Path to the folder containing text files')
    parser.add_argument('txt_output_folder', help='Path to the folder where output text files will be saved')

    args = parser.parse_args()

    extract_content_from_text(args.txt_folder_path, args.txt_output_folder)
