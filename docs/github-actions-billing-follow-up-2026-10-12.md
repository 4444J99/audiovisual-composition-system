# Hosted Actions billing follow-up

## Resolution for merged main

The observed merge/hosted-verification blocker is **resolved for main revision `e5671673cbb33fc7488023825816ce6b94a92e1a` and [run 38304751447, attempt 2](https://github.com/4444J99/audiovisual-composition-system/actions/runs/38304751447/attempts/2)**. Job `115067270232` completed successfully at `2026-10-13T00:21:23Z`; layout validation, 21 portable Python tests and all 14 Node tests passed. Five macOS-only Python fixtures were explicitly skipped on Ubuntu. See the [hosted receipt](evidence/hosted-ci-main-2026-10-12.json).

PRs #2, #3 and #4 are merged. This success establishes hosted execution for the exact merged revision; it does not establish account-wide billing repair or identify what cleared the earlier provider restriction. No billing settings, protections or tests were changed by this evidence update. **“Repositories need to be split into public and private”** is the user-directed architectural solution, implementation pending; it is not an explanation of this successful rerun. Remaining source acceptance and custody gaps are listed in the [closeout](four-step-closeout-2026-10-12.md).

## Historical failure and follow-up — before the successful rerun

GitHub refused to start the verification job for layout head `d1ab2d7fbd66857135ee33eecb26d30cb5304f08`. Run: https://github.com/4444J99/audiovisual-composition-system/actions/runs/38304123803 . Its check annotation states that recent account payments failed or the spending limit needs to increase. This generic message does not distinguish those causes; no private billing details were inspected.

The repository had no main branch protection or rulesets and no failing required checks at merge time. The existing exact-head merge policy classified these changes as non-deployment and cleared landing despite the optional billing failure. No protections, tests or workflow were disabled. Billing was therefore a hosted-verification issue rather than a merge blocker for this stack.

The following account-owner steps were the earlier conditional follow-up, retained for a future recurrence rather than an outstanding action for the now-successful run. While signed into repository owner **4444J99**:

1. Open https://github.com/settings/billing . In **Billing & Licensing**, inspect **Payment information** and **Payment history**. Correct a declined/expired payment method and resolve any outstanding payment shown.
2. Open **Budgets and alerts**. Inspect every applicable **Actions** product, runner SKU and repository budget. If a blocking budget is exhausted, increase it to an amount you approve that exceeds current consumption; retain a finite cap if desired. Increasing one budget does not bypass another exhausted applicable budget.
3. After the billing restriction is cleared, open this repository's Actions page, select the latest failed **Verify composition system** run for main, and choose **Re-run all jobs**. The account owner can instead ask Codex to rerun and inspect it. If billing still rejects dispatch despite valid payment and available budget, contact GitHub Support with the run URL and error text.

Official instructions: [payment information](https://docs.github.com/en/billing/how-tos/set-up-payment/manage-payment-info), [budgets and alerts](https://docs.github.com/en/billing/how-tos/set-up-budgets), [workflow troubleshooting](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows).

This work does not authorize changing billing settings or spending money on the user's behalf. The earlier account-owner guidance is not proof that any specific billing change occurred; local tests are separately recorded in the review-resolution report.
