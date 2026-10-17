<template>
  <span class="friend-avatar" role="img" :aria-label="name">
    <svg v-show="!loaded" class="avatar-placeholder" viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 22v-2a8 8 0 0 1 16 0v2Z" />
    </svg>
    <img
      v-if="src"
      :key="src"
      ref="image"
      :src="src"
      alt=""
      width="56"
      height="56"
      decoding="async"
      :class="{ loaded }"
      @load="checkImage"
      @error="loaded = false"
    />
  </span>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';

const props = defineProps<{ src?: string; name: string }>();
const image = ref<HTMLImageElement>();
const loaded = ref(false);
const checkImage = () => { loaded.value = !!image.value?.complete && image.value.naturalWidth > 0; };

watch(() => props.src, () => { loaded.value = false; });
// Cached images can finish before hydration attaches the load handler.
onMounted(checkImage);
</script>

<style scoped>
.friend-avatar {
  position: relative;
  display: inline-block;
  flex: 0 0 56px;
  width: 56px;
  height: 56px;
  overflow: hidden;
  border-radius: 50%;
  background: var(--vp-c-bg-alt, #edf0f2);
  color: var(--vp-c-text-mute, #7b8992);
  box-shadow: 0 1px 4px rgba(0, 0, 0, .06);
}
.avatar-placeholder {
  position: absolute;
  inset: 10px;
  width: 36px;
  height: 36px;
  fill: currentColor;
}
.friend-avatar img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
}
.friend-avatar img.loaded { opacity: 1; }
</style>
