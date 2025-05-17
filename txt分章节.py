import re
import os

def split_novel_chapters(input_file, output_dir="chapters"):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 匹配章节标题的正则表达式（支持中文数字、阿拉伯数字和空格）
    chapter_pattern = re.compile(
        r'^\s*第[ \t]*([一二三四五六七八九十零百千万0-9]+|[\d]+)[ \t]*章[ \t]*(.*?)\s*$'
    )

    current_chapter = None
    chapter_content = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = chapter_pattern.match(line)
            if match:
                if current_chapter is not None:
                    # 保存前一章
                    save_chapter(current_chapter, chapter_content, output_dir)
                
                # 开始新章节
                chapter_number = match.group(1)
                chapter_title = match.group(2).strip()
                current_chapter = f"第{chapter_number}章 {chapter_title}"
                chapter_content = [line]  # 包含标题行
            else:
                if current_chapter is not None:
                    chapter_content.append(line)

        # 保存最后一章
        if current_chapter is not None:
            save_chapter(current_chapter, chapter_content, output_dir)

def save_chapter(chapter_title, content, output_dir):
    # 清理文件名中的非法字符
    safe_title = re.sub(r'[\\/*?:"<>|]', '', chapter_title)
    file_path = os.path.join(output_dir, f"{safe_title}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f'已保存章节: {safe_title}')

if __name__ == "__main__":
    # 使用示例
    input_path = "all.txt"  # 输入文件路径
    split_novel_chapters(input_path)