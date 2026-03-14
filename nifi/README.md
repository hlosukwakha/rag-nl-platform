# Apache NiFi placeholder

Add a flow that:
1. polls CBS / PDOK / Rijkswaterstaat APIs
2. normalizes payloads to JSON
3. writes raw docs to OpenSearch
4. forwards chunk jobs to the embedding/index service
