<template>
    <button @click="onButtonClick">Read</button>
    
</template>
<script setup>
import {Howl, Howler} from 'howler';

const props = defineProps({
    word: String
});

const onButtonClick = () => {
    var sound = new Howl({
      src: [ 'http://dict.youdao.com/dictvoice?type=0&audio=' + props.word ],
      autoplay: true,
      html5: true,
      format: ['mp3', 'flac', 'mpeg'],
    });
};
</script>