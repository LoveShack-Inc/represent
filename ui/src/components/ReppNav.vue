<template>
    <b-navbar>
        <template slot="brand">
            <b-navbar-item tag="router-link" :to="{path: '/'}">
                <i class="fa fa-2x fa-vote-yea"></i>
            </b-navbar-item>
        </template>

        <template slot="start">
            <b-navbar-item tag="router-link" to="/">
                Home
            </b-navbar-item>
            <b-navbar-dropdown label="View">
                <b-navbar-item tag="router-link" to="/votes">
                    Vote Records
                </b-navbar-item>
                <b-navbar-item tag="router-link" to="/">
                    Am I Represented?
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>

        <template slot="end">
            <b-navbar-item tag="div">
                <div>
                    <a href="https://github.com/LoveShack-Inc/represent">
                        <strong>GitHub</strong>
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>

export default {
  name: 'repp-nav',
  components: {

  },
  props: {
    title: String,
    pages: Array,
  }
}
</script>
