<template>
    <div>
        <div class="columns is-centered">
            <b-field>
                <div class="control">
                    <b-switch v-on:input="onButtonToggle" v-model="includeUnprocessed">Include Unprocessed {{ includeUnprocessed }}</b-switch>
                </div>
            </b-field>
        </div>
        <b-modal v-model="isResultModalActive">
            <repp-vote-result-card 
                :voteObjectId="modalVoteObjectId"
            />
        </b-modal>
        <b-table 
            :data="table_records" 
            :columns="columns"
            :loading="is_loading"
            :striped="true"
            :hoverable="true"
            :paginated-simple="false"
            :paginated-rounded="false"

            paginated
            backend-pagination
            :total="total"
            :per-page="pageSize"
            @page-change="onPageChange"
            >

            <b-table-column field="vote_id" label="ID" numeric v-slot="props">
                <a v-if="props.row.isProcessed" @click="onModalClick(props.row.vote_id)">
                    {{ props.row.vote_id }}
                </a>
                <div v-else>
                    {{ props.row.vote_id }}
                </div>
            </b-table-column>

            <b-table-column field="sourceUrl" label="Source" v-slot="props">
                <a :href="props.row.sourceUrl">
                    {{ props.row.sourceUrl.split("/").pop().split(".")[0] }}
                </a>
            </b-table-column>

            <b-table-column field="sourceType" label="Type" v-slot="props">
                {{ props.row.sourceType }}
            </b-table-column>

            <b-table-column field="sourceFormat" label="Format" v-slot="props">
                {{ props.row.sourceFormat }}
            </b-table-column>

            <b-table-column field="isProcessed" label="Processed?" boolean v-slot="props">
                {{ props.row.isProcessed == 1 ? "Yes" : "No" }}
            </b-table-column>
        </b-table>
    </div>

</template>

<script>
    import ReppVoteResultCard from './ReppVoteResultCard.vue'
    const axios = require('axios');

    export default {
        name: 'repp-vote-record-table',
        components: {
            ReppVoteResultCard,
        },
        methods: {
            getRecordPage: function (page) {
                axios
                .get('/api/v1/votes', {
                    params: {
                        page: page,
                        size: this.pageSize,
                        isProcessed: this.includeUnprocessed ? 0 : 1
                    }
                })
                .then(response => {
                    this.is_loading = true
                    this.table_records = response.data.resources
                    this.is_loading = false
                    this.currentPage = page + 1
                    this.total = response.data.totalCount
                    this.totalPages = response.data.totalPages
                })
                .catch(function (error) {
                    console.log(error);
                    this.is_loading = false
                    this.table_records = []
                })
            },
            onPageChange(page) {
                this.getRecordPage(page)
            },
            onButtonToggle() {
                this.onPageChange(this.currentPage)
            },
            onModalClick(id) {
                this.modalVoteObjectId = id
                this.isResultModalActive = true
            }
        },
        mounted () {
            this.getRecordPage(0)
        },
        data() {
            return {
                currentPage: 0,
                total: 0,
                totalPages: 0,
                is_loading: true,
                pageSize: 12,
                table_records: [],
                columns: [],
                includeUnprocessed: false,
                isResultModalActive: false,
                modalVoteObjectId: null,
            }
        }
    }
</script>
