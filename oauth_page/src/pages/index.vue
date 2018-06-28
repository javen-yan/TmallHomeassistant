<template>
  <section>
    <a-breadcrumb>
      <a-breadcrumb-item href="">
        <a-icon type="home" />
      </a-breadcrumb-item>
      <a-breadcrumb-item href="">
        <span>{{title}}</span>
      </a-breadcrumb-item>
    </a-breadcrumb>
  </section>
</template>

<script>
export default {
  name: 'Index',
  data () {
    return {
      title: '首页'
    }
  }
}
</script>

<style scoped>

</style>
