# Project: Lincan-Travel-Assistant-Agent

## Task Boundaries
<!-- 任务边界约束：大模型不会自动扩展需求，严格遵循以下边界 -->
- Each task MUST be a single, small, atomic unit of work
- Each task MUST be verifiable (answer "is this done?" with yes/no)
- After completing each task, call the **vibe_checkpoint** tool
- Do NOT expand scope beyond the current task without user approval
- Read `docs/vibe/tasks/active.md` at the start of each session

## Current Focus
<!-- TASK: learning-phase-1 -->
- 系统学习 Aligo 商旅助手项目
- 按 learning plan 逐课推进
- 每课产出 Learning 笔记并 push

## Constraints
<!-- 项目约束 -->
- 这是学习项目，注重理解而非产出
- 每课笔记需包含：概念解析 + 代码示例 + 动手任务 + 三语对比
- 使用中文回答和注释
- 函数级注释

## Conventions
<!-- 项目约定 -->
- 笔记保存到 Learning/ 目录
- 动手代码保存到 learning_challenges/ 目录
- 使用 conventional commits 格式

