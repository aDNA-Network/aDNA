# Local Notes

> **Fixture purpose**: triggers R1 (private path leakage — `what/local/*`). The path itself is the violation, not the content.

Arbitrary content here — the hook flags this file because its path matches the private-directory pattern, regardless of body.
