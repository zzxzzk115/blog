import { navbar } from "vuepress-theme-hope";

export const zhNavbar = navbar([
  "/zh/",
  { 
    text: "每日英语",
    icon: "a",
    prefix: "/zh/language/english/daily-english/",
    children: [
      { text: "词汇", icon: "spell-check", link: "01-vocabulary"},
      { text: "听力", icon: "headphones", link: "02-listening"},
      { text: "阅读", icon: "book-open", link: "03-reading"},
      { text: "写作", icon: "pen-to-square", link: "04-writing"},
      { text: "口语", icon: "comment-dots", link: "05-speaking"}
    ]
  },
  { 
    text: "游戏开发",
    icon: "gamepad",
    prefix: "/zh/game-dev/",
    children: [
      { text: "游戏画廊", icon: "images", link: "001-games-gallery"},
    ]
  },
  { text: "关于", icon: "circle-info", link: "/zh/intro"},
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
