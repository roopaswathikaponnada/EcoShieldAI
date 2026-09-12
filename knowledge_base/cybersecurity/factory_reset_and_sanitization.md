# Factory Reset and Data Sanitization

## Purpose

Factory reset and data sanitization are important security processes used when preparing an electronic device for resale, donation, reuse, recycling, or disposal.

Although the terms are sometimes used interchangeably, they do not necessarily represent the same level of data protection.

EcoShield evaluates factory-reset status and secure-erasure status separately so that users are not given a false sense of security before transferring a device.

---

## What Is a Factory Reset?

A factory reset is a device-level process that attempts to return a device to its original or default software state.

Depending on the device and operating system, a factory reset may:

- remove user accounts
- remove installed applications
- delete user settings
- remove locally stored user data
- restore default configuration
- prepare the device for another user

Factory reset functionality is commonly available on:

- smartphones
- tablets
- laptops
- desktop computers
- some smart devices

However, the exact behavior varies between platforms and devices.

---

## What Is Data Sanitization?

Data sanitization is the process of making data stored on a device inaccessible or impractical to recover.

Its purpose is to reduce the possibility that previously stored information can be retrieved after the device leaves the owner's control.

Sanitization methods depend on factors such as:

- storage technology
- device type
- operating system
- device accessibility
- encryption status
- sensitivity of the information
- intended disposal method

Data sanitization should therefore be selected according to the specific device and storage media.

---

## Factory Reset vs Data Sanitization

Factory reset and data sanitization should not automatically be considered equivalent.

A simplified distinction is:

Factory Reset
    ↓
Returns the device toward a default user state

Data Sanitization
    ↓
Focuses specifically on preventing access to previously stored data

The security effectiveness of a factory reset depends on the platform, implementation, encryption state, and storage technology.

EcoShield should therefore avoid assuming that every factory reset provides the same sanitization assurance.

---

## EcoShield Assessment Fields

EcoShield separately tracks:

`factory_reset_performed`

and

`secure_erase_performed`

This separation is intentional.

It allows the risk engine and recommendation system to distinguish between:

- a device that has not been reset
- a device that has only been factory reset
- a device that has undergone secure erasure
- a device where both actions have been completed
- a device where the status is uncertain

---

## Factory Reset Performed — Yes

When:

`factory_reset_performed = Yes`

the user indicates that the device's factory-reset process has been completed.

This is generally a positive preparation step.

However, EcoShield should still consider:

- whether secure erasure was performed
- whether accounts were signed out
- whether removable media was removed
- whether encryption was enabled
- whether personal or sensitive data existed
- what the user intends to do with the device

A factory reset alone should not automatically cause EcoShield to mark every device as safe for transfer.

---

## Factory Reset Performed — No

When:

`factory_reset_performed = No`

the device may still contain:

- user profiles
- application information
- local files
- configuration information
- account associations
- cached information
- personal settings

If the device is being sold, donated, recycled, or transferred, EcoShield should normally recommend completing appropriate security preparation before proceeding.

---

## Factory Reset Status — Unsure

When:

`factory_reset_performed = Unsure`

EcoShield should treat the reset state as uncertain.

The system should not assume that a reset has occurred.

If the device is accessible, the user should verify its current state before transfer.

If verification is impossible, EcoShield should clearly communicate the uncertainty.

---

## Secure Erase Performed — Yes

When:

`secure_erase_performed = Yes`

the user indicates that an appropriate secure-erasure or sanitization process has been completed.

This can significantly reduce residual-data risk.

However, EcoShield should still evaluate other security conditions such as:

- active accounts
- removable storage
- backup status
- device accessibility
- intended transfer method

Secure erasure addresses stored data, but other security or identity issues may still exist.

---

## Secure Erase Performed — No

When:

`secure_erase_performed = No`

previously stored information may not have undergone an intentional sanitization process.

This becomes particularly important when:

- personal data exists
- sensitive data exists
- the device will be sold
- the device will be donated
- ownership will change
- the device will be recycled
- storage media will leave the user's control

EcoShield may recommend an appropriate sanitization procedure before the device is transferred.

---

## Secure Erase Status — Unsure

When:

`secure_erase_performed = Unsure`

EcoShield should not assume that secure sanitization has occurred.

The uncertainty should be highlighted, particularly when the device previously contained sensitive information.

The user should verify the sanitization status where technically possible.

---

## File Deletion Is Not the Same as Sanitization

Deleting files through normal operating-system functions should not automatically be considered secure sanitization.

A typical deletion process may remove the user's normal reference to a file without necessarily providing assurance that the underlying information has been securely handled.

Therefore:

Normal File Deletion ≠ Verified Data Sanitization

EcoShield should not recommend ordinary file deletion as the only security preparation before transferring a device containing important personal or sensitive information.

---

## Formatting Is Not Automatically Secure Erasure

Formatting a storage device may prepare it for reuse, but not every formatting operation provides the same security properties.

The effect depends on:

- formatting method
- operating system
- storage technology
- encryption
- device implementation

EcoShield should therefore avoid treating the word "format" as automatic proof of secure sanitization.

---

## Factory Reset and Encryption

Encryption can significantly affect how data protection works during device reset and sanitization.

On some modern encrypted devices, properly implemented reset processes may remove or invalidate cryptographic information required to access previously stored data.

However, the exact behavior is platform-dependent.

EcoShield should therefore avoid making a universal claim that:

"Factory reset always securely destroys all data."

Instead, platform-specific guidance should be used when detailed sanitization instructions are required.

---

## Sanitization and Storage Technology

Different storage technologies may require different sanitization approaches.

Common storage types include:

- HDD
- SSD
- flash storage
- embedded mobile-device storage
- USB storage
- SD cards
- other removable storage

A method appropriate for one storage technology may not be appropriate for another.

EcoShield tracks:

`storage_type`

so that later RAG retrieval can provide storage-specific guidance.

---

## Hard Disk Drives

Traditional hard disk drives store information magnetically.

Depending on the security requirement and condition of the drive, appropriate sanitization may involve supported overwrite, erase, or destruction procedures.

EcoShield should rely on authoritative sanitization guidance rather than recommending the same method for every hard drive.

---

## Solid-State Drives

Solid-state drives use flash-based storage and behave differently from traditional hard disk drives.

Storage-management mechanisms may make traditional assumptions about simple overwrite procedures unreliable.

Where supported, appropriate device or manufacturer secure-erase functionality should be considered.

EcoShield's RAG system should retrieve SSD-specific sanitization guidance when:

`storage_type = SSD`

---

## Mobile and Embedded Storage

Smartphones and tablets commonly use integrated flash storage and platform-managed encryption.

Sanitization should generally follow the security procedures appropriate to that platform and manufacturer.

EcoShield should retrieve platform-specific guidance rather than applying desktop-drive instructions directly to mobile devices.

---

## Removable Storage

A device may contain separate removable storage such as:

- SD cards
- microSD cards
- USB storage
- external drives

Resetting the primary device may not necessarily sanitize separate removable media.

EcoShield therefore tracks:

`sim_memory_card_removed`

as a separate assessment condition.

Users should inspect and handle removable storage independently before transferring the device.

---

## SIM Cards

A SIM card is different from normal device storage but may contain subscriber-related information or remain associated with a user's mobile service.

A factory reset does not physically remove the SIM card.

Before selling, donating, recycling, or transferring an applicable device, the user should verify that the SIM card has been removed or appropriately handled.

---

## Data Backup Before Sanitization

Sanitization can permanently remove information.

Before performing irreversible data-removal procedures, users should confirm whether important files need to be retained.

EcoShield tracks:

`data_backed_up`

A general sequence is:

Identify Important Data
        ↓
Create Required Backup
        ↓
Verify Backup
        ↓
Prepare Accounts
        ↓
Perform Appropriate Sanitization
        ↓
Factory Reset Where Applicable
        ↓
Verify Final Device State

Users should not intentionally sanitize important information until necessary backups have been completed and verified.

---

## Account Sign-Out Before Reset

Account security should be reviewed before device transfer.

EcoShield separately tracks:

`accounts_signed_out`

Signing out or removing relevant accounts can help prevent:

- cloud-account exposure
- browser-session access
- synchronization issues
- identity exposure
- continued device-account associations

Account preparation and storage sanitization address different security concerns.

Both may be required.

---

## Accessible Devices

When:

`device_accessible = Yes`

the user may be able to:

- back up important data
- verify encryption
- sign out of accounts
- perform secure erasure
- perform factory reset
- remove removable media
- verify the final state

This provides more options for safe device preparation.

---

## Inaccessible Devices

When:

`device_accessible = No`

normal software-based sanitization may not be possible.

EcoShield should not instruct the user to complete software procedures that require access if the device cannot actually be accessed.

Instead, the system should consider:

- whether sensitive data existed
- storage type
- device condition
- intended disposal method
- whether professional handling may be appropriate

The recommendation should acknowledge the limitation.

---

## Devices That Cannot Power On

When:

`can_power_on = No`

the user may be unable to perform:

- account sign-out
- encryption verification
- software-based sanitization
- factory reset
- final verification

A non-functional device should not automatically be considered secure merely because it cannot start.

Its storage may still contain information.

EcoShield should consider the previous sensitivity of the data and the intended handling of the device.

---

## Selling a Device

Before selling a functional device, a general preparation sequence may include:

1. Back up important data.
2. Sign out of relevant accounts.
3. Verify encryption status.
4. Remove removable storage.
5. Perform appropriate data sanitization.
6. Perform the applicable factory-reset process.
7. Verify that personal information is no longer accessible.
8. Prepare the device for the new owner.

---

## Donating a Device

Donation also involves transferring the device to another user.

Before donation:

- required information should be backed up
- accounts should be removed
- personal information should be sanitized
- removable media should be removed
- the device should be reset where appropriate
- the final state should be verified

A functioning device can then potentially receive a second useful life.

This supports both cybersecurity and sustainability goals.

---

## Recycling a Device

Recycling does not automatically guarantee that stored information is securely destroyed.

Before recycling, users should perform appropriate sanitization when technically possible.

If the device is damaged or inaccessible, the storage-media risk should be considered separately.

Users should choose an appropriate responsible recycling process rather than placing electronics in ordinary waste.

---

## Repairing a Device

Repair is different from permanent ownership transfer because the user may expect the device to be returned.

A full factory reset may not always be necessary before repair.

However, depending on the repair:

- important data should be backed up
- unnecessary sensitive information should be minimized
- account exposure should be considered
- encryption should be maintained where practical
- manufacturer or authorized-service guidance should be followed

EcoShield recommendations should therefore consider the intended action rather than recommending factory reset for every scenario.

---

## Reusing a Device

If the device is being reused by the same owner, factory reset and sanitization may not be necessary.

If the device is being reassigned to another person, stronger preparation may be appropriate.

EcoShield should distinguish continued personal use from ownership or user transfer.

---

## Recommended Preparation Flow

For a typical functional device being permanently transferred:

1. Identify important information.
2. Back up required data.
3. Verify the backup.
4. Sign out of relevant accounts.
5. Verify encryption status.
6. Remove SIM cards and removable media.
7. Perform appropriate data sanitization.
8. Perform the applicable factory reset.
9. Restart or inspect the device where appropriate.
10. Verify that previous personal information and accounts are no longer accessible.
11. Proceed with resale, donation, reuse, or recycling.

The exact sequence may vary by platform.

---

## Verification After Reset

Verification is an important final step.

Where technically possible, users should confirm that the device no longer exposes:

- previous user accounts
- personal files
- browser sessions
- email accounts
- cloud-storage connections
- application data
- personal settings

The device should appear appropriately prepared for its next intended use.

---

## What EcoShield Should Not Claim

EcoShield should not make absolute claims such as:

- every factory reset securely destroys all data
- deleted files can never be recovered
- every storage device uses the same sanitization method
- one overwrite method works for every storage technology
- encryption removes the need for sanitization
- a broken device contains no recoverable information

Recommendations should reflect device context and available evidence.

---

## EcoShield Decision Context

Factory reset and sanitization are primarily associated with:

- `factory_reset_performed`
- `secure_erase_performed`
- `storage_type`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `encryption_enabled`
- `accounts_signed_out`
- `sim_memory_card_removed`
- `device_condition`
- `intended_disposal_method`

These relationships allow the later RAG system to retrieve sanitization guidance that matches the user's actual device situation.

---

## EcoShield Recommendation Principle

EcoShield should treat factory reset as one part of a broader secure device-preparation process.

The system should evaluate:

Factory Reset
        +
Secure Erasure
        +
Encryption
        +
Account Sign-Out
        +
Backup
        +
Removable Media Handling
        +
Device Accessibility
        +
Intended Action
        ↓
Secure Device-Transfer Decision

No single control should automatically determine whether a device is ready for transfer.

---

## Keywords

factory reset, data sanitization, secure erase, data deletion, device reset, storage sanitization, HDD, SSD, flash storage, personal data, sensitive data, encryption, backup, account sign-out, removable media, device transfer, resale, donation, recycling, repair, data protection