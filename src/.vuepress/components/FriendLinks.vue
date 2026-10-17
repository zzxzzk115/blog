<template>
  <div class="friend-links">
    <div v-for="friend in friends" :key="friend.link" class="friend-link">
      <a :href="friend.link" target="_blank" rel="noopener noreferrer" class="friend-link-inner">
        <div class="friend-avatar-wrap">
          <FriendAvatar :src="friend.avatar" :name="friend.name" />
        </div>
        <div class="friend-info">
          <div class="friend-name">{{ friend.name }}</div>
          <div class="friend-desc">{{ friend.desc }}</div>
        </div>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import FriendAvatar from './FriendAvatar.vue';

defineProps<{
  friends: Array<{
    name: string;
    link: string;
    desc?: string;
    avatar?: string;
  }>
}>();
</script>

<style scoped>
  .friend-links {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
  }
  .friend-link {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 0;
    min-width: 320px;
    max-width: 420px;
    background: #fafbfc;
    transition: box-shadow 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  }
  .friend-link:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  }
  .friend-link-inner {
    padding: 1rem;
    height: 100%;
  }
  .friend-avatar-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 64px;
  }
  .friend-info {
    flex: 1 1 70%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 1.2rem;
    min-width: 0;
  }
  .friend-name {
    font-weight: bold;
    font-size: 1.15rem;
    color: #222;
    margin-bottom: 0.3rem;
    word-break: break-all;
  }
  .friend-desc {
    color: #888;
    font-size: 0.97rem;
    word-break: break-all;
  }
</style>
