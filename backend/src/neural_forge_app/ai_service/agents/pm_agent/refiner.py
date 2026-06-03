# from neural_forge_app.agents.pm_agent.helpers import splice_and_remap_tasks
# from neural_forge_app.agents.pm_agent.models import Plan, Task, TaskList

# from neural_forge_app.agents.tech_lead_agent.agent import TechLeadAgent
# from neural_forge_app.agents.pm_agent.agent import PMAgent

# async def refine_project_plan(max_loops: int, plan: Plan | None, pm_agent: PMAgent
# ,  tech_lead: TechLeadAgent):
#     for _ in range(max_loops):
        
#         if(not isinstance(plan, Plan) or len(plan.tasks) == 0):
#             print("No tasks found in the plan.")
#             break

#         vague_tasks_to_expand: list[Task] = await get_vague_tasks(plan, tech_lead)

#         # If no tasks need expansion, we are done!
#         if not vague_tasks_to_expand:
#             break

#         # 3. TARGETED EXPANSION (Only fix what is broken)
#         for vague_task in vague_tasks_to_expand:
#             print(f"\nExpanding vague task: {vague_task.title}\n")
#             new_subtasks = await pm_agent.expand_vague_task(vague_task)
#             print(f"new subtasks for {vague_task.title}: {new_subtasks}")

#             if(not isinstance(new_subtasks, TaskList) or len(new_subtasks.tasks) == 0):
#                 print(f"No subtasks found to expand vague task: {vague_task.title}")
#                 continue

#             plan.tasks = splice_and_remap_tasks(plan.tasks, vague_task, new_subtasks.tasks)
#     return plan

# async def get_vague_tasks(plan: Plan, tech_lead: TechLeadAgent):
#     vague_tasks_to_expand: list[Task] = []
    
#     for task in plan.tasks:

#         forbidden_words = ["dashboard", "module", "system", "flow", "feature", "page"]
#         contains_forbidden = any(word in task.title.lower() for word in forbidden_words)
        
#         is_truly_atomic = False
#         if(task.is_sufficiently_atomic):
#             print(f"/nEvaluating atomicity for task: {task.title}/n")
#             evaluation = await tech_lead.evaluate_task_atomicity(task.title)
#             is_truly_atomic = evaluation.value.is_atomic if evaluation.value else False


#         if contains_forbidden or not is_truly_atomic:
#             vague_tasks_to_expand.append(task)

#     return vague_tasks_to_expand