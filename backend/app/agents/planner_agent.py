from typing import Dict


class PlannerAgent:

    def plan(self, query: str) -> Dict:

        query_lower = query.lower()

        if any(word in query_lower for word in [
            "document",
            "pdf",
            "summarize",
            "report",
            "file",
            "services",
            "pricing",
            "plans",
            "company",
            "offerings"
        ]):

            return {
                "task": "rag_qa",
                "needs_retrieval": True,
                "needs_validation": True
            }

        elif any(word in query_lower for word in [
            "interested",
            "pricing",
            "demo",
            "contact",
            "crm"
        ]):

            return {
                "task": "lead_capture",
                "needs_retrieval": True,
                "needs_validation": True
            }

        elif any(word in query_lower for word in [
            "email",
            "follow-up",
            "automation",
            "schedule"
        ]):

            return {
                "task": "automation",
                "needs_retrieval": False,
                "needs_validation": True
            }

        return {
            "task": "general_chat",
            "needs_retrieval": False,
            "needs_validation": True
        }