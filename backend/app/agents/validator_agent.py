class ValidatorAgent:

    def validate(
        self,
        response: str,
        retrieved_docs: list
    ):

        if not response:

            return {
                "status": "FAILED",
                "reason": "Empty response"
            }

        if len(response.strip()) < 5:

            return {
                "status": "FAILED",
                "reason": "Too short"
            }

        if retrieved_docs:

            combined_docs = " ".join(retrieved_docs)

            overlap = any(
                word in combined_docs
                for word in response.split()
            )

            if not overlap:

                return {
                    "status": "FAILED",
                    "reason": "Response not grounded"
                }

        return {
            "status": "VALID",
            "reason": None
        }