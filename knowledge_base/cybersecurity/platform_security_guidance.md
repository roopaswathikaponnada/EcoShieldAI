# Platform Security Guidance

## Purpose

Different operating systems and device platforms provide different security, encryption, account-management, reset, and data-protection features.

EcoShield uses platform security guidance to provide recommendations that are relevant to the operating system and device type selected during the device assessment.

Platform-specific guidance should complement EcoShield's general cybersecurity recommendations rather than replace them.

---

## Why Platform-Specific Guidance Matters

Security procedures are not identical across all electronic devices.

A Windows laptop, Android phone, iPhone, macOS computer, Linux system, and Chromebook may use different mechanisms for:

- device encryption
- account management
- backup
- factory reset
- storage sanitization
- device recovery
- remote management
- removable media
- ownership transfer

EcoShield should therefore avoid giving identical instructions to every platform.

---

## EcoShield Platform Context

EcoShield primarily uses:

`device_type`

and

`operating_system`

to determine which platform guidance is relevant.

Other important assessment fields include:

- `storage_type`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `data_backed_up`
- `factory_reset_performed`
- `secure_erase_performed`
- `encryption_enabled`
- `accounts_signed_out`
- `sim_memory_card_removed`
- `intended_disposal_method`

Platform guidance should be considered together with these security conditions.

---

# Windows Security Guidance

## Account Security

Windows devices may use:

- local user accounts
- Microsoft accounts
- work accounts
- school accounts
- browser profiles
- application accounts
- cloud-storage accounts

Before permanently transferring a Windows device, users should review and remove relevant account connections.

Signing out of applications alone should not be considered a replacement for appropriate device sanitization.

---

## Windows Encryption

Windows devices may provide encryption technologies such as:

- Device Encryption
- BitLocker

Availability depends on factors such as:

- Windows edition
- hardware
- device configuration
- organizational policies

Users should verify the actual encryption status of the device rather than assuming that encryption is enabled.

EcoShield should never request BitLocker recovery keys, passwords, PINs, or other authentication secrets.

---

## Windows Backup

Before performing irreversible reset or sanitization procedures, users should back up information they need to retain.

Possible backup locations may include:

- external storage
- trusted cloud storage
- another secure computer
- organization-approved backup systems

The backup should be verified before the original information is intentionally removed.

---

## Windows Reset

Windows provides system recovery and reset capabilities.

A reset can help prepare a computer for reuse or ownership transfer.

However, EcoShield should not assume that every reset option provides identical data-sanitization assurance.

For devices containing sensitive information, the reset process should be considered together with:

- encryption
- secure erasure
- storage technology
- account removal
- intended transfer method

---

## Windows Device Transfer

Before selling or donating a Windows computer, a general preparation process may include:

1. Back up required files.
2. Review Microsoft and other linked accounts.
3. Verify encryption status.
4. Sign out of relevant services.
5. Remove unnecessary external or removable storage.
6. Perform appropriate data sanitization.
7. Perform the applicable Windows reset procedure.
8. Verify that previous user information is no longer accessible.

---

# macOS Security Guidance

## Account Security

macOS devices may be connected to:

- Apple accounts
- iCloud
- email accounts
- browser profiles
- application accounts
- work or educational accounts

These account connections should be reviewed before transferring ownership.

---

## macOS Encryption

macOS systems may use FileVault to protect information stored on the startup disk.

Encryption can provide additional protection against unauthorized access to stored information.

Users should verify whether encryption is enabled rather than assuming that it is active.

EcoShield should never request:

- Apple account passwords
- FileVault recovery keys
- device passwords
- authentication secrets

---

## macOS Backup

Important files should be backed up before performing irreversible reset or erasure operations.

Users should verify that required information can be recovered from the backup before sanitizing the original device.

---

## macOS Device Transfer

Before selling or donating a Mac, users should generally consider:

1. Backing up required information.
2. Reviewing Apple and other account connections.
3. Verifying encryption status.
4. Signing out or removing relevant accounts.
5. Performing the appropriate erase/reset process.
6. Verifying that personal information is no longer accessible.
7. Preparing the device for its next owner.

The exact procedure can vary by Mac model and operating-system version.

---

# Linux Security Guidance

## Linux Account Security

Linux systems may contain:

- local user accounts
- administrator accounts
- browser accounts
- SSH credentials
- application credentials
- development credentials
- cloud-service configurations
- work or educational information

Users should carefully review these before transferring a Linux computer.

---

## Linux Encryption

Linux systems can use several storage-encryption technologies.

The implementation depends heavily on how the system was originally configured.

EcoShield should therefore avoid assuming that all Linux devices use the same encryption mechanism.

Users should verify their actual disk or partition encryption status.

---

## Linux Data Sensitivity

Linux systems used for software development, cybersecurity, administration, or professional work may contain sensitive material such as:

- SSH keys
- API credentials
- configuration files
- source code
- browser profiles
- authentication tokens
- certificates
- virtual-machine data

These should be considered when preparing the device for transfer.

EcoShield should never ask users to provide these secrets.

---

## Linux Device Transfer

A general transfer process may include:

1. Back up required information.
2. Review local and remote accounts.
3. Remove sensitive credentials.
4. Verify encryption status.
5. Perform storage-appropriate sanitization.
6. Reinstall or reset the operating environment where appropriate.
7. Verify the final state.

Exact procedures depend on the Linux distribution and storage configuration.

---

# Android Security Guidance

## Google and Manufacturer Accounts

Android devices may be connected to:

- Google accounts
- manufacturer accounts
- email accounts
- social applications
- cloud-storage services
- payment applications
- work profiles

These accounts may contain or provide access to personal information.

They should be reviewed before the device is permanently transferred.

---

## Android Device Encryption

Modern Android devices commonly provide platform-managed storage protection, but the implementation and behavior can vary by:

- Android version
- manufacturer
- device hardware
- configuration

EcoShield should not assume identical encryption behavior across all Android devices.

---

## Android Backup

Before reset or sanitization, users should identify information that needs to be retained.

This may include:

- photos
- videos
- documents
- contacts
- messages
- application data

Backups should be verified before irreversible actions are performed.

---

## Android SIM and Memory Cards

Android devices may contain:

- SIM cards
- microSD cards
- other removable storage

A factory reset does not physically remove these components.

EcoShield therefore separately evaluates:

`sim_memory_card_removed`

Users should review removable media before selling, donating, or recycling the device.

---

## Android Device Transfer

A general preparation flow may include:

1. Back up important information.
2. Review Google and manufacturer accounts.
3. Verify encryption where possible.
4. Remove relevant accounts.
5. Remove SIM and memory cards.
6. Perform the appropriate reset process.
7. Verify that personal information is no longer accessible.

Platform and manufacturer instructions should be followed for detailed procedures.

---

# iOS and iPadOS Security Guidance

## Apple Account Security

iPhones and iPads may be linked to an Apple account and associated services.

Before transferring ownership, users should review account and device associations.

Personal services may include:

- iCloud
- email
- photos
- messages
- synchronized contacts
- application data
- device-location services

---

## iPhone and iPad Data Protection

Apple mobile devices use platform-integrated data-protection mechanisms.

The exact implementation depends on hardware and operating-system configuration.

EcoShield should treat encryption and reset guidance according to the platform rather than applying desktop-storage instructions directly to mobile devices.

---

## iPhone SIM Handling

Depending on the model and region, an iPhone may use:

- a physical SIM
- an eSIM
- both

A physical SIM should be handled separately from the device-reset process.

eSIM configuration may require platform-specific handling before ownership transfer.

EcoShield should not assume that every iPhone uses a removable physical SIM.

---

## iPhone and iPad Transfer

A general ownership-transfer process may include:

1. Back up information that must be retained.
2. Review Apple account and device associations.
3. Review relevant services and applications.
4. Handle SIM or eSIM configuration where applicable.
5. Perform the appropriate platform erase/reset process.
6. Verify that previous user information is no longer accessible.
7. Prepare the device for its next owner.

---

# ChromeOS Security Guidance

## Google Account Security

Chromebooks are closely associated with Google accounts.

Before transferring a Chromebook, users should review:

- Google account sessions
- synchronized browser information
- downloaded files
- local user information
- work or school accounts

---

## ChromeOS Reset

ChromeOS provides reset functionality intended to remove local user information and prepare the device for another user.

However, organization-managed devices may have additional administrative restrictions.

Users should follow appropriate organizational procedures when the Chromebook belongs to a school, workplace, or other managed environment.

---

## ChromeOS Device Transfer

A general process may include:

1. Back up required local information.
2. Review Google account synchronization.
3. Remove relevant user accounts.
4. Follow the appropriate ChromeOS reset process.
5. Verify that previous user information is no longer accessible.
6. Confirm that organizational management requirements have been addressed.

---

# Other and Unknown Platforms

EcoShield may encounter a device whose operating system is:

- Other
- Unknown
- unsupported
- proprietary
- unavailable

In these cases, EcoShield should avoid inventing platform-specific procedures.

Instead, the system should provide general security principles such as:

- back up important information
- remove user accounts where possible
- verify encryption where possible
- sanitize storage appropriately
- remove removable media
- follow manufacturer guidance
- verify the final device state

The RAG or LLM layer should clearly communicate uncertainty when exact platform guidance is unavailable.

---

# Platform Guidance for Inaccessible Devices

If:

`device_accessible = No`

platform-specific software procedures may not be possible.

For example, the user may be unable to:

- sign out of accounts
- check encryption
- initiate a reset
- perform software-based sanitization
- verify the final device state

EcoShield should not recommend impossible steps without acknowledging this limitation.

Instead, recommendations should consider:

- storage type
- data sensitivity
- device condition
- ability to power on
- intended disposal method

---

# Platform Guidance for Devices That Cannot Power On

If:

`can_power_on = No`

normal operating-system procedures may be unavailable.

A device that does not power on should not automatically be considered secure.

Its storage may still contain information.

EcoShield should therefore consider storage-media security and responsible handling rather than relying solely on platform reset instructions.

---

# Platform Guidance for Repair

Repair differs from permanent ownership transfer.

The device is normally expected to return to the same owner.

Before repair, where practical:

- back up important data
- minimize unnecessary sensitive information
- maintain encryption
- sign out of particularly sensitive services where appropriate
- use authorized or trusted repair channels
- follow manufacturer guidance

A factory reset should not automatically be recommended for every repair scenario.

---

# Platform Guidance for Selling and Donation

Selling and donation normally involve a permanent transfer to another user.

For supported platforms, EcoShield should consider:

Backup
    ↓
Account Review
    ↓
Encryption Verification
    ↓
Data Sanitization
    ↓
Platform Reset
    ↓
Removable Media Handling
    ↓
Final Verification
    ↓
Ownership Transfer

The exact implementation of each stage depends on the platform.

---

# Platform Guidance for Recycling

If a device cannot reasonably be reused or repaired, recycling may be appropriate.

Before recycling, users should still consider stored information.

Platform reset procedures may be useful when the device remains functional.

When the device is damaged or inaccessible, storage-specific sanitization or appropriate destruction guidance may become more relevant than operating-system instructions.

---

# Privacy-by-Design Principle

EcoShield provides guidance based on device-security status.

The system should never request:

- passwords
- PINs
- recovery keys
- encryption keys
- authentication tokens
- private keys
- account credentials
- personal file contents

Platform-specific recommendations should explain what the user should verify or perform without collecting the secrets required to perform those actions.

---

# RAG Retrieval Guidance

This document should be considered particularly relevant when a query or assessment contains platform information.

Examples:

`operating_system = Windows`

Retrieve Windows account, encryption, reset, and transfer guidance.

`operating_system = Android`

Retrieve Android account, encryption, reset, SIM, and memory-card guidance.

`operating_system = iOS`

Retrieve Apple account, device-protection, reset, and SIM/eSIM guidance.

`operating_system = macOS`

Retrieve macOS account, FileVault, backup, reset, and ownership-transfer guidance.

`operating_system = Linux`

Retrieve Linux account, credential, encryption, and storage guidance.

`operating_system = ChromeOS`

Retrieve Google account, ChromeOS reset, and managed-device guidance.

Platform guidance should be combined with more specialized knowledge-base documents when necessary.

For example:

Windows + SSD + Secure Erase
    ↓
Platform Security Guidance
        +
Storage Media Sanitization
        +
Secure Data Erasure

This allows EcoShield to produce more contextually relevant recommendations.

---

# EcoShield Decision Context

Platform security guidance is primarily associated with:

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
- `accounts_signed_out`
- `sim_memory_card_removed`
- `intended_disposal_method`

These fields provide the context required to determine which platform guidance is relevant.

---

# EcoShield Recommendation Principle

EcoShield should provide platform-aware recommendations without assuming that all operating systems use identical security procedures.

The recommendation process should follow:

Device Type
      +
Operating System
      +
Storage Type
      +
Security State
      +
Data Sensitivity
      +
Intended Action
      ↓
Relevant Platform Guidance

When exact platform-specific information is unavailable, EcoShield should provide general security guidance and clearly communicate the limitation rather than inventing technical instructions.

---

# Keywords

platform security, Windows security, BitLocker, Device Encryption, macOS security, FileVault, Linux security, Android security, iOS security, iPadOS security, ChromeOS security, device reset, account removal, device encryption, data protection, device transfer, device donation, device resale, recycling, factory reset, secure erase, SIM card, eSIM, removable storage