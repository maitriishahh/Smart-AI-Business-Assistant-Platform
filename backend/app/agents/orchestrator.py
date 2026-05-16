from backend.app.agents.planner_agent import PlannerAgent
from backend.app.agents.executor_agent import ExecutorAgent
from backend.app.agents.validator_agent import ValidatorAgent

class AgentOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent()

        self.executor = ExecutorAgent()

        self.validator = ValidatorAgent()

    async def run(self,message:str,session_id:str,user_id:str):
        plan = self.planner.plan(message)
        print(f"Plan: {plan}")
        
        execution_result = await self.executor.execute(message=message, session_id=session_id, user_id=user_id, plan=plan)

        validation = self.validator.validate(execution_result["response"],execution_result["retrieved_docs"])

        print(f"Validation: {validation}")
        print(f"Provider Used: {execution_result['provider']}")

        return {
            "plan":plan,
            "response": execution_result["response"],
            "validation":validation,  
            "provider": execution_result["provider"]
}