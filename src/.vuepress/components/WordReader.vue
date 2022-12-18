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
    fill: var(--text-color-bright);
}

.button:active {
  box-shadow: 0 5px var(--grey3);
  transform: translateY(4px);
}

.button > .left {
    float: left;
}

.button > .right {
    float: right;
}
</style>

<template>
    <button class="button" @click="onButtonClick">
      <div class="left">
        {{ Pronounciations[props.type].name }}<br/> 
        {{ props.phoneticSymbol }} 
      </div>
      <div class="right">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="30" height="30"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M512 256c0 141.4-114.6 256-256 256S0 397.4 0 256S114.6 0 256 0S512 114.6 512 256zM188.3 147.1c-7.6 4.2-12.3 12.3-12.3 20.9V344c0 8.7 4.7 16.7 12.3 20.9s16.8 4.1 24.3-.5l144-88c7.1-4.4 11.5-12.1 11.5-20.5s-4.4-16.1-11.5-20.5l-144-88c-7.4-4.5-16.7-4.7-24.3-.5z"/></svg>
      </div>
    </button>
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