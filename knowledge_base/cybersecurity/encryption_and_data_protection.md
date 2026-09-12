# Encryption and Data Protection

## Purpose

Encryption and data protection help protect information stored on an electronic device from unauthorized access.

Before a device is sold, donated, repaired, recycled, or otherwise transferred, users should understand whether the device contains personal or sensitive information and whether that information is protected by encryption.

EcoShield uses encryption status as one of the security conditions considered when assessing a device.

---

## What Is Encryption?

Encryption converts readable information into a protected form that cannot normally be understood without the correct cryptographic key or authentication mechanism.

In simple terms:

Normal Data
    ↓
Encryption
    ↓
Protected / Unreadable Data
    ↓
Correct Key or Authentication
    ↓
Readable Data

For example, files stored on an encrypted laptop may be difficult for an unauthorized person to access without the user's password, PIN, recovery key, or another required authentication method.

---

## Why Encryption Matters

Electronic devices may contain information such as:

- personal documents
- photographs
- emails
- contact information
- saved browser information
- financial records
- academic information
- work-related documents
- authentication information
- application data
- account information

If an unencrypted device is lost, stolen, sold, donated, or improperly disposed of, someone with access to its storage may potentially attempt to recover information from it.

Encryption provides an additional layer of protection against unauthorized access.

---

## EcoShield Encryption Assessment

EcoShield tracks encryption through the assessment field:

`encryption_enabled`

Possible values may include:

- Yes
- No
- Unsure
- Not Applicable

The exact accepted values should follow the options defined by the EcoShield configuration and validation layer.

---

## Encryption Enabled — Yes

If encryption is enabled, information stored on the device has an additional layer of protection.

This can reduce the risk of unauthorized access when:

- the device is lost
- the device is stolen
- storage is removed from the device
- another person obtains physical access
- the device is awaiting sanitization or transfer

However, encryption does not automatically make a device safe to sell, donate, or recycle.

Other preparation steps may still be required.

These may include:

- backing up required data
- signing out of accounts
- securely erasing data
- performing an appropriate factory reset
- removing removable storage
- verifying that personal information is no longer accessible

---

## Encryption Enabled — No

If encryption is not enabled, information stored on the device may have less protection against unauthorized physical access.

This becomes particularly important when the device:

- contains personal data
- contains sensitive data
- will be transferred to another person
- will be donated
- will be sold
- will be recycled
- will leave the owner's physical control

EcoShield may therefore treat disabled encryption as an additional security concern depending on the overall device context.

---

## Encryption Status — Unsure

A user may not know whether encryption is enabled.

In this situation, EcoShield should not automatically assume that encryption is active.

Instead, the encryption state should be treated as uncertain.

The user should verify the encryption status using the appropriate operating-system or device security settings when possible.

Uncertainty becomes more important when the device contains sensitive information or is about to leave the user's control.

---

## Encryption — Not Applicable

Some devices or storage scenarios may not provide a meaningful user-controlled encryption option.

In such cases, `Not Applicable` may be appropriate.

However, this value should not be used simply because the user does not know whether encryption exists.

When the status is unknown, `Unsure` is more appropriate than `Not Applicable`.

---

## Full-Disk Encryption

Full-disk encryption protects information across an entire storage device or a large portion of the device's storage.

Depending on the platform, encryption may protect:

- operating-system files
- user files
- application data
- temporary information
- system information

Access normally depends on an authentication mechanism or cryptographic key.

Full-disk encryption can significantly improve protection when a device or storage drive is physically obtained by an unauthorized person.

---

## File-Level Encryption

File-level encryption protects specific files, folders, or groups of information rather than necessarily protecting the entire storage device.

This may be useful for protecting particularly sensitive information.

However, other unencrypted information may still remain elsewhere on the device.

Therefore, file-level encryption should not automatically be treated as equivalent to complete device encryption.

---

## Device Encryption

Modern devices may provide built-in storage encryption.

The exact implementation depends on:

- operating system
- hardware
- device manufacturer
- device configuration
- account configuration
- security settings

EcoShield should avoid assuming that every device uses the same encryption technology.

Platform-specific guidance should be retrieved when detailed instructions are required.

---

## Encryption and Authentication

Encryption protection commonly depends on authentication mechanisms such as:

- passwords
- PINs
- security keys
- recovery keys
- hardware-backed credentials
- biometric authentication

Encryption is most useful when access credentials are properly protected.

Weak or exposed authentication credentials may reduce the practical security provided by encryption.

EcoShield does not require users to provide passwords, encryption keys, recovery keys, or other authentication secrets.

---

## Encryption Does Not Replace Secure Erasure

Encryption and secure data erasure serve different purposes.

### Encryption

Encryption protects information by making it unreadable without the required key or authentication mechanism.

### Secure Erasure

Secure erasure or sanitization focuses on making previously stored information inaccessible or impractical to recover.

Therefore:

Encryption ≠ Secure Erasure

A device should not automatically be considered safe for transfer simply because encryption is enabled.

Appropriate sanitization should still be considered before:

- selling
- donating
- recycling
- transferring ownership

---

## Encryption Does Not Replace Factory Reset

Encryption and factory reset are also different security controls.

Encryption protects stored information.

A factory reset generally attempts to return a device to a default or initial state.

Depending on the device and storage technology, a factory reset may not represent the same process as dedicated storage sanitization.

EcoShield therefore tracks:

`encryption_enabled`

`factory_reset_performed`

and

`secure_erase_performed`

as separate security conditions.

---

## Encryption and Personal Data

EcoShield tracks whether a device contains personal information using:

`contains_personal_data`

If personal data exists and encryption is disabled, the potential impact of unauthorized access may increase.

Examples of personal information include:

- names
- photographs
- personal documents
- messages
- contact information
- account information
- browsing information

Encryption provides additional protection while this information remains on the device.

---

## Encryption and Sensitive Data

EcoShield also tracks:

`contains_sensitive_data`

Sensitive information may require stronger protection because unauthorized disclosure could have greater consequences.

Examples may include:

- financial information
- confidential documents
- identity documents
- private communications
- organizational information
- authentication-related information
- confidential academic or professional data

When sensitive data exists, encryption status becomes particularly important.

However, encryption should still be combined with appropriate sanitization before ownership transfer.

---

## Encryption and Device Accessibility

EcoShield tracks:

`device_accessible`

If the device is accessible, the user may be able to:

- verify encryption status
- back up required information
- sign out of accounts
- perform sanitization
- perform a factory reset
- verify the final device state

If the device is inaccessible, normal security preparation may become more difficult.

EcoShield should highlight this limitation rather than assuming that security controls were completed.

---

## Encryption and Power State

EcoShield also considers:

`can_power_on`

A device that cannot power on may prevent the user from verifying:

- encryption settings
- account status
- stored information
- sanitization status
- factory-reset status

The inability to power on a device should therefore be considered together with the sensitivity of the information previously stored on it.

---

## Encryption Before Selling a Device

Before selling a device, users should consider the complete security-preparation process.

A general sequence may include:

1. Back up required information.
2. Verify encryption status.
3. Sign out of relevant accounts.
4. Remove unnecessary account associations.
5. Perform appropriate data sanitization.
6. Perform a factory reset when applicable.
7. Remove SIM cards or removable storage.
8. Verify that personal information is no longer accessible.

Encryption provides protection during this process but does not replace the process.

---

## Encryption Before Donating a Device

Donation transfers the device to another person or organization.

Before donation:

- important information should be backed up
- accounts should be removed
- stored information should be appropriately sanitized
- removable media should be removed
- factory reset should be performed where appropriate
- final device state should be verified

If encryption was enabled, it provides an additional protection layer while data remains on the device.

---

## Encryption Before Repair

Repair scenarios differ from permanent ownership transfer.

A technician may need access to some device functions to diagnose or repair the device.

Before repair, where practical:

- back up important information
- minimize unnecessary sensitive information
- sign out of sensitive applications when appropriate
- understand whether device access credentials are required
- follow manufacturer or authorized service guidance

Users should avoid unnecessarily sharing account passwords or encryption recovery keys.

---

## Encryption Before Recycling

A device intended for recycling may still contain recoverable information.

Users should not assume that recycling automatically destroys stored data.

Before recycling, appropriate sanitization should be performed when technically possible.

If the device cannot be sanitized because it is damaged or inaccessible, the user may require a recycling or destruction process appropriate for the storage media and sensitivity of the information.

---

## Encryption and Removable Media

Encryption of the main device does not necessarily mean that removable storage is encrypted.

Examples include:

- SD cards
- microSD cards
- USB drives
- external hard drives
- external SSDs

These storage devices may contain separate copies of personal information.

EcoShield therefore separately tracks:

`sim_memory_card_removed`

where applicable.

Removable storage should be reviewed separately before device transfer.

---

## Data Protection Layers

Secure device handling should use multiple protective layers rather than relying on a single control.

A simplified protection model is:

Account Security
        ↓
Authentication
        ↓
Encryption
        ↓
Backup
        ↓
Data Sanitization
        ↓
Factory Reset
        ↓
Verification
        ↓
Secure Transfer / Reuse / Recycling

Each layer addresses a different part of the security problem.

---

## Recommended Actions

When preparing a device that stores personal or sensitive information:

1. Determine whether important information must be retained.
2. Back up required information.
3. Verify whether device encryption is enabled.
4. Protect passwords, PINs, and recovery keys.
5. Sign out of relevant accounts.
6. Perform appropriate storage sanitization.
7. Perform a factory reset where applicable.
8. Remove removable storage or SIM cards.
9. Verify that personal information is no longer accessible.
10. Proceed with the intended device action only after security preparation is complete.

---

## What EcoShield Should Not Request

EcoShield should never require users to enter:

- account passwords
- device PINs
- encryption passwords
- recovery keys
- authentication tokens
- private cryptographic keys
- personal file contents

EcoShield only needs security-status information required for decision support.

This supports the project's privacy-by-design approach.

---

## Important Limitations

Encryption behavior differs across:

- Windows
- macOS
- Linux
- Android
- iOS and iPadOS
- ChromeOS
- storage technologies
- device manufacturers

The exact security effect of encryption may also depend on:

- device configuration
- encryption implementation
- key management
- authentication configuration
- hardware support
- operating-system version

EcoShield should therefore avoid claiming that encryption alone guarantees that data cannot be recovered.

---

## EcoShield Decision Context

Encryption and data protection are primarily associated with the following EcoShield assessment fields:

- `encryption_enabled`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `accounts_signed_out`
- `sim_memory_card_removed`
- `intended_disposal_method`

The RAG system can use these relationships to retrieve encryption guidance when a user's assessment indicates that encryption is disabled, uncertain, or particularly important because sensitive information is present.

---

## EcoShield Recommendation Principle

Encryption should be treated as a protective security layer rather than proof that a device is ready for transfer.

For devices containing personal or sensitive information, EcoShield should evaluate encryption together with:

- account security
- backup status
- secure erasure
- factory reset
- device accessibility
- removable-media handling
- intended device action

The final recommendation should reflect the complete security state of the device rather than relying on encryption alone.

---

## Keywords

encryption, data protection, device encryption, full-disk encryption, file encryption, personal data, sensitive data, secure erase, data sanitization, factory reset, authentication, recovery key, storage security, device transfer, device donation, device resale, device recycling, privacy, removable media