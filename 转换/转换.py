import json
import ijson

def process_large_json(input_file, output_file):
    converted = []
    current_scene = {"background": "", "dialogues": []}
    row_count = 0
    current_body = None  # 存储当前body内容
    
    with open(input_file, "r", encoding="utf-8") as f:
        # 解析到rows数组
        rows = ijson.items(f, "importGridList.item.rows.item")
        
        for row in rows:
            row_count += 1
            if row_count % 10000 == 0:
                print(f"已处理 {row_count} 行...")
            
            # 跳过注释行和空行
            if row.get("isCommentOut") or row.get("isEmpty"):
                continue
                
            strings = row["strings"]
            command = strings[0] if len(strings) > 0 else ""
            arg1 = strings[1] if len(strings) > 1 else ""
            arg2 = strings[2] if len(strings) > 2 else ""
            
            # 1. 检查是否是特殊行：索引0为空，索引2不为空
            if command == "" and arg2 != "" and len(strings) > 2 and arg2 != "<Off>":
                current_body = arg1  # 设置新的body内容
                continue
            
            # 2. 处理背景命令
            if command in ["Bg", "BgEvent"] and arg1:
                # 背景切换时重置body
                current_body = None
                
                # 如果当前场景已有对话，保存并开始新场景
                if current_scene["dialogues"]:
                    converted.append(current_scene)
                    current_scene = {"background": arg1, "dialogues": []}
                else:
                    current_scene["background"] = arg1
            
            # 3. 处理对话行
            elif command == "" and len(strings) > 12:
                chinese_text = strings[12].strip()
                if chinese_text:
                    character = "" if arg1 == "<Off>" else arg1
                    
                    # 创建对话对象
                    dialogue = {
                        "character": character, 
                        "text": chinese_text
                    }
                    
                    # 如果有当前body内容，添加到对话
                    if current_body:
                        dialogue["body"] = current_body
                    
                    current_scene["dialogues"].append(dialogue)
    
    # 添加最后一个场景
    if current_scene["dialogues"] or current_scene["background"]:
        converted.append(current_scene)
    
    # 保存结果
    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(converted, out_f, ensure_ascii=False, indent=2)
    
    print(f"转换完成！共处理 {row_count} 行，生成 {len(converted)} 个场景")

# 使用示例
process_large_json("hoshishiro_01.book.json", "转换后的剧本.json")