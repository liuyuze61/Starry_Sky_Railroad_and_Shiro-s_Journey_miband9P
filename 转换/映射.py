import json
import os

def load_mapping(mapping_file):
    """加载映射表数据"""
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    
    # 角色名映射 {日文: 中文}
    char_map = {}
    for item in mapping_data.get("character", []):
        if not item.get("isCommentOut") and not item.get("isEmpty") and len(item["strings"]) >= 3:
            jp_name = item["strings"][0]
            cn_name = item["strings"][2]  # 第3列是中文名
            char_map[jp_name] = cn_name
    
    # 背景映射 {背景名: 文件名}
    bg_map = {}
    for item in mapping_data.get("cg", []):
        if not item.get("isCommentOut") and not item.get("isEmpty") and len(item["strings"]) >= 9:
            bg_name = item["strings"][0]
            file_name = item["strings"][8]  # 第9列是文件名
            bg_map[bg_name] = file_name
    
    # body映射 {body键: 文件名}
    body_map = {}
    for item in mapping_data.get("body", []):
        if not item.get("isCommentOut") and not item.get("isEmpty") and len(item["strings"]) >= 10:
            body_key = item["strings"][0]
            file_name = item["strings"][9]  # 第10列是文件名
            body_map[body_key] = file_name
    
    return char_map, bg_map, body_map

def apply_mappings(script_file, char_map, bg_map, body_map):
    """应用映射到剧本文件"""
    with open(script_file, 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    # 处理每个场景
    for scene in script_data:
        # 1. 映射背景
        bg_name = scene.get("background", "")
        if bg_name in bg_map:
            scene["background"] = bg_map[bg_name]
        
        # 2. 处理每个对话
        for dialogue in scene.get("dialogues", []):
            # 映射角色名
            char_name = dialogue.get("character", "")
            if char_name in char_map:
                dialogue["character"] = char_map[char_name]
            
            # 映射body
            if "body" in dialogue:
                body_key = dialogue["body"]
                if body_key in body_map:
                    dialogue["body"] = body_map[body_key]
    
    return script_data

def main():
    # 文件路径配置
    mapping_file = "映射表.json"
    input_script = "转换后的剧本.json"
    output_script = "映射后的剧本.json"
    
    # 加载映射表
    char_map, bg_map, body_map = load_mapping(mapping_file)
    
    # 应用映射
    mapped_script = apply_mappings(input_script, char_map, bg_map, body_map)
    
    # 保存结果
    with open(output_script, 'w', encoding='utf-8') as f:
        json.dump(mapped_script, f, ensure_ascii=False, indent=2)
    
    print(f"映射完成! 结果已保存到 {output_script}")

if __name__ == "__main__":
    main()