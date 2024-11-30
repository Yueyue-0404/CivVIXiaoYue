# ETL步骤
1. ## 本地化
   本地化发生在`DebugLocalization.sqlite`库里。
   1. 将游戏中所有xml格式存储的文本文件置于`../../text`，允许可以分装在不同的子目录里，但不允许有其他`.xml`干扰。
   2. 打开`zh_Hans_L.py`并修改`sort_key`函数使资料片按顺序跑数。
   3. 执行`zh_Hans_L.py`，生成的`.sql`可以用于数据迁移。
   4. 用可视化工具将结果表`zh_Hans_Text`迁移到`DebugGamePlay.sqlite`中，或用第3步中生成的`.sql`在`DebugGamePlay.sqlite`中跑一遍。这个表后续有大用。
2. ## 建立真实数据与汉字的映射
   这些发生在`DebugGamePlay.sqlite`库里。
   1. 执行本目录下的`BotData_ETL.py`。
