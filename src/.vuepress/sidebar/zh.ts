import { sidebar } from "vuepress-theme-hope";

export const zhSidebar = sidebar({
  "/zh/": [
    "",
    // {
    //   text: "如何使用",
    //   icon: "creative",
    //   prefix: "guide/",
    //   link: "guide/",
    //   children: "structure",
    // },
    {
      text: "文章",
      icon: "feather",
      prefix: "posts/",
      children: "structure",
      collapsible: true,
    },
    {
      text: "语言学习",
      icon: "language",
      prefix: "language/",
      children: "structure",
      collapsible: true,
    },
    {
      text: "游戏开发",
      icon: "gamepad",
      prefix: "game-dev/",
      children: "structure",
      collapsible: true,
    },
    "intro",
    // "slides",
  ],
});
