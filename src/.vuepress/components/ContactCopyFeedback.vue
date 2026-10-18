<template>
  <div v-if="message" class="contact-copy-feedback" role="status">{{ message }}</div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from "vue";
import { wechatId, wechatFallback } from "../socialContacts";

const message = ref("");
let timer: ReturnType<typeof setTimeout> | undefined;
async function copyContact(event: MouseEvent) {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const link = event.target instanceof Element ? event.target.closest<HTMLAnchorElement>("a.vp-social-media") : null;
  if (link?.getAttribute("href") !== wechatFallback) return;
  event.preventDefault();
  const chinese = document.documentElement.lang.startsWith("zh");
  try {
    await navigator.clipboard.writeText(wechatId);
    message.value = chinese ? "微信号已复制" : "WeChat ID copied.";
    clearTimeout(timer);
    timer = setTimeout(() => { message.value = ""; }, 2500);
  } catch {
    window.location.assign(chinese ? "/blog/zh/intro.html#wechat" : wechatFallback);
  }
}
onMounted(() => document.addEventListener("click", copyContact));
onBeforeUnmount(() => { document.removeEventListener("click", copyContact); clearTimeout(timer); });
</script>

<style scoped>
.contact-copy-feedback {
  position: fixed;
  z-index: 1000;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 18px;
  border: 1px solid var(--vp-c-border);
  border-radius: 4px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text);
  box-shadow: 0 2px 12px rgb(0 0 0 / 15%);
}
</style>
