# Reconcile layout PR 2

1. Compare merged main with the feature baseline and preserve the published layout tree.
2. Merge main without rewriting published commits; retain relocated evidence and tests only at their declared paths.
3. Run strict and catalog checks, Python and Node safety suites, and diff checks.
4. Push the verified merge and update PR 2 to describe only layout 2.0 changes. Leave it open for review; retain this checkout.
