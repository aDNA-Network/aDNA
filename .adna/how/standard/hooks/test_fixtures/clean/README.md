# Example Project

This is a minimal README — innocuous content used by the pre-push-sanitize hook's self-test as a clean fixture. Contains no private paths, no secret patterns, no flagged frontmatter.

## What this fixture proves

When the hook scans this file, it should produce **zero findings** across R1-R7. If the hook flags this file, the rule logic has a false-positive defect.
