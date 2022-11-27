export const typeMap = {"article":{"/":{"path":"/article/","keys":["v-6516c560"]},"/zh/":{"path":"/zh/article/","keys":["v-3cb9fdd1"]}},"encrypted":{"/":{"path":"/encrypted/","keys":[]},"/zh/":{"path":"/zh/encrypted/","keys":[]}},"slide":{"/":{"path":"/slide/","keys":[]},"/zh/":{"path":"/zh/slide/","keys":[]}},"star":{"/":{"path":"/star/","keys":["v-6516c560"]},"/zh/":{"path":"/zh/star/","keys":["v-3cb9fdd1"]}},"timeline":{"/":{"path":"/timeline/","keys":["v-6516c560"]},"/zh/":{"path":"/zh/timeline/","keys":["v-3cb9fdd1"]}}};

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept();
  if (__VUE_HMR_RUNTIME__.updateBlogType)
    __VUE_HMR_RUNTIME__.updateBlogType(typeMap);
}

if (import.meta.hot)
  import.meta.hot.accept(({ typeMap }) => {
    __VUE_HMR_RUNTIME__.updateBlogType(typeMap);
  });

