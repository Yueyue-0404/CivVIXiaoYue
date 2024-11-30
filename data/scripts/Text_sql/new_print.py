def new_print(text, *, font_style="", color="", background_color="",end="\n"):
    """
    new_print仍然是print的功能，但额外集合了样式功能
    只提供你要打印的对象则效果和print完全一致
    你可以选择性输入3个命名形参：
    ===============================
    一、font_style 传入字体样式
        1. 加粗：BOLD
        2. 斜体：ITALIC
        3. 下划线：UNDER_LINE
        4. 隐藏：HIDDEN
    ※ font_style 支持多样式混合，例：传入 font_style=BOLD+ITALIC 将实现加粗+斜体
    ===============================
    二、color 和 background_color 传入颜色代码
        1. 黑色：BLACK
        2. 红色：RED
        3. 绿色：GREEN
        4. 黄色：YELLOW
        5. 蓝色：BLUE
        6. 洋红色：MAGENTA
        7. 青色：CYAN
        8. 白色：WHITE
        9. 浅灰色：LIGHT_GRAY
        10. 亮红色：BRIGHT_RED
        11. 亮绿色：BRIGHT_GREEN
        12. 亮黄色：BRIGHT_YELLOW
        13. 亮蓝色：BRIGHT_BLUE
        14. 亮洋红色：BRIGHT_MAGENTA
        15. 亮青色：BRIGHT_CYAN
        16. 亮白色：BRIGHT_WHITE
    ===============================
    """
    text = str(text)
    if font_style:
        font_style = ";".join(list(font_style))
    if color:
        color = str(int(color) + 30)
    if background_color:
        background_color = str(int(background_color) + 40)

    ANSI_start_code = "\033[{}m".format(
        ";".join([i for i in [font_style, color, background_color] if i])
    )
    ANSI_end_code = "\033[0m"

    print("{}{}{}".format(ANSI_start_code, text, ANSI_end_code),end=end)


# def help():
#     print("="*45)
#     print("new_print是个集合了样式功能的打印函数")
#     print("想使用样式，除了提供你要打印的对象以外，还可以选择性输入3个命名形参：")
#     print("一、font_style传入字体样式")
#     print("\t1. 加粗：BOLD")
#     print("\t2. 斜体：ITALIC")
#     print("\t3. 下划线：UNDER_LINE")
#     print("\t4. 隐藏：HIDDEN")
#     print("二、color和background_color传入颜色代码")
#     print("\t1. 黑色：BLACK")
#     print("\t2. 红色：RED")
#     print("\t3. 绿色：GREEN")
#     print("\t4. 黄色：YELLOW")
#     print("\t5. 蓝色：BLUE")
#     print("\t6. 洋红色：MAGENTA")
#     print("\t7. 青色：CYAN")
#     print("\t8. 白色：WHITE")
#     print("\t9. 浅灰色：LIGHT_GRAY")
#     print("\t10. 亮红色：BRIGHT_RED")
#     print("\t11. 亮绿色：BRIGHT_GREEN")
#     print("\t12. 亮黄色：BRIGHT_YELLOW")
#     print("\t13. 亮蓝色：BRIGHT_BLUE")
#     print("\t14. 亮洋红色：BRIGHT_MAGENTA")
#     print("\t15. 亮青色：BRIGHT_CYAN")
#     print("\t16. 亮白色：BRIGHT_WHITE")


# 字体样式

BOLD = bold = "1"
ITALIC = italic = "3"
UNDERLINE = underline = "4"
HIDDEN = hidden = "8"

# 颜色
BLACK = black = "0"
RED = red = "1"
GREEN = green = "2"
YELLOW = yellow = "3"
BLUE = blue = "4"
MAGENTA = magenta = "5"
CYAN = cyan = "6"
WHITE = white = "7"
LIGHT_GRAY = light_gray = "60"
BRIGHT_RED = bright_red = "61"
BRIGHT_GREEN = bright_green = "62"
BRIGHT_YELLOW = bright_yellow = "63"
BRIGHT_BLUE = bright_blue = "64"
BRIGHT_MAGENTA = bright_magenta = "65"
BRIGHT_CYAN = bright_cyan = "66"
BRIGHT_WHITE = bright_white = "67"

