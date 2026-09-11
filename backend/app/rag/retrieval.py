class TenantRetriever:
    async def search_business(self, business_id: str, query: str) -> list[dict]:
        # MongoDB Vector Search filter: business_id + source_scope="business" + enabled=true.
        return []

    async def search_common(self, query: str) -> list[dict]:
        # MongoDB Vector Search filter: source_scope="common" + enabled=true.
        return []
