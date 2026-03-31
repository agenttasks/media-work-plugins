# Dispatch a content pipeline task to agent teams

Dispatch a content pipeline task for processing. This command:

1. Validates the task parameters
2. Selects the appropriate agent team topology
3. Dispatches subtasks to teammates
4. Monitors progress and reports status

## Usage

```
/media-operations:dispatch-task [task-type] [--platform <platform>] [--priority <P0|P1|P2>]
```

## Task Types

- `generate-content` - Parse CHANGELOG and generate content briefs
- `run-experiment` - Create or analyze A/B experiments
- `publish` - Execute scheduled publishing pipeline
- `review` - Review pending content or requirements

## Examples

```
/media-operations:dispatch-task generate-content --priority P0
/media-operations:dispatch-task publish --platform instagram
/media-operations:dispatch-task review
```
