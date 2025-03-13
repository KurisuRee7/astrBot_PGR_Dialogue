import requests
from bs4 import BeautifulSoup
import os
url = "https://wiki.biligame.com/zspms/%E8%96%87%E6%8B%89%C2%B7%E7%BB%AF%E8%80%80"
def get_page_text(url):
    try:
        # 发送 HTTP 请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 使用 BeautifulSoup 解析 HTML 并提取文本
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取所有文本内容
        text = soup.get_text()

        return text

    except Exception as e:
        print(f"获取网页内容时出错: {e}")
        return None

# 使用示例
page_text = get_page_text(url)

def save_to_txt(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"内容已成功保存到 {filename}")
    except Exception as e:
        print(f"保存内容时出错: {e}")


if page_text:
    save_to_txt(page_text, "tmp_page_content.txt")

def get_first_non_empty_line(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 去除行首尾的空白字符
                stripped_line = line.strip()
                if stripped_line:  # 如果去除空白字符后不为空
                    return stripped_line
        return None  # 如果文件中没有非空行，返回 None

    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None
name = get_first_non_empty_line("tmp_page_content.txt")


def extract_content_between_lines(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 初始化变量
        count_zhong = 0
        start_index = -1
        end_index = -1

        # 遍历行，找到符合条件的起始行和结束行
        for i, line in enumerate(lines):
            # 去除行首尾的空白字符
            stripped_line = line.strip()

            # 条件1：找到第二行仅包含“中”的行
            if stripped_line == "中":
                count_zhong += 1
                if count_zhong == 1:
                    start_index = i

            # 条件2：从第二行“中”开始，找到第一行仅包含“日”的行
            if start_index != -1 and stripped_line == "日":
                end_index = i
                break

        # 检查是否找到符合条件的行
        if start_index == -1 or end_index == -1:
            print("未找到符合条件的行")
            return

        # 提取两行之间的内容
        content_between = lines[start_index:end_index]

        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(content_between)

        print(f"提取的内容已保存到 {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

# 使用示例
input_file = "tmp_page_content.txt"  # 输入文件名
output_file = "tmp_txt.txt"  # 输出文件名
extract_content_between_lines(input_file, output_file)

def extract_and_filter_content(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 初始化变量
        start_line = None
        end_line = None

        # 查找起始行和结束行的索引
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line == "日常问候1":
                start_line = i
            if stripped_line == "助战":
                end_line = i

        if start_line is None or end_line is None:
            print("未找到起始行或结束行")
            return

        # 提取两行之间的内容
        content_between = lines[start_line:end_line + 1]

        # 删除空白行
        filtered_content = [line for line in content_between if line.strip()]

        # 删除奇数行（索引从0开始）
        final_content = [filtered_content[i] for i in range(len(filtered_content)) if (i % 2 != 0)]

        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(final_content)

        print(f"提取并过滤后的内容已保存到 {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

# 使用示例
input_file = "tmp_txt.txt"  # 输入文件名
output_file = "tmp_yuyin.txt"  # 输出文件名
extract_and_filter_content(input_file, output_file)

def format_lines(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 格式化每一行
        formatted_lines = ['"{0}",\n'.format(line.strip()) for line in lines]

        # 保存到输出文件
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(formatted_lines)

        print(f"格式化后的内容已保存到 {output_file}")

    except Exception as e:
        print(f"处理文件时出错: {e}")

# 使用示例
input_file = "tmp_yuyin.txt"  # 输入文件名
output_file = name + ".txt"  # 输出文件名
format_lines(input_file, output_file)