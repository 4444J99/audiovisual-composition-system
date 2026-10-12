# Helper buildup investigation — 2026-10-12

Status: reproducible runtime buildup observed; root fix and original-media custody remain incomplete. Owner: Codex desktop/app-server MCP discovery and loaded-thread runtime lifecycle. Local acceptance/custody checkpoint owner: audiovisual-composition-system PR #3.

## Live observations

After the authorized app restart, the primary bundled app-server PID was 36050. During a 20-second sample its direct helper children grew from 208 to 259: 51 creations and zero exits. Additions comprised 18 DomusAgentHost processes, 12 SkyComputerUseClient processes, 12 Node processes, three 1Password MCP servers, three GitHub MCP servers and three node_repl processes. This is three matching 17-process groups. A later lsof snapshot found 2,742 pipe descriptors on the primary process. Sampled stdio helpers remain connected to live parents; they are not proven abandoned.

Desktop log aggregates since restart showed 85 global mcpServerStatus/list responses and 84 discovery errors each for limen-runtime and netlify. Limen reports that its configured bearer-token environment variable is absent; Netlify reports authentication required. Log bodies, credentials, personal chat content and account identifiers were not committed. Authentication failure and repeated status calls coexist with growth; the sample does not prove that either auth failure alone causes the retained groups. Loaded chats and native runtime retention are a competing explanation.

Swap remained above admission: samples included 8,278.25 MiB and 8,344.81 MiB versus the 4,096 MiB threshold. No unchanged heavy-acquisition retry or media payload I/O occurred. The configured updater reports installed app 26.1007.30912, build 20156, prod channel, up_to_date; this is the configured update channel, not proof no fix exists on another channel.

## Ownership and repair boundary

The live direct helpers originate beneath the bundled Codex app-server. Domus's ensure wrapper validates an inherited stable-identity lifetime pipe before either exec or native supervision; its native supervisor deliberately retains descendant lifetime and forwards cancellation. No disconnected-pipe or abandoned-parent evidence justified changing that behavior or terminating individual helpers. The effective MCP configuration includes both managed and app-managed entries. No deployed config, native bundle, helper binary, credential, plugin enablement or host-admission threshold was changed.

Related upstream reports describe repeated global full status requests and MCP helper recreation ([38171](https://github.com/openai/codex/issues/38171), Linux unofficial packaging), and passive-chat loading with retained MCP groups ([20867](https://github.com/openai/codex/issues/20867), Windows). Those are corroborating reports on other platforms, not proof of the exact macOS implementation defect or an available fixed release.

## Concrete fix and acceptance criteria

The app owner needs to distinguish global status discovery from starting a fresh loaded-thread MCP fleet; reuse or explicitly release temporary connection managers, coalesce concurrent discovery requests, and bound inactive runtime ownership. Authentication errors need bounded retry/backoff rather than repeated full fleet startup. Repair missing desktop credential delivery through its owning source without copying credentials into config, and diagnose Netlify's existing grant before requesting consent. Neither workaround may disable declared tools or evict active work merely to reduce counts.

Acceptance: repeated read-only global status discovery without opening chats or starting turns must stop adding retained helper groups; temporary groups must exit and their descriptors must close. Opening then leaving a passive chat must have a documented, measured runtime release boundary. Existing active chats and full MCP tool capability must continue working. Observe stable swap <=25% and VITALS outside shed, then acquire a real persistent runner heavy lease and resume the committed original-media plan within the cumulative budget. An idle process, a restart, or one low swap sample does not satisfy this predicate.

No verified local source fix was found or deployed. The evidence is preserved for review instead of applying an unverified vendor-bundle patch. Originals and existing custody copies remain retained; PRs #2 and #3 remain open.
