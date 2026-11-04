# Quad-Dimensional DataMatrix: app-held state selection

[Português](pt/app-state-flow.md) · [Scope and Limitations](scope-and-limitations.md)

The **application holds the sequence**. The user selects a state and supplies its code to a service or website. The service is the consumer or verifier; it does not need to render the sequence.

| Stage | App | User or receiving service |
|---|---|---|
| Load | Load the local sequence and its state-to-code mapping | Wait for a selected code |
| Advance | Select the next displayed state at the chosen cadence | Observe or request a state |
| Click | Stop advancement and freeze the displayed state | Select the current state |
| Copy | Write the associated hexadecimal code to the clipboard | Paste or consume the code |
| Resume | Continue the local sequence on request | Choose another state later |

The transport example uses eight frames per second. The interaction example uses one state per minute. These are separate controls. A 64-state sequence takes eight seconds at 8 fps or 64 minutes at one state per minute.

The local viewer defaults to one state per minute. Its image is a standalone indexed GIF for the selected state, so pausing does not depend on stopping a browser's built-in animation. On click, the viewer clears its timer before copying. If direct clipboard access is unavailable, it selects the hexadecimal text for manual copying.

For the synthetic example, the copied code is the complete 3 KiB state payload, written as 6,144 hexadecimal digits. This is a concrete study convention. The service-facing code length and its relationship to a key remain RfD questions.

The analogy with [TOTP, RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html) concerns an app-held evolving state and a receiving verifier. The user interaction does not require that the sequence follow TOTP's particular derivation.

Clipboard reference: [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/).
