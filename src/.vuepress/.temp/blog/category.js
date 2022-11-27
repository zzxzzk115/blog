export const categoryMap = {"category":{"/":{"path":"/category/","map":{"Jottings":{"path":"/category/jottings/","keys":["v-6516c560"]}}},"/zh/":{"path":"/zh/category/","map":{"随笔":{"path":"/zh/category/%E9%9A%8F%E7%AC%94/","keys":["v-3cb9fdd1"]}}}},"tag":{"/":{"path":"/tag/","map":{"Jottings":{"path":"/tag/jottings/","keys":["v-6516c560"]}}},"/zh/":{"path":"/zh/tag/","map":{"随笔":{"path":"/zh/tag/%E9%9A%8F%E7%AC%94/","keys":["v-3cb9fdd1"]}}}}};

if (import.meta.webpackHot) {
  import.meta.webpackHot.accept();
  if (__VUE_HMR_RUNTIME__.updateBlogCategory)
    __VUE_HMR_RUNTIME__.updateBlogCategory(categoryMap);
}

if (import.meta.hot)
  import.meta.hot.accept(({ categoryMap }) => {
    __VUE_HMR_RUNTIME__.updateBlogCategory(categoryMap);
  });


