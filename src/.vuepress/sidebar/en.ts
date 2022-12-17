import { sidebar } from "vuepress-theme-hope";

export const enSidebar = sidebar({
  "/": [
    "",
    // {
    //   icon: "discover",
    //   text: "Demo",
    //   prefix: "demo/",
    //   link: "demo/",
    //   children: "structure",
    // },
    {
      text: "Articles",
      icon: "feather",
      prefix: "posts/",
      children: "structure",
      collapsible: true,
    },
    {
      text: "GameDev",
      icon: "gamepad",
      prefix: "game-dev/",
      children: "structure",
      collapsible: true,
    },
    "intro",
    // "slides",
  ],
});
