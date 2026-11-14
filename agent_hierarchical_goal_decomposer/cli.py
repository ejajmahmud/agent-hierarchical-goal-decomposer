"""CLI for agent-hierarchical-goal-decomposer."""
import argparse
import sys
from .core import GoalDecomposer

def main():
    parser = argparse.ArgumentParser(description="Agent Hierarchical Goal Decomposer CLI")
    parser.add_argument("--demo", action="store_true", help="Run goal tree decomposition demo")
    args = parser.parse_args()

    if args.demo:
        decomposer = GoalDecomposer()
        tree = decomposer.decompose("Migrate Postgres User Schema")
        print(f"[+] Root Goal: {tree.description}")
        for sg in tree.subgoals:
            print(f"    Subgoal [{sg.goal_id}]: {sg.description} (pre: {sg.preconditions})")
        context = {"env_ready": True}
        plan_res = decomposer.execute_plan(tree, context)
        print(f"[+] Execution Plan Result: {plan_res}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
