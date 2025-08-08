import json
import ijson

def process_large_json(input_file, output_file):
    converted = []
    current_scene = {"background": "", "dialogues": []}
    row_count = 0
    current_body = None
    
    with open(input_file, "r", encoding="utf-8") as f:
        rows = ijson.items(f, "importGridList.item.rows.item")
        
        for row in rows:
            row_count += 1
            if row_count % 10000 == 0:
                print(f"已处理 {row_count} 行...")
            
            if row.get("isCommentOut") or row.get("isEmpty"):
                continue
                
            strings = row["strings"]
            command = strings[0] if len(strings) > 0 else ""
            arg1 = strings[1] if len(strings) > 1 else ""
            arg2 = strings[2] if len(strings) > 2 else ""
            
            # 1. 首先处理背景命令
            if command in ["Bg", "BgEvent"] and arg1:
                current_body = None
                if current_scene["dialogues"]:
                    converted.append(current_scene)
                    current_scene = {"background": arg1, "dialogues": []}
                else:
                    current_scene["background"] = arg1
            
            # 2. 修正对话行判断：增加中文文本存在性检查
            elif command == "" and len(strings) > 12 and strings[12].strip():
                chinese_text = strings[12].strip()
                character = "" if arg1 == "<Off>" else arg1
                
                dialogue = {
                    "character": character, 
                    "text": chinese_text
                }
                
                if current_body:
                    dialogue["body"] = current_body
                
                current_scene["dialogues"].append(dialogue)
            
            # 3. 最后处理特殊行：增加额外限制条件
            elif (
                command == "" 
                and arg2 != "" 
                and len(strings) > 2 
                and arg2 != "<Off>"
                # 新增条件：确保不是对话行（中文文本列不存在或为空）
                and (len(strings) <= 12 or not strings[12].strip())
            ):
                current_body = arg1
    
    # 添加最后一个场景
    if current_scene["dialogues"] or current_scene["background"]:
        converted.append(current_scene)
    
    # 保存结果
    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(converted, out_f, ensure_ascii=False, indent=2)
    
    print(f"转换完成！共处理 {row_count} 行，生成 {len(converted)} 个场景")

# 使用示例
process_large_json("hoshishiro_01.book.json", "转换后的剧本.json")