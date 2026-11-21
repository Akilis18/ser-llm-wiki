# Workflow graph and validation loops

## Graph A: Wiki construction

```mermaid
flowchart TD
    A[Select research paper] --> B[Discuss content and intended changes]
    B --> C[Extract claims and citations]
    C --> D{Source checks pass?}
    D -- No --> B
    D -- Yes --> E[Update linked Wiki pages]
    E --> F[Log ingest and run lint]
    F --> G{Wiki checks pass?}
    G -- No --> H[Repair or flag unresolved gaps]
    H --> F
    G -- Yes --> I{More sources?}
    I -- Yes --> A
    I -- No --> J[Ready for teaching queries]
```

## Graph B: Wiki-to-slides

```mermaid
flowchart TD
    A[Teaching goals] --> B[Outline]
    B --> C[Query Wiki]
    C --> D[Draft content with Wiki citations]
    D --> E{Claims verified?}
    E -- No --> F[Retrieve again or revise]
    F --> C
    E -- Yes --> G[Create HTML slides]
    G --> H[Test navigation/layout]
    H --> I{Tests pass?}
    I -- No --> J[Repair HTML]
    J --> H
    I -- Yes --> K[Publish and log]
```

## Loop versus graph
Graph: nodes/edges define possible operations and conditions. Loop: a repeated path inside the graph to improve or correct a failed step. Maintain state containing source IDs, known claims, retry counters, diagnostics, and outputs. Max 2 retries per validation failure; unresolved issues require explicit human review.

## Evidence for reflection
Log actual failure frequency by node, which validation moved earlier, and before/after run results. Never invent a failure history to satisfy grading criteria.
