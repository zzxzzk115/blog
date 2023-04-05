import { navbar } from "vuepress-theme-hope";

export const zhNavbar = navbar([
  "/zh/",
  { 
    text: "游戏开发",
    icon: "gamepad",
    prefix: "/zh/game-dev/",
    children: [
      { text: "游戏画廊", icon: "images", link: "001-games-gallery"},
      { 
        text: "复古游戏开发",
        icon: "video-game-gamasutra",
        prefix: "retro/",
        children: [ { text: "GB/GBC 游戏开发", icon: "gameboy", link: "gameboy/intro"} ]
      }
    ]
  },
  { 
    text: "游戏引擎开发",
    icon: "unity",
    prefix: "/zh/game-engine-dev/",
    children: [
      { 
        text: "计算机图形学",
        icon: "triangle",
        prefix: "computer-graphics/",
        children: [ { text: "基础理论", link: "basic-theories/intro"} ]
      },
    ]
  },
  { text: "关于", icon: "md-information-circle", link: "/zh/intro"},
  // { text: "演示", icon: "discover", link: "/zh/demo/" },
  // {
  //   text: "博文",
  //   icon: "edit",
  //   prefix: "/zh/posts/",
  //   children: [
  //     {
  //       text: "苹果",
  //       icon: "edit",
  //       prefix: "apple/",
  //       children: [
  //         { text: "苹果1", icon: "edit", link: "1" },
  //         { text: "苹果2", icon: "edit", link: "2" },
  //         "3",
  //         "4",
  //       ],
  //     },
  //     {
  //       text: "香蕉",
  //       icon: "edit",
  //       prefix: "banana/",
  //       children: [
  //         {
  //           text: "香蕉 1",
  //           icon: "edit",
  //           link: "1",
  //         },
  //         {
  //           text: "香蕉 2",
  //           icon: "edit",
  //           link: "2",
  //         },
  //         "3",
  //         "4",
  //       ],
  //     },
  //     { text: "樱桃", icon: "edit", link: "cherry" },
  //     { text: "火龙果", icon: "edit", link: "dragonfruit" },
  //     "tomato",
  //     "strawberry",
  //   ],
  // },
  // {
  //   text: "V2 文档",
  //   icon: "note",
  //   link: "https://vuepress-theme-hope.github.io/v2/zh/",
  // },
]);
