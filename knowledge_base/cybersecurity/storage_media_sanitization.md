# Storage Media Sanitization

## Purpose

Storage media sanitization is the process of reducing the possibility that previously stored information can be recovered from a storage device after it is reused, transferred, recycled, or disposed of.

EcoShield uses storage-media guidance to make more technically appropriate recommendations based on the storage type selected during assessment.

Different storage technologies behave differently.

Therefore:

**One sanitization method should not automatically be applied to every storage device.**

---

# Why Storage Type Matters

EcoShield currently recognizes storage types such as:

- HDD
- SSD
- eMMC
- Flash Storage
- Hybrid
- Unknown
- Not Applicable

These technologies may differ in:

- how information is stored
- how data is managed internally
- how deletion behaves
- how overwrite operations behave
- whether device-level secure-erase functions exist
- whether encryption is integrated
- how damaged media can be handled

Storage type should therefore influence sanitization guidance.

---

# EcoShield Assessment Context

The primary EcoShield field associated with this document is:

`storage_type`

Other related assessment fields include:

- `storage_capacity`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `encryption_enabled`
- `device_condition`
- `intended_disposal_method`

These values help determine which storage-related guidance is relevant.

---

# Sanitization Is Different From Normal Deletion

Normal file deletion typically removes the user's ordinary reference to a file.

That should not automatically be treated as storage sanitization.

Conceptually:

Delete File
    ↓
File Disappears
    ↓
Storage Location May Become Available
    ↓
Underlying Information May Still Exist
    ↓
Potential Recovery Risk

Therefore:

**Delete ≠ Sanitization**

---

# Sanitization Is Different From Formatting

Formatting prepares a storage device or filesystem for use.

Different formatting operations may behave differently.

Therefore:

**Format ≠ Automatically Secure Erasure**

EcoShield should avoid assuming that a generic "format" operation provides adequate sanitization for every device.

---

# Sanitization and Factory Reset

A factory reset is generally a device-level operation.

Storage sanitization focuses specifically on previously stored information.

EcoShield should therefore evaluate:

`factory_reset_performed`

and:

`secure_erase_performed`

separately.

A factory reset may be part of the overall preparation process, but storage-specific guidance may still be relevant.

---

# Sanitization and Encryption

Encryption can reduce the risk of unauthorized access to stored information.

However:

Encryption
    ≠
Automatic Proof of Sanitization

EcoShield should consider encryption together with:

- storage technology
- secure-erasure status
- reset status
- account security
- removable media
- intended action

On some modern systems, cryptographic key destruction may form part of a sanitization process, but the exact effect depends on implementation and platform.

EcoShield should not make universal claims without appropriate evidence.

---

# Hard Disk Drives — HDD

## What Is an HDD?

A hard disk drive stores information magnetically on rotating platters.

HDDs differ significantly from flash-based storage devices.

---

## HDD Sanitization Considerations

Historically, overwrite-based approaches have commonly been used with magnetic storage.

However, EcoShield should not prescribe one universal overwrite count or procedure.

The appropriate process depends on:

- device condition
- storage size
- data sensitivity
- intended reuse
- organizational requirements
- supported sanitization tools

EcoShield should prefer trusted sanitization guidance rather than outdated assumptions.

---

## HDD Reuse Scenario

If an HDD is healthy and intended for reuse:

1. back up required information
2. verify the backup
3. use an appropriate sanitization process
4. verify the result where practical
5. reuse or transfer the drive

This supports both security and sustainability.

---

## Damaged HDD

A damaged HDD may not respond to normal software-based sanitization.

If sensitive information exists and the drive cannot be sanitized normally, additional physical or professional handling may be appropriate.

EcoShield should clearly communicate the limitation rather than assuming the data is gone.

---

# Solid-State Drives — SSD

## What Is an SSD?

A solid-state drive stores information in flash memory rather than magnetic platters.

SSDs use internal controllers to manage storage.

These controllers may use mechanisms such as:

- wear leveling
- spare areas
- over-provisioning
- garbage collection
- remapping

These behaviors mean that HDD-oriented assumptions should not automatically be applied to SSDs.

---

## SSD Sanitization Considerations

Simple overwrite assumptions may be less reliable for SSDs because the storage controller decides where information is physically written.

Therefore, when supported, SSD-specific sanitization functions or platform-supported erase mechanisms may be more appropriate.

EcoShield should avoid telling users to repeatedly overwrite SSDs as a universal solution.

---

## SSD and Encryption

Many modern systems use encryption together with SSD storage.

Where properly implemented, encryption may strengthen the sanitization process.

However, EcoShield should not assume that:

`encryption_enabled = Yes`

means:

`secure_erase_performed = Yes`

These are separate assessment states.

---

## Damaged SSD

A damaged SSD may prevent normal software-based sanitization.

If sensitive information remains and the SSD cannot be accessed, the user may need a trusted handling or destruction process appropriate to the sensitivity of the data.

EcoShield should not claim that data is safe merely because the drive has failed.

---

# eMMC Storage

## What Is eMMC?

eMMC is embedded flash storage commonly used in:

- smartphones
- tablets
- lightweight laptops
- embedded devices

It is generally integrated into the device rather than designed to be removed like a traditional drive.

---

## eMMC Sanitization Considerations

Sanitization usually depends heavily on:

- the operating system
- manufacturer implementation
- device encryption
- device reset process
- accessibility of the device

EcoShield should combine this document with:

`platform_security_guidance.md`

when eMMC is selected.

---

## Inaccessible eMMC Device

If a device with eMMC storage cannot power on or cannot be accessed, software-based sanitization may be unavailable.

Because the storage is integrated, physical removal may also be difficult.

EcoShield should acknowledge this limitation and recommend an appropriate cautious handling or recycling path.

---

# Flash Storage

Flash storage may appear in:

- USB drives
- smartphones
- tablets
- embedded devices
- memory cards
- external devices

Flash storage shares some characteristics with SSDs, including internal controller behavior.

Therefore, simple HDD-style sanitization assumptions should not automatically be applied.

---

# USB Flash Drives

USB drives may contain independent copies of sensitive information.

Before reuse, resale, donation, or recycling, users should determine whether the drive:

- contains personal data
- contains sensitive data
- has been backed up
- requires sanitization
- is encrypted
- remains functional

USB drives should be treated as independent storage devices.

---

# Memory Cards

Memory cards include:

- SD
- microSD
- other removable flash media

They may contain:

- photos
- documents
- application data
- backups
- videos
- exported files

A reset of the main device should not automatically be treated as sanitization of the memory card.

EcoShield should combine this document with:

`removable_media_security.md`

when memory cards are relevant.

---

# Hybrid Storage

Hybrid storage combines characteristics of different storage technologies.

For example, a system may combine:

- HDD capacity
- flash acceleration
- multiple storage devices

EcoShield should avoid assuming that one sanitization process addresses every storage component.

The user may need to identify each storage component separately.

---

# Unknown Storage Type

If:

`storage_type = Unknown`

EcoShield should not invent a sanitization method.

Instead, the system should recommend identifying the storage technology before applying detailed technical guidance.

Example recommendation:

"Identify whether the device uses HDD, SSD, eMMC, flash storage, or another storage technology before choosing a sanitization method."

This is safer than providing potentially inappropriate instructions.

---

# Not Applicable

If:

`storage_type = Not Applicable`

storage-media sanitization may not be relevant.

For example, some devices may not contain meaningful user-controlled storage.

EcoShield should not generate unnecessary storage sanitization warnings in such cases.

---

# Accessible Storage

When:

`device_accessible = Yes`

and:

`can_power_on = Yes`

the user may be able to:

- identify storage technology
- back up data
- verify encryption
- use supported sanitization tools
- perform platform reset
- verify the result

This generally provides the best conditions for safe preparation.

---

# Inaccessible Storage

When:

`device_accessible = No`

normal software sanitization may not be possible.

EcoShield should not instruct the user to complete impossible software steps without acknowledging the limitation.

Instead, the system should consider:

- data sensitivity
- storage type
- device condition
- intended action
- whether professional handling is appropriate

---

# Storage That Cannot Power On

If:

`can_power_on = No`

the device may still contain recoverable data.

A storage device should not be considered safe simply because the host device does not start.

Relevant reasoning is:

Device Cannot Power On
        ↓
Software Sanitization Unavailable
        ↓
Storage May Still Contain Information
        ↓
Evaluate Data Sensitivity
        ↓
Choose Appropriate Handling

---

# Data Sensitivity and Sanitization Priority

Sanitization priority increases when sensitive information exists.

Example:

Storage:
SSD

Personal Data:
Yes

Sensitive Data:
Yes

Secure Erase:
No

Device Accessible:
Yes

Intended Action:
Sell

This scenario should receive strong sanitization guidance before ownership transfer.

---

# Backup Before Sanitization

Sanitization can permanently remove information.

Before sanitizing storage:

1. identify data that must be retained
2. create a backup
3. verify the backup
4. continue with sanitization

EcoShield should consider:

`data_backed_up`

before recommending irreversible actions.

---

# Storage Sanitization Before Selling

Selling permanently transfers storage to another person.

Before resale:

- back up required information
- verify storage type
- review encryption
- perform an appropriate sanitization process
- perform the relevant device reset
- verify final state
- handle removable media separately

Storage-specific guidance should be selected according to the actual media technology.

---

# Storage Sanitization Before Donation

Donation is also a permanent transfer.

A functional storage device may continue to be useful after appropriate sanitization.

This supports:

Secure Data Handling
        +
Device Reuse
        =
More Sustainable Donation

EcoShield should not recommend destroying reusable storage unnecessarily when secure reuse is possible.

---

# Storage Sanitization Before Recycling

Recycling may be appropriate when storage is no longer reusable.

However, sensitive data should still be considered.

A responsible sequence may be:

Evaluate Data
      ↓
Attempt Appropriate Sanitization
      ↓
If Not Possible
      ↓
Use Trusted Handling / Destruction
      ↓
Responsible Recycling

Recycling should not be represented as automatic proof of secure data destruction.

---

# Storage Sanitization Before Repair

Repair normally represents temporary transfer.

Complete storage sanitization may not always be necessary.

Instead, EcoShield should consider:

- sensitivity of the information
- whether storage access is needed
- whether a backup exists
- whether removable storage can be retained
- whether encryption is enabled

The recommendation should be proportional to the actual repair scenario.

---

# Storage Sanitization Before Reuse

If the same owner continues using the device, sanitization may not be required.

If the storage will be reassigned to another user, sanitization becomes more important.

EcoShield should distinguish:

Same User Reuse
        vs
Different User Reuse

---

# Reuse vs Destruction

From a sustainability perspective, destroying functional storage should not be the default response to security concerns.

A better sequence is:

Can Storage Be Safely Sanitized?
        ↓
       Yes
        ↓
Reuse / Donation / Resale
        ↓
Extended Useful Life

If:

Safe Sanitization Is Not Possible
        +
Sensitive Information Remains
        ↓
Trusted Destruction / Recycling May Be Appropriate

This balances security and sustainability.

---

# Sanitization Verification

Where practical, users should verify the result after sanitization.

Verification may include confirming that:

- previous files are no longer normally accessible
- previous user environment is removed
- accounts are no longer available
- the storage/device is prepared for its next use

EcoShield should not claim forensic verification.

The system only knows what the user reports.

---

# What EcoShield Should Not Recommend Universally

EcoShield should avoid blanket statements such as:

- overwrite every drive seven times
- one overwrite is always enough for every device
- SSDs should be treated exactly like HDDs
- formatting always sanitizes data
- factory reset always securely destroys data
- encryption always makes sanitization unnecessary
- broken drives contain no recoverable information

Technical recommendations should reflect the actual storage technology and available evidence.

---

# Authoritative Guidance Principle

Detailed sanitization procedures should ideally be grounded in:

- current manufacturer documentation
- operating-system documentation
- recognized sanitization standards
- organizational security policy
- certified recycling or destruction requirements where applicable

EcoShield's RAG architecture is intended to support this evidence-grounded approach.

---

# RAG Retrieval Guidance

This document should receive high relevance for queries involving:

- HDD
- hard drive
- SSD
- solid-state drive
- eMMC
- flash storage
- USB drive
- memory card
- storage wiping
- storage sanitization
- erase SSD
- erase HDD
- broken drive
- damaged drive
- storage disposal
- storage recycling

It should also receive strong relevance when:

`storage_type`

is known and:

`secure_erase_performed = No`

or:

`secure_erase_performed = Unsure`

---

# RAG Retrieval by Storage Type

## HDD

Retrieve:

Storage Media Sanitization
+
Secure Data Erasure
+
Secure Device Transfer

## SSD

Retrieve:

Storage Media Sanitization
+
Secure Data Erasure
+
Platform Security Guidance

## eMMC

Retrieve:

Storage Media Sanitization
+
Platform Security Guidance
+
Factory Reset and Sanitization

## Flash Storage

Retrieve:

Storage Media Sanitization
+
Secure Data Erasure

## Unknown

Retrieve:

Storage Media Sanitization

with guidance to identify the actual media before detailed sanitization advice.

---

# Example — SSD Laptop for Sale

## Assessment

Device:
Laptop

Storage:
SSD

Personal Data:
Yes

Sensitive Data:
Yes

Device Accessible:
Yes

Secure Erase:
No

Factory Reset:
No

Encryption:
No

Intended Action:
Sell

## Reasoning

Sensitive Data Present
        +
SSD Storage
        +
No Secure Erasure
        +
No Reset
        +
Permanent Transfer
        ↓
Sanitization Required Before Sale

## Recommendation

Do not transfer the device yet.

Back up required data and use an appropriate SSD-aware sanitization process before completing the platform reset and sale.

---

# Example — HDD for Reuse

## Assessment

Device:
External Hard Drive

Storage:
HDD

Personal Data:
Yes

Sensitive Data:
No

Data Backed Up:
Yes

Secure Erase:
No

Intended Action:
Reuse

## Reasoning

Storage Remains Functional
        +
Data No Longer Needed
        +
Reuse Planned
        ↓
Sanitize Before Reassignment

## Recommendation

Use an appropriate sanitization process before assigning the drive to another user.

If successful, reuse is preferable to unnecessary disposal.

---

# Example — Broken Storage for Recycling

## Assessment

Device:
Laptop

Storage:
SSD

Condition:
Physically Damaged

Can Power On:
No

Device Accessible:
No

Sensitive Data:
Yes

Secure Erase:
No

Intended Action:
Recycle

## Reasoning

Sensitive Data May Remain
        +
Normal Erasure Unavailable
        +
Device Leaving User Control
        ↓
Additional Handling Required

## Recommendation

Do not assume that the storage is safe because the device is broken.

Use a trusted process capable of handling the remaining storage-security risk before or as part of responsible recycling.

---

# EcoShield Decision Context

Storage-media sanitization is primarily associated with:

- `device_type`
- `operating_system`
- `device_condition`
- `storage_type`
- `storage_capacity`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `encryption_enabled`
- `intended_disposal_method`

The most important field for this document is:

`storage_type`

---

# Relationship With Other Knowledge Documents

Use:

`secure_data_erasure.md`

for general secure-erasure concepts.

Use:

`factory_reset_and_sanitization.md`

for reset-versus-sanitization guidance.

Use:

`platform_security_guidance.md`

for operating-system-specific preparation.

Use:

`removable_media_security.md`

for SIM cards, SD cards, and other removable media.

Use:

`secure_device_transfer.md`

for the overall transfer workflow.

This document should remain focused on **storage-technology-specific sanitization decisions**.

---

# EcoShield Recommendation Principle

EcoShield should reason about storage sanitization using:

Storage Type
      +
Data Sensitivity
      +
Device Accessibility
      +
Power State
      +
Encryption
      +
Secure-Erase Status
      +
Intended Action
      ↓
Appropriate Sanitization Guidance

The system should never assume that all storage technologies behave identically.

---

# Privacy-by-Design Principle

EcoShield should never require users to upload or expose the actual contents of storage media.

The application should not request:

- personal files
- photographs
- confidential documents
- passwords
- encryption keys
- recovery keys
- account credentials
- forensic disk images
- authentication secrets

EcoShield only requires status information needed for decision support.

---

# Important Limitation

EcoShield does not perform forensic verification.

It cannot prove that:

- every storage sector has been sanitized
- deleted information is absolutely unrecoverable
- physical destruction has been completed correctly
- a manufacturer sanitization command succeeded internally

The system should therefore use careful language such as:

- "based on the information provided"
- "reported as sanitized"
- "verify before transfer"
- "use an appropriate trusted sanitization process"

rather than issuing absolute technical guarantees.

---

# Keywords

storage sanitization, HDD sanitization, SSD sanitization, eMMC, flash storage, USB drive, SD card, microSD card, secure erase, data wiping, storage wiping, data destruction, factory reset, encryption, wear leveling, over-provisioning, broken drive, damaged storage, device recycling, device resale, device donation, secure transfer, data privacy