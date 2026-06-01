from neural_forge_app.ai_service.agents.pm_agent.models import Task

def splice_and_remap_tasks(
    plan_tasks: list[Task], 
    vague_task: Task, 
    new_sub_tasks: list[Task]
) -> list[Task]:
    """
    Replaces a vague task with new atomic sub-tasks, dynamically remapping
    all upstream and downstream dependencies to maintain graph integrity.
    """
    
    # 1. Find the highest existing task_id to generate safe new unique IDs
    max_existing_id = max([t.id for t in plan_tasks], default=0)
    
    # Dictionary to map the LLM's temporary/dummy IDs to our new global IDs
    id_mapping = {}
    new_global_ids: list[int] = []

    # 2. Assign new global IDs to the newly generated sub-tasks
    for sub_task in new_sub_tasks:
        max_existing_id += 1
        id_mapping[sub_task.id] = max_existing_id
        sub_task.id = max_existing_id
        new_global_ids.append(max_existing_id)

    # 3. Fix internal dependencies for the new sub-tasks & inherit upstream dependencies
    original_upstream_deps = vague_task.dependencies

    for sub_task in new_sub_tasks:
        # Map any dummy dependencies the LLM generated to their new global IDs
        updated_internal_deps : list[int] = [
            id_mapping[dep] for dep in sub_task.dependencies if dep in id_mapping
        ]
        
        # The sub-task must ALSO wait for whatever the original vague task was waiting for
        combined_deps = updated_internal_deps + original_upstream_deps
        
        # Deduplicate and update
        sub_task.dependencies = list(set(combined_deps))

    # 4. Update downstream dependencies in the rest of the plan
    vague_id = vague_task.id
    
    for task in plan_tasks:
        if vague_id in task.dependencies:
            # Remove the old vague task ID
            task.dependencies.remove(vague_id)
            
            # Make the downstream task depend on ALL the newly generated sub-tasks.
            # (Waiting for all sub-tasks ensures the whole "epic" is done before proceeding).
            task.dependencies.extend(new_global_ids)
            
            # Deduplicate
            task.dependencies = list(set(task.dependencies))

    # 5. Remove the vague task and insert the new sub-tasks
    updated_plan = [t for t in plan_tasks if t.id != vague_id]
    updated_plan.extend(new_sub_tasks)

    # Optional: Sort by task_id for readability in debugging
    updated_plan.sort(key=lambda t: t.id)

    return updated_plan