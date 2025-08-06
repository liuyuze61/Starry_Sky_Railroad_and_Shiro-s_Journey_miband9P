import json
import os

def split_script_by_lines(input_file, output_dir, lines_per_chunk=2000):
    """按行数分割剧本，确保在场景结束时分割"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取整个剧本
    with open(input_file, 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    # 初始化变量
    current_chunk = []
    current_line_count = 0
    chunk_index = 1
    scene_index = 0
    
    # 遍历所有场景
    while scene_index < len(script_data):
        scene = script_data[scene_index]
        
        # 序列化当前场景以计算行数
        scene_json = json.dumps([scene], ensure_ascii=False, indent=2)
        scene_lines = scene_json.count('\n') + 1  # 计算行数
        
        # 检查添加当前场景是否会超过限制
        if current_line_count + scene_lines > lines_per_chunk and current_chunk:
            # 保存当前块
            save_chunk(current_chunk, output_dir, chunk_index)
            chunk_index += 1
            current_chunk = []
            current_line_count = 0
        else:
            # 添加场景到当前块
            current_chunk.append(scene)
            current_line_count += scene_lines
            scene_index += 1
    
    # 保存最后一个块
    if current_chunk:
        save_chunk(current_chunk, output_dir, chunk_index)

def save_chunk(chunk_data, output_dir, chunk_index):
    """保存剧本块到文件"""
    output_file = os.path.join(output_dir, f"{chunk_index}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_data, f, ensure_ascii=False, indent=2)
    print(f"已保存章节 {chunk_index}: {len(chunk_data)} 个场景")

def main():
    # 配置参数
    input_script = "映射后的剧本.json"
    output_directory = "分割后的章节"
    
    # 分割剧本
    split_script_by_lines(input_script, output_directory)
    print("剧本分割完成!")

if __name__ == "__main__":
    main()