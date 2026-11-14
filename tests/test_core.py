"""Unit tests for agent-hierarchical-goal-decomposer."""
import unittest
from agent_hierarchical_goal_decomposer.core import GoalDecomposer, GoalNode, InvariantValidator

class TestGoalDecomposer(unittest.TestCase):
    def setUp(self):
        self.decomposer = GoalDecomposer()

    def test_decomposition_structure(self):
        tree = self.decomposer.decompose("Build Release Wheel")
        self.assertEqual(len(tree.subgoals), 3)
        self.assertEqual(tree.subgoals[0].goal_id, "prep")
        self.assertEqual(tree.subgoals[1].goal_id, "exec")
        self.assertEqual(tree.subgoals[2].goal_id, "ver")

    def test_execution_with_satisfied_preconditions(self):
        tree = self.decomposer.decompose("Test Task")
        context = {"env_ready": True}
        res = self.decomposer.execute_plan(tree, context)
        self.assertEqual(len(res["results"]), 3)
        self.assertTrue(all(r["status"] == "COMPLETED" for r in res["results"]))

    def test_blocked_by_missing_precondition(self):
        tree = self.decomposer.decompose("Blocked Task")
        context = {"env_ready": False}
        res = self.decomposer.execute_plan(tree, context)
        self.assertEqual(res["results"][0]["status"], "BLOCKED_PRECONDITION")
