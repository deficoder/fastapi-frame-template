import re, os

def format_file_size(fsize):
    Kb = 1000
    Mb, Gb = Kb * Kb, Kb * Kb * Kb

    if fsize < Mb:
        return '%.2f' % (fsize / Kb) + ' Kb'
    elif fsize >= Mb and fsize < Gb:
        return '%.2f' % (fsize / Mb) + ' Mb'
    else:
        return '%.2f' % (fsize / Gb) + ' Gb'

def vtt_to_txt(path):
    texts = []
    with open(path) as f:
        for line in f.readlines():
            # 00:00:02.000 --> 00:00:08.720
            s = re.search(r'[0-9]{2}:[0-5][0-9]:[0-5][0-9].[0-9]{3} --> [0-9]{2}:', line)
            if s:
                continue

            texts.append(line)
        f.close()

    with open('new.txt', 'w') as f:
        f.writelines(texts)
        f.close()

# vtt_to_txt('/root/workspace/Vocabulary_Grammar_Pronunciation.vtt')