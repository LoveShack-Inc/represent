<template>
  <div>
      <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'repp-view',
  props: {
    title: String,
  }
}
</script>

<style scoped>
</style>
