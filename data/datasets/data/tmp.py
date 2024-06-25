import os

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    processed_lines = []
    for line in lines:
        if line.startswith('1'):
            continue  # 跳过删除的行
        elif line.startswith('2'):
            continue
        elif line.startswith('3'):
            #line = '1' + line[1:]  # 将行首4改为2
            continue
        elif line.startswith('4'):
            #line = '1' + line[1:]  # 将行首4改为2
            continue
        processed_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            process_file(file_path)
            print(f"Processed file: {file_path}")

if __name__ == "__main__":
    directory_path = 'D:\\aimbot\data\datasets\data\overwatch.v2i.yolov8_without_friend\\test\labels'  # 修改为你的目标文件夹路径
    process_directory(directory_path)
