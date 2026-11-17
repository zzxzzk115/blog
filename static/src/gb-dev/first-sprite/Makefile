# 设置 LCC 编译器执行路径
CC  = $(GBDKDIR)/bin/lcc

# 设置 SameBoy 执行路径
EMU = /Applications/SameBoy.app/Contents/MacOS/SameBoy

# 默认行为，编译各个编译单元，最后链接得到 FirstSprite.gb
all:
	$(CC) -Wa-l -Wl-m -Wl-j -o FirstSprite.gb Smile.c FirstSprite.c

# 编译得到 FirstSprite.gb 后，使用 SameBoy 启动
run: all
	$(EMU) FirstSprite.gb

# 清理
clean:
	rm -f *.o *.lst *.map *.gb *.ihx *.sym *.cdb *.adb *.asm *.noi