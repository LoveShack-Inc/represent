<template>
    <div>
        <section>
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
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
                >

                <b-table-column field="vote_id" label="ID" numeric v-slot="props">
                    {{ props.row.vote_id }}
                </b-table-column>

                <b-table-column field="sourceUrl" label="Source" v-slot="props">
                    <a :href="props.row.sourceUrl">
                        {{ props.row.sourceUrl.split("/").pop().split(".")[0] }}
                    </a>
                    <!-- <a :href="`/view/vote/${props.row.vote_id}`">
                        {{ props.row.sourceUrl }}
                    </a> -->
                </b-table-column>

                <b-table-column field="sourceType" label="Type" v-slot="props">
                    {{ props.row.sourceType }}
                </b-table-column>

                <b-table-column field="sourceFormat" label="Format" v-slot="props">
                    {{ props.row.sourceFormat }}
                </b-table-column>

                <b-table-column field="isProcessed" label="Processed?" boolean v-slot="props">
                    {{ props.row.vote_id == 0 }}
                </b-table-column>
            </b-table>
        </section>
    </div>

</template>

<script>
    const axios = require('axios');

    export default {
        name: 'repp-vote-record-table',
        methods: {
            getRecordPage: function (page) {
                axios
                .get('/api/v1/votes', {
                    params: {
                        page: page,
                        size: this.pageSize,
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
                columns: []
            }
        }
    }
</script>