def convert_rules():
    """将用户输入的图灵机规则转换为字典格式"""
    rules = {}
    print("请输入你的图灵机指令（输入'end'结束）：")
    
    while True:
        line = input().strip()
        if line.lower() == 'end':
            break
        
        parts = line.split(',')  # 按逗号分割                                                                   
        if len(parts) != 5:
            print(f"无效的规则格式: {line}")
            continue
        
        current_state, read_symbol, write_symbol, direction, new_state = parts
        rule_key = (current_state.strip(), read_symbol.strip())
        rule_value = (write_symbol.strip(), direction.strip(), new_state.strip())
        
        rules[rule_key] = rule_value
    
    return rules

def main():
    rules = convert_rules()
    
    if not rules:
        print("没有加载到有效的规则，程序退出")
        return
    
    # 打印转换后的规则
    print("转换后的规则:")
    rule_list = list(rules.items())
    for i, (rule_key, rule_value) in enumerate(rule_list):
        if i < len(rule_list) - 1:
            print(f"{rule_key}: {rule_value},")
        else:
            print(f"{rule_key}: {rule_value}")

if __name__ == "__main__":
    main()