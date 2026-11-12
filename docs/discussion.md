<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT

Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix

AI-assisted development:
OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration.
No OpenAI sponsorship, affiliation, or endorsement is implied.

License: See the repository LICENSE file and SPDX identifier above.
-->

# Quad-Dimensional DataMatrix: discussion agenda

[Português](pt/discussion.md) · [Scope and Limitations](scope-and-limitations.md)

The RfD invites discussion of the following choices. The working prototype supplies examples rather than normative answers.

| Topic | Questions |
|---|---|
| Four-coordinate catalogue | Which applications need a catalogue address, a dense state, or a sparse event? |
| Hexadecimal dictionary | Should a dimension name a palette entry, a Unicode scalar, an external key entry, or a derived code? |
| Unicode | Should text use UTF-8 octets, a four-dimension scalar mapping, or an adaptive dictionary with at most 64 active entries per state? |
| Sequence ownership | How is the app-held sequence provisioned, renewed, and associated with a receiving service? |
| Selection | Should a click freeze until explicit resume, until consumption, or until a new challenge? |
| Cadence | Which use cases need 8 fps, one state per minute, or a user-driven advance? |
| Clipboard | The viewer uses a six-character selected color. Should selection use the first module, the last, explicit coordinates, or coordinates declared in the matrix header? |
| Authentication | How should a selected state be bound to a session, a challenge, or an acceptance window? |
| Framing | Where should payload length, version, state identity, and integrity data live? |
| Evidence | Which later experiments would decide between candidate mappings? |

The Unicode proposal is particularly concrete: every scalar has a unique hexadecimal integer. That integer fits into the 24-bit four-coordinate catalogue or four six-bit dimension identifiers. The RfD asks which interpretation is useful as an entry in the eventual key or dictionary.

The [0.2.0 release notes](release-notes.md) delimit the implemented study and app behaviour. The [deposit guide](publication.md) prepares this RfD as a technical report with reproducible supporting material; the discussion questions remain open.
