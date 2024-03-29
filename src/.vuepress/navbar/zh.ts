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
    text: "HPG笔记",
    icon: "note",
    prefix: "/zh/hpg-notes/",
    children: [
      {
        text: "COMP5812M - 模型与渲染基础",
        link: "comp5812m/001-rendering-and-transformations",
      },
      {
        text: "COMP5821M - 几何处理",
        link: "comp5821m/001-basic-concepts",
      },
      {
        text: "COMP5823M - 动画与模拟",
        link: "comp5823m",
      },
      {
        text: "COMP5930M - 科学计算",
        link: "comp5930m",
      },
    ]
  },
  // { 
  //   text: "游戏引擎开发",
  //   icon: "unity",
  //   prefix: "/zh/game-engine-dev/",
  //   children: [
  //     { 
  //       text: "计算机图形学",
  //       icon: "triangle",
  //       prefix: "computer-graphics/",
  //       children: [ { text: "基础理论", link: "basic-theories/intro"} ]
  //     },
  //   ]
  // },
  { text: "关于", icon: "md-information-circle", link: "/zh/intro"},
  {
    text: "个人网站",
    icon: "md-at",
    link: "https://zzxzzk115.github.io",
  },
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
