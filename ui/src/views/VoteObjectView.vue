<template>
    <section>
        <div class="card">
            <div class="card-header" role="button">
                <p class="card-header-title">
                    <template>Vote Records</template>
                </p>
            </div>
            <div class="card-content">
                <div>
                    <p>
                        The Repp project periodically gathers data from different official public
                        sources and stores them. Once stored, they are processed and key information
                        is pulled from them and made available for Repp users to search and view.
                    </p>
                    <p>
                        This page displays the records that have been discovered and stored within
                        the Repp system.
                    </p>
                </div>
            </div>
        </div>
        <hr>
        <repp-vote-record-table></repp-vote-record-table>
    </section>
</template>

<script>
import ReppVoteRecordTable from '../components/ReppVoteRecordTable.vue';
export default {
  name: 'repp-vote-object-view',
  components: {
      ReppVoteRecordTable,
  },
  props: {
    title: String,
  }
}
</script>

