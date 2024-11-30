# ETL步骤
1. ## 本地化
   本地化发生在`DebugLocalization.sqlite`库里，然后会在`SimplizedData.sqlite`库里创建一模一样的表。
   1. 将游戏中所有xml格式存储的文本文件置于`../../text`，允许分装在不同的子目录里，但不允许有其他`.xml`干扰。
   2. 打开`zh_Hans_L.py`并修改`sort_key`函数使资料片按顺序跑数。
   3. 执行`zh_Hans_L.py`。
2. ## 数据处理
   这些发生在`DebugGamePlay.sqlite`库里，然后会在`SimplizedData.sqlite`库里创建一模一样的表。
   1. 执行本目录下的`BotData_ETL.py`。
3. ## 建立真实数据与汉字的映射
   这些发生在`DebugGamePlay.sqlite`库里，然后会在`SimplizedData.sqlite`库里创建一模一样的表。
   1. 执行本目录下的`Alias_L.py`。
