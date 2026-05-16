from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from backend.app.agents.planner_agent import PlannerAgent
from backend.app.agents.executor_agent import ExecutorAgent
from backend.app.agents.validator_agent import ValidatorAgent


# =========================
# INITIALIZE AGENTS
# =========================
planner = PlannerAgent()

executor = ExecutorAgent()

validator = ValidatorAgent()


# =========================
# GRAPH STATE
# =========================
class AgentState(TypedDict):

    message: str
    session_id: str
    user_id: str

    plan: Dict[str, Any]

    response: str

    retrieved_docs: List[str]

    validation: Dict[str, Any]

    provider: str


# =========================
# PLANNER NODE
# =========================
def planner_node(state: AgentState):

    plan = planner.plan(state["message"])

    print(f"PLAN: {plan}")

    state["plan"] = plan

    return state


# =========================
# EXECUTOR NODE
# =========================
async def executor_node(state: AgentState):

    result = await executor.execute(
        message=state["message"],
        session_id=state["session_id"],
        user_id=state["user_id"],
        plan=state["plan"]
    )

    state["response"] = result["response"]

    state["retrieved_docs"] = result["retrieved_docs"]

    state["provider"] = result["provider"]

    print(f"PROVIDER USED: {result['provider']}")

    return state


# =========================
# VALIDATOR NODE
# =========================
def validator_node(state: AgentState):

    validation = validator.validate(
        state["response"],
        state["retrieved_docs"]
    )

    print(f"VALIDATION: {validation}")

    state["validation"] = validation

    return state


# =========================
# BUILD LANGGRAPH
# =========================
workflow_graph = StateGraph(AgentState)

# ADD NODES
workflow_graph.add_node(
    "planner",
    planner_node
)

workflow_graph.add_node(
    "executor",
    executor_node
)

workflow_graph.add_node(
    "validator",
    validator_node
)

# ENTRY POINT
workflow_graph.set_entry_point("planner")

# EDGES
workflow_graph.add_edge(
    "planner",
    "executor"
)

workflow_graph.add_edge(
    "executor",
    "validator"
)

workflow_graph.add_edge(
    "validator",
    END
)

# COMPILE GRAPH
workflow = workflow_graph.compile()