# Removable Media Security

## Purpose

Removable media can contain personal, sensitive, confidential, or authentication-related information independently of the main electronic device.

EcoShield uses removable-media security guidance to help users identify, remove, sanitize, retain, or responsibly handle removable storage and communication media before a device is sold, donated, reused, repaired, recycled, or disposed of.

---

# What Is Removable Media?

Removable media refers to storage or communication components that can be physically separated from a device.

Common examples include:

- SIM cards
- microSD cards
- SD cards
- USB flash drives
- external HDDs
- external SSDs
- memory cards
- removable storage modules

These components should be considered separately from the device's internal storage.

---

# Why Removable Media Matters

Users may correctly reset or erase a device but accidentally leave removable media inside it.

This can create a privacy or cybersecurity risk.

For example:

Smartphone
    ↓
Factory Reset Performed
    ↓
Personal Data Removed From Internal Storage
    ↓
microSD Card Still Installed
    ↓
Photos / Documents May Still Exist
    ↓
Potential Data Exposure

Therefore:

**Device sanitization does not automatically mean removable-media sanitization.**

---

# EcoShield Assessment Context

The primary EcoShield field associated with this document is:

`sim_memory_card_removed`

However, removable-media recommendations may also depend on:

- `device_type`
- `operating_system`
- `storage_type`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `encryption_enabled`
- `intended_disposal_method`

These fields help determine the seriousness and relevance of removable-media risks.

---

# SIM Card Security

## What Is a SIM Card?

A SIM card is used by mobile devices to connect to a cellular network and associate the device with a subscriber or mobile service.

Depending on the device, a SIM-related configuration may be:

- physical SIM
- eSIM
- dual SIM
- physical SIM + eSIM

SIM handling should therefore be considered separately from normal device storage.

---

## Why Remove a Physical SIM?

Before permanently transferring a mobile device, the user should check whether a physical SIM card is installed.

A physical SIM should normally not be unintentionally transferred with the device.

The user may need to:

1. remove the SIM
2. retain it
3. transfer it to another device
4. return it to the service provider
5. otherwise handle it according to provider requirements

EcoShield should not assume that a factory reset physically removes or deactivates a SIM card.

---

# eSIM Considerations

Some devices use an embedded SIM rather than a removable physical SIM.

An eSIM cannot simply be removed from the device like a physical card.

Therefore, when a device uses eSIM technology, EcoShield should avoid giving instructions such as:

"Remove the SIM card"

without considering the platform.

Instead, platform-specific account and cellular-plan guidance may be required.

The user may need to review:

- cellular plans
- device associations
- carrier instructions
- manufacturer instructions

Exact steps vary by device, operating system, and mobile provider.

---

# SD and microSD Card Security

SD and microSD cards can contain significant amounts of user information.

Examples include:

- photos
- videos
- documents
- downloads
- application files
- backups
- media
- exported data

A device factory reset may not necessarily sanitize removable memory cards.

Therefore, these cards should be reviewed separately.

---

# Example Risk Scenario

Consider:

Device Type:
Android Smartphone

Personal Data:
Yes

Sensitive Data:
Yes

Factory Reset:
Yes

Secure Erase:
Yes

SIM / Memory Card Removed:
No

Intended Action:
Sell

The device may appear ready for transfer because its internal storage has been sanitized.

However:

microSD card remains installed
        ↓
Stored files may remain
        ↓
New owner receives the card
        ↓
Previous information may be exposed

EcoShield should therefore identify the removable media as an unresolved security issue.

---

# Factory Reset vs Removable Media

A factory reset primarily affects the device according to the operating system and manufacturer implementation.

It should not automatically be interpreted as proof that all removable media has been sanitized.

EcoShield should reason about these separately:

Internal Device Storage
        ↓
Reset / Sanitization

Removable Media
        ↓
Separate Review / Removal / Sanitization

This separation improves the reliability of the security assessment.

---

# Secure Erasure and Removable Media

If removable storage contains sensitive information and will not remain with the user, appropriate sanitization should be considered.

The suitable sanitization approach depends on:

- media type
- media condition
- sensitivity of information
- intended reuse
- encryption status
- ability to access the media

EcoShield should retrieve more detailed guidance from:

`secure_data_erasure.md`

and:

`storage_media_sanitization.md`

when technical sanitization guidance is required.

---

# Removable Media Before Selling

Selling normally transfers the device permanently to another person.

Before selling a device, users should check for:

- physical SIM cards
- SD cards
- microSD cards
- USB storage
- external storage connected to the device
- other removable memory

A general process is:

Identify Removable Media
        ↓
Back Up Required Information
        ↓
Remove Media
        ↓
Retain or Sanitize Media
        ↓
Verify Device
        ↓
Transfer Ownership

---

# Removable Media Before Donation

Donation also represents a permanent ownership transfer.

The same removable-media precautions that apply to resale generally apply to donation.

Users should avoid unintentionally donating storage containing personal information unless the media has been appropriately sanitized and is intentionally included.

---

# Removable Media Before Recycling

Before recycling an electronic device, removable media should be checked.

Where possible:

1. identify removable media
2. remove it
3. determine whether it will be reused
4. sanitize it appropriately if required
5. recycle it through an appropriate channel if it is no longer usable

A damaged main device does not necessarily mean that its removable media is damaged or unreadable.

---

# Removable Media Before Repair

Repair differs from permanent transfer.

The device is normally expected to return to the same owner.

Users should still review removable media before giving the device to a repair provider.

Where appropriate, removable media that is not required for the repair can be retained by the owner.

This can reduce unnecessary exposure of stored information.

EcoShield should not automatically recommend destroying or permanently sanitizing removable media for ordinary repair scenarios.

---

# Inaccessible Devices

If:

`device_accessible = No`

the user may not be able to inspect the device through the operating system.

However, removable media may still be physically accessible.

For example:

Broken Smartphone
        ↓
Screen Cannot Be Used
        ↓
Device Data Cannot Be Reviewed
        ↓
microSD Card Can Still Be Removed

Therefore, EcoShield should distinguish between:

- logical device accessibility
- physical removable-media accessibility

---

# Devices That Cannot Power On

If:

`can_power_on = No`

software-based procedures may not be possible.

However, the user should still consider whether removable components can be safely removed.

A device that cannot power on should never automatically be considered free of sensitive information.

---

# Unknown Removable-Media Status

If:

`sim_memory_card_removed = Unknown`

or the user is unsure whether removable media exists, EcoShield should treat this as an uncertainty.

The system should recommend checking the device before permanent transfer.

Example:

"Verify whether the device contains a physical SIM, SD card, microSD card, or other removable storage before transferring ownership."

The system should not claim that removable media is present unless that information is known.

---

# Not Applicable Cases

Some devices may not contain removable media.

For example, certain devices may have:

- only soldered internal storage
- no memory-card slot
- eSIM only
- no cellular functionality

In these situations, removable-media guidance may not be applicable.

EcoShield should avoid generating unnecessary warnings when removable media genuinely does not apply.

---

# Encryption and Removable Media

Encryption of the main device does not necessarily mean that removable storage is encrypted.

For example:

Internal Storage
    → Encrypted

microSD Card
    → Encryption Status Unknown

Therefore:

`encryption_enabled = Yes`

should not automatically cause EcoShield to assume that every removable storage device is protected.

The actual protection depends on how the removable media was configured.

---

# Backup Considerations

Before sanitizing removable storage, users should determine whether important information needs to be retained.

A safe sequence is:

Identify Required Information
        ↓
Create Backup
        ↓
Verify Backup
        ↓
Sanitize or Retain Media
        ↓
Verify Final State

EcoShield should avoid recommending irreversible erasure before necessary backup considerations have been addressed.

---

# Privacy-by-Design Principle

EcoShield should determine only the security status of removable media.

The application should never ask users to upload or provide:

- SIM credentials
- personal photos
- personal documents
- stored files
- authentication data
- passwords
- PINs
- encryption keys
- private information stored on the media

EcoShield needs to know the **condition and status**, not the contents.

---

# RAG Retrieval Guidance

This document should receive high retrieval relevance when queries contain terms such as:

- SIM
- SIM card
- eSIM
- memory card
- microSD
- SD card
- removable media
- removable storage
- USB
- external storage
- phone transfer
- device resale
- device donation

It should also be retrieved when:

`sim_memory_card_removed = No`

or:

`sim_memory_card_removed = Unknown`

and the intended action involves transferring or disposing of the device.

---

# RAG Combination Example

Consider:

Device Type:
Smartphone

Operating System:
Android

Contains Sensitive Data:
Yes

Factory Reset:
Yes

SIM / Memory Card Removed:
No

Intended Disposal Method:
Donate

Relevant retrieval may include:

Platform Security Guidance
        +
Removable Media Security
        +
Secure Device Transfer
        +
Secure Data Erasure

The LLM can then generate a recommendation grounded in several relevant knowledge sources rather than relying on a single document.

---

# EcoShield Decision Context

Removable-media guidance is primarily associated with:

- `device_type`
- `operating_system`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `encryption_enabled`
- `sim_memory_card_removed`
- `intended_disposal_method`

The most directly relevant field is:

`sim_memory_card_removed`

---

# EcoShield Recommendation Principle

EcoShield should treat removable media independently from the main device storage.

The reasoning process should follow:

Device
   ↓
Does Removable Media Apply?
   ↓
Yes
   ↓
Has It Been Removed or Reviewed?
   ↓
No / Unknown
   ↓
Evaluate Data Sensitivity
   ↓
Evaluate Intended Action
   ↓
Recommend Removal, Verification,
Retention, Sanitization, or
Appropriate Handling

The system should never assume that:

Factory Reset
    =
All Storage Sanitized

Instead:

Factory Reset
    +
Internal Storage Status
    +
Removable Media Status
    =
More Complete Transfer Assessment

---

# Example EcoShield Recommendation

## Situation

- Device: Android smartphone
- Personal data: Yes
- Sensitive data: Yes
- Factory reset: Performed
- Secure erase: Performed
- SIM / memory card removed: No
- Intended action: Sell

## Recommendation

**Priority: High**

Remove and review any physical SIM or removable memory card before transferring the device.

**Why:**

The device's internal storage may have been reset or sanitized, but removable media can retain information independently and may be transferred unintentionally to the next owner.

---

# Keywords

removable media, removable storage, SIM card, physical SIM, eSIM, SD card, microSD card, memory card, USB drive, external storage, external SSD, external HDD, data exposure, device transfer, smartphone security, mobile security, factory reset, secure erase, sanitization, recycling, resale, donation, repair