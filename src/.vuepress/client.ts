import { defineClientConfig } from "@vuepress/client";
import WordReader from "./components/WordReader.vue";
import FriendLinks from "./components/FriendLinks.vue";
import ContactCopyFeedback from "./components/ContactCopyFeedback.vue";

export default defineClientConfig({
  rootComponents: [ContactCopyFeedback],
  enhance: ({ app, router, siteData }) => {
    app.component("WordReader", WordReader);
    app.component("FriendLinks", FriendLinks);
  },
});
