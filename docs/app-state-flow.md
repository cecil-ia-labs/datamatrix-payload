# Quad-Dimensional DataMatrix: app-held state selection

[Português](pt/app-state-flow.md) · [Scope and Limitations](scope-and-limitations.md)

The **application holds the sequence**. The user selects a state and supplies its code to a service or website. The service is the consumer or verifier; it does not need to render the sequence.

| Stage | App | User or receiving service |
|---|---|---|
| Load | Load the local sequence and its state-to-code mapping | Wait for a selected code |
| Advance | Display the next state at the chosen cadence | Observe or request a state |
| Click | Freeze the displayed state and select its module | Select the current state |
| Copy | Copy six uppercase hexadecimal characters, without a leading `#` | Receive a value such as `F519DA` |
| Highlight | Outline the matrix with that color for 2.5 seconds | See which color was selected |
| Paste | Read the clipboard after a click or tap on the receiver circle | Fill the circle with the matching color and show success |
| Resume | Continue the local sequence on request | Choose another state later |

The transport example uses eight frames per second. The interaction example defaults to one state per minute. A 64-state sequence takes eight seconds at 8 fps or 64 minutes at one state per minute.

The distributed viewer loads **16 synthetic states**. Its actual cycle is two seconds at 8 fps or 16 minutes at the default cadence. The 64-state cycle describes the maximum supported profile. The [recorded PoC](media/README.md) shows the interface, while the [case-study GIF](../examples/quad-dimensional-datamatrix-16-states.gif) is the data-bearing container.

## Choosing the code

The viewer copies the selected module's hexadecimal palette entry. The complete state remains available to the transport decoder; copying a color does not copy that payload.

| Selection rule | Coordinates | Status |
|---|---|---|
| First module | `(0, 0)` | Default in the viewer |
| Last module | `(63, 63)` | Available in Code source |
| Explicit coordinates | User-selected `(x, y)`, both from 0 to 63 | Available in Code source |
| Coordinates declared at the start of the matrix | For example, the first two dimension indices encode `x` and `y` | RfD candidate; not implemented |

Coordinates refer to the effective 64 × 64 module grid, with the origin at the top left. The generator records the module indices and palette as hexadecimal values, so the viewer reads the same color as the indexed GIF.

The local viewer renders each state as an independent GIF. Clicking stops the app timer before copying. The large payload console is removed. If direct copying is unavailable, a small field reveals only the six-character code for manual copying. If reading the clipboard is blocked, a native-paste/input field is offered. The receiving circle accepts an optional leading `#` and either letter case, normalizes the text, and reports success only for a match with the latest selection.

## Clipboard retention

A successful copy schedules cleanup for 30 seconds later. A new copy restarts that interval. Cleanup checks the current clipboard text and attempts to clear it only when it still matches the code written by the app.

Automatic cleanup requires a focused, visible page and already-granted read permission. The timer never opens a permission prompt. When the page is in the background, it retries on return. If the browser blocks cleanup, a clear action is offered; that action also checks the current contents before writing.

This is best-effort clipboard retention, rather than code expiry or a receiving-service acceptance rule. The browser provides no atomic compare-and-clear operation; clipboard history and copies in other applications remain outside the page's control. These boundaries are collected in [Scope and Limitations](scope-and-limitations.md).

The analogy with [TOTP, RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html) concerns an app-held evolving state and a receiving verifier. It does not require the sequence to follow TOTP's derivation.

Clipboard reference: [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/).
