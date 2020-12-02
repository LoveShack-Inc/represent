
<template>
  <div class="card">
      <div class="card-image">
          <embed 
            type="application/pdf" 
            :src="'/api/v1/view/vote/' + voteObjectId"
            width="100%"
            height="100%"
          >
      </div>
      <div class="card-content">
          <div class="content">
              <div v-for="(value, key) in results" :key="key">
                {{ value.display }}: {{ value.value }}
              </div>
              <br>
              <small>Vote Taken: {{ vote_time }}</small>
              <br>
              <small>Vote id: {{ voteObjectId }}</small>
          </div>
      </div>
  </div>
</template>

<script>
const axios = require('axios');
export default {
  name: 'repp-vote-result-card',
  components: {},
  props: {
    voteObjectId: Number,
  },
  methods: {
    getVoteResult: function (voteObjectId) {
        axios
          .get('/api/v1/result', {
              params: {
                voteRecordId: voteObjectId
              }
          })
          .then(response => {
              this.is_loading = true
              this.votes = response.data.resources
              this.is_loading = false
              for (const i in this.votes) {
                let vote = this.votes[i]["repVote"].toLowerCase()
                this.results[vote]["value"] = this.results[vote]["value"] + 1
              }
              if (this.votes.length > 0) {
                this.vote_time = Date(this.votes[0]["unixTime"] * 1000).toLocaleString()
                this.vote_name = this.votes[0]["voteName"]

              }
          })
          .catch(function (error) {
              console.log(error);
              this.is_loading = false
              this.table_records = []
              this.vote_time = 0
              this.vote_name = ""
          })
      },
  },
  mounted () {
      this.getVoteResult(this.voteObjectId)
  },
  data() {
      return {
          is_loading: true,
          votes: [],
          results: {
            y: {display: "Yea", value: 0},
            n: {display: "Nay", value: 0},
            a: {display: "Absent/Abstain", value: 0},
            x: {display: "Absent", value: 0},
          },
          vote_time: 0,
          vote_name: ""
      }
  }
}
</script>

<style scoped>
.card-image {
  height: 60vh;
}

</style>