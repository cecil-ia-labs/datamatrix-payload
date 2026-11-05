# Quad-Dimensional DataMatrix: Scope and Limitations

[Português](pt/scope-and-limitations.md)

This section collects the qualifications for the RfD. The mathematical argument and the app proposal can therefore be read without repeating them in each section.

1. **Status.** This is a request for discussion, with a working prototype and reproducible examples. Interoperability, framing, key management, state renewal, and a service-verification protocol remain design questions.
2. **Four dimensions.** The four axes are logical coordinates in a catalogue. A dense matrix selects one dimension identifier at each position and temporal state. The $64^4$ catalogue size and the selected payload bit count describe different objects.
3. **Hexadecimal values.** Hexadecimal is the sole public palette and code representation. GIF89a defines the internal container serialization. Writing a value in hexadecimal does not add entropy to it.
4. **Working profile.** The prototype accepts complete opaque 256 × 256 pixel frames, 4 × 4 identical indexed pixels per effective module, and power-of-two palettes of 2 to 64 entries. It preserves up to 64 frames, including identical states. The original payload length is supplied by the caller. Container metadata, authentication fields, and redundancy are outside the gross payload budget.
5. **Timing.** The 8 fps example is a nominal playback cadence, quantized to GIF delay units. The app cadence is independent; the example defaults to one state per minute. These values do not measure network transfer speed or model-generation throughput.
6. **App and authentication.** The viewer uses public synthetic states and copies a selected module's six-character color. A 64-entry palette supplies at most 64 color alternatives per state; the six-character display width does not measure authentication strength. It demonstrates selection and clipboard behaviour. Confidentiality, derivation, expiry, rate limiting, challenge binding, cycle renewal, and replay handling require a separately reviewed design. TOTP and AEAD are references for that discussion.
7. **Unicode.** The scalar domain has 1,112,064 values. Assigned characters, grapheme clusters, UTF-8 octets, scalar values, palette entries, and secret keys are distinct units. One-to-one hexadecimal mappings are candidates for representation or dictionary design. Palette cardinality, ordering, repeated characters, and dictionary storage must be accounted for in a text transport.
8. **Clipboard retention.** The 30-second cleanup is best effort and requires browser permission and page focus. It checks current text before writing; the API has no atomic compare-and-clear operation. Clipboard history and copies held by other applications are outside its control. Retention is separate from code expiry and the receiving service's acceptance rules.
9. **Evidence.** The case study validates exact recovery in the stated digital profile. The work does not make performance claims for generative models or physical capture. The later specification may adopt a different profile after discussion.

References: [GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), [Unicode §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/), [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html), [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html), [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html).

## Reading the distributed artifacts

The current app contains 16 public states, giving a 16-minute default interaction cycle. The 64-state profile is the supported maximum. The interface recordings use a separate presentation palette and geometry; recovery measurements use the exact indexed case-study file. The [release notes](release-notes.md) and [deposit guide](publication.md) preserve these distinctions.
