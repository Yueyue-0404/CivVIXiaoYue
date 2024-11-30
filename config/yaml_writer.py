"""
这是个yaml写入器
"""
import yaml

command_dict = {
    # 6:"bug",
    # 5:"ab",
    # 4:"ub",
    # 2:"ud",
    # 3:"ui",
    1: ["领袖","文明"]
}

with open('command_target_types.yaml', 'w') as f:
    yaml.dump(command_dict, f)
