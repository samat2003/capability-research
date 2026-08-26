# Manuscript

The publication manuscript is [`main.tex`](main.tex); references are in [`references.bib`](references.bib).

A standard BibTeX build is:

```bash
cd paper
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The manuscript intentionally distinguishes:

- ordered empirical recoverability `E_k` from standard unbiased `pass@k`;
- selected-from-eight accuracy (`selected@8`) from ordinary one-sample benchmark accuracy;
- diagnostic hidden-state signal from causal control;
- internal mechanically verified experiments from the final public HumanEval+ transfer.

No benchmark-SOTA claim is made. The paper should be read together with [`../docs/AUDIT.md`](../docs/AUDIT.md) and [`../docs/STATISTICAL_CORRECTION.md`](../docs/STATISTICAL_CORRECTION.md).
