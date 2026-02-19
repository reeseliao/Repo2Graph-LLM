import os
import argparse
import ollama
from tqdm import tqdm
import time

# --- 核心配置 ---
MODEL_NAME = "gemma2" 
IGNORE_DIRS = {'.git', 'build', 'out', 'bin', 'test', 'tests', 'samples', '3rdparty', 'doc', 'cmake', '.vs'} 
EXTENSIONS = {'.hpp', '.cpp', '.h', '.c', '.cc'}

def get_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if os.path.splitext(file)[1] in EXTENSIONS:
                file_list.append(os.path.join(root, file))
    return file_list

def generate_prompt(file_name, code_content):
    return f"""
Target File: `{file_name}`

Analyze this C++ file from OpenCV. Output a strictly formatted Markdown note.

Rules:
1. **NO INTRO/OUTRO:** Start directly with the header.
2. **LINKING:** Wrap key classes in brackets: [[Mat]], [[Point]].
3. **CONCISE:** Be extremely brief.

Output Format:
# {file_name}

## Summary
(1 sentence explanation)

## Key Components
* **[[ClassName]]**: (What it does)
* **Function()**: (Brief logic)

## Logic & Dependencies
(Explain interactions using [[Links]])

---
Code snippet:
{code_content[:4000]}
"""

def analyze_file(file_path, output_dir):
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if len(content) < 50: return 

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': generate_prompt(file_name, content)}],
            options={'temperature': 0.0} 
        )
        
        md_content = response['message']['content']
        final_md = f"---\ntags: [opencv, gemma2]\n---\n\n" + md_content
        
        output_file = os.path.join(output_dir, file_name + ".md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_md)
            
    except Exception as e:
        print(f"Skipped {file_name}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", help="OpenCV 源码文件夹路径")
    parser.add_argument("--out", default="./opencv_wiki", help="输出结果的文件夹")
    args = parser.parse_args()
    
    if not os.path.exists(args.out):
        os.makedirs(args.out)
    
    print(f"🔍 扫描路径: {args.source_path}")
    files = get_files(args.source_path)
    print(f"📂 找到 {len(files)} 个文件。准备分析...")
    
    for file in tqdm(files, desc="Processing"):
        analyze_file(file, args.out)

if __name__ == "__main__":
    main()