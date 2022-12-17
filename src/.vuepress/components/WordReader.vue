<style>
.button {
  display: inline-block;
  padding: 5px 15px;
  margin: 5px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: var(--text-color);
  background-color: var(--grey14);
  border: 3px solid var(--border-color);
  border-radius: 10px;
  box-shadow: 0 9px var(--light-grey);
}

.button:hover {background-color: var(--white)}

.button:active {
  box-shadow: 0 5px var(--dark-grey);
  transform: translateY(4px);
}
</style>

<template>
    <button class="button" @click="onButtonClick"> {{ Pronounciations[props.type].name }} <i class="fa-solid fa-circle-play"></i></button>
</template>

<script setup>
import {Howl, Howler} from 'howler';

const Pronounciations = {
    US: {
        value: 0,
        name: '美🇺🇸'
    },
    UK: {
        value: 1,
        name: '英🇬🇧'
    }
}

const props = defineProps({
    word: String,
    type: String
});

var _howl = null;

var _canPlay = true;

const onButtonClick = () => {
    if (!_howl) {
        _howl = new Howl({
            src: ['http://dict.youdao.com/dictvoice?type=' + Pronounciations[props.type].value + '&audio=' + props.word],
            html5: true,
            format: ['mp3', 'flac', 'mpeg']
        });
        _howl.on('end', function(){
            _canPlay = true;
        });
    }
    if (_canPlay) {
        _howl.play();
        _canPlay = false;
    }
};
</script>