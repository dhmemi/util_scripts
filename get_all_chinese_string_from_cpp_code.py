import os

# get all file path from given directory
def get_all_file_path(dir_path):
    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path_list.append(os.path.join(root, file))
    return file_path_list

# if file extension is .h, .hpp, .cpp or .c, return True
def if_cpp_file(file_path):
    if file_path.endswith('.h') or file_path.endswith('.hpp') or file_path.endswith('.cpp') or file_path.endswith('.c'):
        return True
    else:
        return False

# guess encoding of the file.
def guess_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'utf-16le', 'utf-16be']
    for encoding in encodings:
        try:
            raw.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    return None

# check if string contans chinese.
def if_contains_chinese(string):
    for ch in string:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

# filter all chinese string from string list
def filter_chinese_string(string_list):
    chinese_string_list = []
    for string in string_list:
        if if_contains_chinese(string):
            chinese_string_list.append(string)
    return chinese_string_list


# get all sub string in double quotes from string.
def get_all_sub_string_in_double_quotes(string):
    sub_string_list = []
    start_index = 0
    while True:
        start_index = string.find('"', start_index+1)
        if start_index == -1:
            break
        end_index = string.find('"', start_index + 1)
        if end_index == -1:
            break
        sub_string = string[start_index + 1:end_index]
        sub_string_list.append(sub_string)
        start_index = end_index
    return sub_string_list

# get all string which contains chinese from file. return string, line number of each string and file path.
def get_all_chinese_string_from_file(file_path):
    chinese_string_list = []
    encoding = guess_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as f:
        line_number = 0
        for line in f:
            line_number += 1
            sub_string_list = get_all_sub_string_in_double_quotes(line)
            sub_string_list = filter_chinese_string(sub_string_list)
            for sub_string in sub_string_list:
                chinese_string_list.append((sub_string, line_number, file_path))
    return chinese_string_list


if __name__ == '__main__':
    file_path_list = get_all_file_path("./")
    chinese_string_list = []
    for file_path in file_path_list:
        if if_cpp_file(file_path):
            chinese_string_list += get_all_chinese_string_from_file(file_path)
    # write all chinese string and information into an po translation file.
    with open('chinese_string.po', 'w') as f:
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version:\\n"\n')
        f.write('"POT-Creation-Date: 2017-07-25 15:52+0800\\n"\n')
        f.write('"PO-Revision-Date: 2017-07-25 15:52+0800\\n"\n')
        f.write('"Last-Translator: \\n"\n')
        f.write('"Language-Team: \\n"\n')
        f.write('"MIME-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('"Plural-Forms: nplurals=1; plural=0;\\n"\n')
        for chinese_string in chinese_string_list:
            f.write('msgid "' + chinese_string[0] + '"\n')
            f.write('msgstr ""\n\n')
            f.write('#: ' + chinese_string[2] + ':' + str(chinese_string[1]) + '\n')

    # write all chinese string and information into an csv file.
    with open('chinese_string.csv', 'w') as f:
        f.write('string, line number, file path\n')
        for chinese_string in chinese_string_list:
            f.write('"' + chinese_string[0] + '", ' + str(chinese_string[1]) + ', "' + chinese_string[2] + '"\n')
