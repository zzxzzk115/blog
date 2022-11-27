import { defineUserConfig } from "vuepress";
import { searchProPlugin } from "vuepress-plugin-search-pro";
import { mdEnhancePlugin } from "vuepress-plugin-md-enhance";
import theme from "./theme.js";

export default defineUserConfig({
  base: "/blog/",

  description: 'TALK IS CHEAP, SHOW ME THE CODE.',
  
  locales: {
    // 键名是该语言所属的子路径
    // 作为特例，默认语言可以使用 '/' 作为其路径。
    '/': {
      lang: 'en-US', // 将会被设置为 <html> 的 lang 属性
      title: "Lazy_V's Blog"
    },
    '/zh/': {
      lang: 'zh-CN',
      title: "Lazy_V 的博客"
    }
  },

  plugins: [
    searchProPlugin({
      indexContent: true
    }),
    mdEnhancePlugin({
      // 你的选项
    }),
  ],

  theme,

  shouldPrefetch: false,
});
