class TuringMachine:
    def __init__(self, initial_string, rules):
        self.tape_size = 100
        self.tape = self.initialize_tape(initial_string)  # 初始化纸带
        self.rules = rules  # 图灵机的规则
        self.state = 'q0'  # 初始状态
        self.head_position = 0  # 纸带头的初始位置
        self.blank_symbol = 'B'  # 空白符号
    
    def upd(self, initial_string):
        self.state = 'q0'
        self.head_position = 0
        for i in range(self.tape_size):
            if i < len(initial_string):
                self.tape[i] = initial_string[i]
            else:
                self.tape[i] = 'B'
        return

    def initialize_tape(self, initial_string):
        """初始化纸带 使用初始字符串填充从位置0开始的部分"""
        # 创建一个足够大的列表来模拟纸带，初始值为'B'
        tape = ['B'] * self.tape_size
        
        # 使用初始字符串填充从位置0开始的部分
        for i in range(len(initial_string)):
            tape[i] = initial_string[i]
        return tape
    
    def run(self):
        """运行图灵机直到达到停机状态(qa)"""
        while self.state != 'qa':
            # 读取当前纸带位置的符号
            current_symbol = self.tape[self.head_position]
            
            # 查找对应的规则
            rule_key = (self.state, current_symbol)
            if rule_key not in self.rules:
                print(f"没有找到规则: {rule_key}，图灵机停止")
                break

            rule = self.rules[rule_key]
            write_symbol, move_direction, new_state = rule
            
            # 执行规则
            self.tape[self.head_position] = write_symbol  # 写入符号
            self.state = new_state  # 更新状态
            
            # 移动纸带头
            if move_direction == 'R':
                self.head_position += 1
                self.head_position %= self.tape_size
            elif move_direction == 'L':
                self.head_position -= 1
                if self.head_position < 0:
                    self.head_position += self.tape_size
            else:
                print(f"未知的移动方向: {move_direction}")
                break
        if self.state == 'qa':
            return self.display_tape()
        print("图灵机已停机")
    
    def cal(self, s):
        if len(s) == 0 or (len(s) > 1 and s[0] != '1'):
            return -3
        sum_val = 0
        for i in s:
            if i == '0':
                sum_val = sum_val * 2
            elif i == '1':
                sum_val = sum_val * 2 + 1
            else:
                return -1
        return sum_val
    
    def display_tape(self):
        """显示当前纸带状态"""
        flag = False
        result = ""
        for i in range(self.tape_size):
            symbol = self.tape[i]
            if flag == False and symbol == '=':
                flag = True
            elif flag and symbol == 'B':
                break
            elif flag:
                result += symbol
        if flag:
            return self.cal(result)
        else:
            return -2

def dec_to_bin(x):
    if x == 0:
        return '0'
    s = ''
    while x:
        if x & 1 == 1:
            s = '1' + s
        else:
            s = '0' + s
        x >>= 1
    return s

def bin_to_dec(s):
    return int(s, 2)

def main():
    # 定义图灵机规则
    rules = {
        ('q0', '0'): ('0', 'R', 'q0'),
        ('q0', '1'): ('1', 'R', 'q0'),
        ('q0', '+'): ('+', 'L', 'check0'),
        ('q0', '#'): ('#', 'L', 'check0'),
        ('check0', '0'): ('#', 'R', 'p0'),
        ('check0', '1'): ('#', 'R', 'pp0'),
        ('check0', 'B'): ('B', 'R', 'check0'),
        ('check0', '#'): ('#', 'R', 'check1'),
        ('p0', '+'): ('+', 'R', 'p0'),
        ('p0', '1'): ('1', 'R', 'p0'),
        ('p0', '0'): ('0', 'R', 'p0'),
        ('p0', '='): ('=', 'L', 'tr0'),
        ('p0', 'F'): ('F', 'L', 'tr0'),
        ('p0', 'T'): ('T', 'L', 'tr0'),
        ('p0', '#'): ('#', 'R', 'p0'),
        ('tr0', '0'): ('F', 'L', 'bp'),
        ('tr0', '1'): ('T', 'L', 'bp'),
        ('tr0', '#'): ('F', 'L', 'bp'),
        ('bp', '+'): ('0', 'L', 'bp'),
        ('bp', '1'): ('1', 'L', 'bp'),
        ('bp', '0'): ('0', 'L', 'bp'),
        ('bp', '#'): ('#', 'L', 'bp'),
        ('bp', 'B'): ('B', 'R', 'q0'),
        ('pp0', '0'): ('0', 'R', 'pp0'),
        ('pp0', '1'): ('1', 'R', 'pp0'),
        ('pp0', '#'): ('#', 'R', 'pp0'),
        ('pp0', '+'): ('+', 'R', 'pp0'),
        ('pp0', 'F'): ('F', 'L', 'tr1'),
        ('pp0', 'T'): ('T', 'L', 'tr1'),
        ('pp0', '='): ('=', 'L', 'tr1'),
        ('tr1', '1'): ('F', 'L', 'bpp'),
        ('tr1', '0'): ('T', 'L', 'bp'),
        ('tr1', '#'): ('T', 'L', 'bp'),
        ('bpp', '0'): ('1', 'L', 'bp'),
        ('bpp', '1'): ('0', 'L', 'bpp'),
        ('bpp', '+'): ('1', 'L', 'bp'),
        ('bpp', '#'): ('1', 'L', 'bp'),
        ('check1', '#'): ('#', 'R', 'check1'),
        ('check1', '0'): ('#', 'L', 'check1'),
        ('check1', '1'): ('A', 'R', 'move1'),
        ('check1', 'T'): ('A', 'R', 'move1'),
        ('check1', 'F'): ('A', 'R', 'move2'),
        ('move1', 'T'): ('T', 'R', 'move1'),
        ('move1', 'F'): ('F', 'R', 'move1'),
        ('move1', '='): ('=', 'R', 'move1'),
        ('move1', '1'): ('1', 'R', 'move1'),
        ('move1', '0'): ('0', 'R', 'move1'),
        ('move1', 'B'): ('1', 'L', 'back'),
        ('back', '='): ('=', 'L', 'back'),
        ('back', 'T'): ('T', 'L', 'back'),
        ('back', 'F'): ('F', 'L', 'back'),
        ('back', '1'): ('1', 'L', 'back'),
        ('back', '0'): ('0', 'L', 'back'),
        ('back', 'A'): ('A', 'R', 'check3'),
        ('check3', 'T'): ('A', 'R', 'move1'),
        ('check3', 'F'): ('A', 'R', 'move2'),
        ('check3', '0'): ('A', 'R', 'move2'),
        ('check3', '1'): ('A', 'R', 'move1'),
        ('check3', '='): ('=', 'R', 'qa'),
        ('move2', 'T'): ('T', 'R', 'move2'),
        ('move2', 'F'): ('F', 'R', 'move2'),
        ('move2', '1'): ('1', 'R', 'move2'),
        ('move2', '0'): ('0', 'R', 'move2'),
        ('move2', '='): ('=', 'R', 'move2'),
        ('move2', 'B'): ('1', 'L', 'back'),
    }

    tm = TuringMachine("0+0=", rules)
    
    # 验证图灵机的正确性
    for i in range(0, 256):
        for t in range(0, 256):
            initial_string = dec_to_bin(i) + '+' + dec_to_bin(t) + '='
            print(initial_string, end='')
            
            tm.upd(initial_string)
            result = tm.run()
            
            if result != i + t:
                print('Wrong!!!!!', initial_string, result, i + t)
                return False
            else:
                print(result)
    
    return True

if __name__ == "__main__":
    if main():
        print("alright")
    else:
        print("some wrong")