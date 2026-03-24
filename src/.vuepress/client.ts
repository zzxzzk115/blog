import { defineClientConfig } from "@vuepress/client";
import WordReader from "./components/WordReader.vue";
import FriendLinks from "./components/FriendLinks.vue";

export default defineClientConfig({
  enhance: ({ app, router, siteData }) => {
    app.component("WordReader", WordReader);
    app.component("FriendLinks", FriendLinks);
  },
});