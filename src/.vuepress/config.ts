import { defineUserConfig } from "vuepress";
import { viteBundler } from "@vuepress/bundler-vite";

import theme from "./theme.js";

const isDev = process.env.NODE_ENV === 'development';

export default defineUserConfig({
  base: isDev ? '/' : '/blog/', // 本地调试时，不用前缀

  description: 'Notes on graphics, games, and things I build. By Kexuan Zhang / Lazy_V.',
  
  locales: {
    // 键名是该语言所属的子路径
    // 作为特例，默认语言可以使用 '/' 作为其路径。
    '/': {
      lang: 'en-US', // 将会被设置为 <html> 的 lang 属性
      title: "Lazy_V's Blog",
      description: "Notes on graphics, games, and things I build. By Kexuan Zhang / Lazy_V.",
    },
    '/zh/': {
      lang: 'zh-CN',
      title: "Lazy_V 的博客",
      description: "图形、游戏，以及我捣鼓的小东西。张可宣 / Lazy_V 的技术笔记。",
    }
  },

  plugins: [],

  theme,

  shouldPrefetch: false,

  bundler: viteBundler(),
});
