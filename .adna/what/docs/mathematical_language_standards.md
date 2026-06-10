---
type: context
title: "Mathematical Language Standards for aDNA Documentation"
created: 2026-03-01
updated: 2026-03-01
status: approved
last_edited_by: agent_init
tags: [adna, standards, mathematical_language, documentation]
---

# Mathematical Language Standards

Guidelines for using mathematical language in aDNA documentation. Mathematical framing should clarify, not obscure.

## Rules

1. **Analogy must be labeled.** When mathematical terms are used analogically (not literally), mark them explicitly: "analogous to projection," "can be modeled as," "informally similar to." Never present an analogy as an identity.

2. **Name it for what it is.** Use the simplest correct term. If the structure is a finite chain of nested sets, call it a "finite refinement chain" — not a "convergent series." If a function selects a subset, call it a "selection function" — not a "projection operator."

3. **Axiom check before naming.** Before using a mathematical term (Hilbert space, norm, basis, orthogonal), verify the structure satisfies the term's axioms. A Hilbert space requires an inner product and completeness. A norm requires a vector space and homogeneity. If the axioms aren't met, either (a) use a weaker term that fits, or (b) explicitly note the analogy is informal.

4. **Two-layer structure.** For audiences that include both practitioners and theorists, use operational language in the main text and provide precise mathematical backing in a callout or appendix. The operational layer should stand alone without the math.

5. **Empirical claims over theoretical claims.** "Token counts decrease from 500K to 5K across four levels" is verifiable and unassailable. "The working set converges" imports infinite-sequence semantics that don't apply. Prefer the empirical statement.

6. **Convention vs. structure.** When a property depends on agent compliance (governance isolation, naming conventions), describe it as a convention or design rule — not as a structural property. "Governance is designed not to cross boundaries" is correct. "Governance does not leak" sounds like a theorem.

7. **Cite when claiming formalism.** If a claim is grounded in established mathematics or literature, cite it explicitly and show the mapping. Formal claims should reference the source and demonstrate that the structure satisfies the required properties.

---

## Origin

These standards emerged from the M03 Mathematical Precision Audit (campaign_adna_lattice), which catalogued 42 mathematical claims across 13 files. The audit found 16 precise, 18 imprecise, 7 hand-wavy, and 1 incorrect claim. These rules codify the patterns that distinguished precise claims from imprecise ones.

## See Also

- `context_prompt_engineering_convergence_model.md` — primary application of these standards
- `context_adna_core_convergence_model.md` — operational quick-reference applying two-layer structure
