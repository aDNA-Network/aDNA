---
type: note
created: 2026-09-07
updated: 2026-09-07
confidential: true
tags: [fixture, dirty, r5]
---

# Confidential Control (Fixture)

> **Fixture purpose**: triggers R5 (frontmatter `confidential: true`) in a **`.md`** file.
> Pairs with `test_confidential.yaml`, which carries the identical flag in a **non-`.md`** file.
> The two differ **only in extension**, so a run that flags this one and misses its sibling has
> located the extension predicate and nothing else. Both hook versions must flag *this* file —
> a miss here is a HARNESS BUG, not a rule finding.
