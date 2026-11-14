"""Core hierarchical goal decomposer implementation."""
from typing import List, Dict, Any, Optional

class InvariantValidator:
    def validate_precondition(self, pre: str, context: Dict[str, Any]) -> bool:
        if not pre:
            return True
        key = pre.strip().lower()
        return context.get(key, True) is True

    def validate_postcondition(self, post: str, context: Dict[str, Any]) -> bool:
        if not post:
            return True
        key = post.strip().lower()
        return context.get(key, True) is True

class GoalNode:
    def __init__(self, goal_id: str, description: str, preconditions: Optional[List[str]] = None, postconditions: Optional[List[str]] = None):
        self.goal_id = goal_id
        self.description = description
        self.preconditions = preconditions or []
        self.postconditions = postconditions or []
        self.subgoals: List["GoalNode"] = []
        self.completed = False

    def add_subgoal(self, node: "GoalNode"):
        self.subgoals.append(node)

    def is_executable(self, context: Dict[str, Any], validator: InvariantValidator) -> bool:
        return all(validator.validate_precondition(p, context) for p in self.preconditions)

class GoalDecomposer:
    def __init__(self):
        self.validator = InvariantValidator()

    def decompose(self, macro_goal: str) -> GoalNode:
        root = GoalNode("root", macro_goal)
        # Decompose into standard 3-tier lifecycle: prepare, execute, verify
        g_prep = GoalNode("prep", f"Prepare environment for: {macro_goal}", preconditions=["env_ready"])
        g_exec = GoalNode("exec", f"Execute action for: {macro_goal}", preconditions=["prep_completed"])
        g_ver = GoalNode("ver", f"Verify invariant postconditions for: {macro_goal}", preconditions=["exec_completed"])

        root.add_subgoal(g_prep)
        root.add_subgoal(g_exec)
        root.add_subgoal(g_ver)
        return root

    def execute_plan(self, root: GoalNode, context: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for sg in root.subgoals:
            if sg.is_executable(context, self.validator):
                # Mark execution
                context[f"{sg.goal_id}_completed"] = True
                sg.completed = True
                results.append({"goal_id": sg.goal_id, "status": "COMPLETED"})
            else:
                results.append({"goal_id": sg.goal_id, "status": "BLOCKED_PRECONDITION"})
                break
        return {"total_subgoals": len(root.subgoals), "results": results}
