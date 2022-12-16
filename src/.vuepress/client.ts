import { defineClientConfig } from "@vuepress/client";
import WordReader from "./components/WordReader.vue";

export default defineClientConfig({
  enhance: ({ app, router, siteData }) => {
    app.component("WordReader", WordReader);
  },
});