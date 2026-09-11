class TenantRetriever:
    async def search(self, tenant_id: str, query: str) -> list[dict]:
        # Replace with pgvector hybrid search. tenant_id is a mandatory WHERE filter.
        return []
