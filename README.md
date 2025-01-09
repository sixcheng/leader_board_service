# leader_board_service
![img.png](img.png)
底层数据结构使用跳表，跳表时间复杂度为logN，数据量大时性能更优，实际游戏系统通过redis的zset来实现。



第三题，可以通过修改跳表的node来实现，每个node的obj改为一个包含多个player的数组