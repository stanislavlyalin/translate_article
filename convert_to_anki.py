from tqdm import tqdm

if __name__ == '__main__':

    unknown_filepath = 'unknown.txt'
    with open(unknown_filepath, encoding='utf-8') as f:
        content = f.readlines()

    file_name = 'anki.txt'
    with open(file_name, encoding='utf-8', mode='w') as f:
        for line in tqdm(content):
            word, translation, transcription = line.split(';')
            f.write(f'{word};{translation}<br>{transcription}\n')

    print(f'Convert finished. Result writed to {file_name}')
