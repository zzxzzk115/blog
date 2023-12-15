import { defineUserConfig } from "vuepress";
import { searchProPlugin } from "vuepress-plugin-search-pro";
import theme from "./theme.js";

const isDev = process.env.NODE_ENV === 'development';

export default defineUserConfig({
  base: isDev ? '/' : '/blog/', // 本地调试时，不用前缀

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
    })
  ],

  theme,

  shouldPrefetch: false,
});
