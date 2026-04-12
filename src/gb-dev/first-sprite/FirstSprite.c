#include <gb/gb.h>
#include <stdio.h>
#include "Smile.h"

void main()
{
    // 设置精灵数据
    // 从第 0 号位的 Tile 开始，设置 No.0 的瓦块的数据
    // 数据来源于 Smile 数组
    set_sprite_data(0, 0, Smile);

    // 设置精灵使用哪个瓦块的数据
    // 这里是 No.0 精灵使用 No.0 瓦块数据
    set_sprite_tile(0, 0);

    // 一个宏，内部设置 LCDC 寄存器的第 1 位为 1，
    // 目的是开启精灵层，代表显示所有精灵
    SHOW_SPRITES;

    // 将精灵 No.0 移动到 (84, 78) 的位置，即屏幕中央附近
    move_sprite(0, 84, 78);
}