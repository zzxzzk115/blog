<style>
.button {
  min-width: 150px;
  display: inline-block;
  padding: 5px 15px;
  margin: 5px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: var(--text-color);
  background-color: var(--theme-color-mask);
  border: 3px solid var(--dark-grey);
  border-radius: 10px;
  box-shadow: 0 9px var(--light-grey);
}

.button:hover {
    color: var(--text-color-bright);
}

.button:active {
  box-shadow: 0 5px var(--grey3);
  transform: translateY(4px);
}
</style>

<template>
    <button class="button" @click="onButtonClick"> {{ Pronounciations[props.type].name }} <i class="fa-solid fa-circle-play"></i> <br/> {{ props.phoneticSymbol }} </button>
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
    type: String,
    phoneticSymbol: String
});

var _howl = null;

var _canPlay = true;

const onButtonClick = () => {
    if (!_howl) {
        _howl = new Howl({
            src: ['http://dict.youdao.com/dictvoice?type=' + Pronounciations[props.type].value + '&audio=' + props.word],
            html5: true,
            format: ['mp3', 'flac', 'mpeg'],
            volume: 0.6
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