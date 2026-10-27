# Rule grammar

## Shape

Use `TRIGGER → ACTION → OBJECT/OUTCOME → FAILURE OR EXCEPTION` where those parts matter. Example: “When changing generated schema types, run the package's existing code generator; if unavailable, report the missing prerequisite and preserve generated files.” A short prohibition may stand alone when no permitted alternative exists.

Prefer the smallest instruction that expresses the required behavior. Keep scope, accepted exceptions and necessary detail; a model-specific preference for brief instructions does not repeal a user requirement.

## Retention tests

1. Purpose: identify the requirement, accepted decision, preference, obligation or concrete mistake the line protects. Lack of a past incident does not invalidate proactive controls.
2. Scope: distinguish an acceptance criterion from an effort mandate. Reuse already-required evidence rather than adding a check to make every sentence measurable.
3. Authority: compare equivalent obligations and precedence; preserve the policy's owner and runtime-specific differences.
4. Enforcement honesty: “must” or “mandatory review” describes a normative requirement. “The hook blocks every violation” claims technical coverage and requires inspection of its binding, predicate and event. A prose prohibition can be binding without technically preventing an action.

## One owner per effective chain

Consolidate repeated general policy in the actual loaded chain and leave a short conditional pointer to detailed procedures. Separate runtime mirrors may need the same portable policy; file equality alone does not prove duplicate loading. An imported split reduces source-file size, not loaded context.

## Origins and examples

Valid origins include accepted product decisions, user preferences, external obligations, proactive safety analysis, architecture boundaries, reviews and observed regressions. Unknown origin is a question for review, not automatic deletion. An admitted empirical comparison uses the canonical verification policy; ordinary rewrites use static evidence.

Before: “Any uncertainty requires stopping.” After: “Ask when the answer changes scope, authority, data or external effects; resolve routine reversible choices from relevant conventions.” Preserve a stricter user-required approval boundary where it applies.

Before: “Verify thoroughly again after all tests pass.” After: delete the duplicate obligation or bind it to the existing named acceptance check. Add another check only for a specific unresolved criterion.
