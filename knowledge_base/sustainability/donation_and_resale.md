# Donation and Resale

## Purpose

Donating or reselling a functional electronic device can extend its
useful life and reduce premature electronic waste.

However, donation and resale also involve a permanent change of
ownership.

This creates an important cybersecurity requirement:

**A device should not be transferred to another person until the
previous owner's personal data, accounts, credentials, and removable
media have been appropriately handled.**

EcoShield uses this knowledge to combine:

- secure device transfer
- data protection
- account protection
- appropriate data sanitization
- device reuse
- sustainable lifecycle extension

---

# Why Donation and Resale Matter

A device that is no longer required by its current owner may still
have useful life remaining.

Instead of:

Functional Device
        ↓
Discard
        ↓
Electronic Waste

a more sustainable route may be:

Functional Device
        ↓
Secure Preparation
        ↓
Donate / Resell
        ↓
New Owner
        ↓
Second Useful Life

Donation and resale can therefore support device reuse and delay
end-of-life recycling.

---

# Donation vs Resale

Donation and resale have different purposes, but they create similar
cybersecurity concerns.

## Donation

The device is transferred without a normal commercial sale.

Examples include:

- giving a laptop to another person
- donating a tablet
- giving an old smartphone to a family member
- donating equipment to an organization

## Resale

The device is transferred to another owner in exchange for payment.

Examples include:

- selling a used laptop
- selling a smartphone
- selling a tablet
- trading or transferring used electronics

In both cases:

Ownership Changes
        ↓
Previous User Loses Control
        ↓
Security Preparation Required

---

# EcoShield Assessment Context

Important EcoShield fields include:

- `device_type`
- `operating_system`
- `device_age`
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
- `accounts_signed_out`
- `sim_memory_card_removed`
- `intended_disposal_method`

This document should receive particularly strong retrieval relevance
when:

`intended_disposal_method = Donate`

or:

`intended_disposal_method = Sell`

---

# Core Security Principle

Donation and resale should be treated as permanent ownership
transfers.

Therefore:

Device Suitable for Reuse
        ↓
Is Ownership Changing?
        ↓
       Yes
        ↓
Security Preparation Required
        ↓
Transfer Only After Preparation

A functional device is not automatically transfer-ready.

---

# Recommended Transfer Sequence

A general preparation sequence is:

Review Device
      ↓
Back Up Important Data
      ↓
Review Accounts and Services
      ↓
Remove Removable Media
      ↓
Apply Appropriate Data Sanitization
      ↓
Perform Platform-Appropriate Reset
      ↓
Verify Personal Information Is Removed
      ↓
Transfer Device
      ↓
Second Useful Life

The exact sequence may vary by device and platform.

EcoShield should therefore combine this document with more specific
cybersecurity guidance.

---

# Step 1 — Confirm the Device Is Suitable for Transfer

Before donation or resale, evaluate whether the device remains useful.

Consider:

- device condition
- ability to power on
- accessibility
- repairability
- platform support
- expected continued usefulness

If the device has a repairable problem, repair may help extend its
useful life before transfer.

Relevant sustainability documents include:

`device_repair.md`

and:

`device_reuse.md`

---

# Step 2 — Back Up Important Information

Before destructive sanitization or reset operations, important data
should be backed up when necessary.

EcoShield should evaluate:

`data_backed_up`

If:

`data_backed_up = No`

and the device contains information the user wants to preserve,
EcoShield should recommend backing up the required data before
sanitization.

Conceptually:

Important Data
      ↓
Backup
      ↓
Verify Backup
      ↓
Sanitize
      ↓
Transfer

---

# Why Backup Comes Before Sanitization

Sanitization and factory-reset operations may permanently remove data.

Therefore, users should not be instructed to erase a device before
considering whether required information has been preserved.

EcoShield should clearly distinguish:

Backup

from:

Sanitization

A backup preserves required information.

Sanitization removes information from the device being transferred.

---

# Step 3 — Protect Accounts and Identity

Electronic devices may remain connected to:

- operating-system accounts
- cloud accounts
- email accounts
- browser profiles
- application sessions
- synchronization services
- device-management services

Before ownership transfer, these relationships should be reviewed.

EcoShield should evaluate:

`accounts_signed_out`

If accounts remain active, the device may not be ready for transfer.

Relevant guidance should be retrieved from:

`account_and_identity_security.md`

---

# Account Credentials

EcoShield should never request the user's:

- passwords
- PINs
- one-time passwords
- authentication tokens
- recovery codes
- security answers
- encryption keys

The assessment only needs to know whether relevant account-security
preparation has been completed.

---

# Step 4 — Remove Removable Media

Before donation or resale, removable media that belongs to the current
owner should generally be considered separately.

Examples include:

- SIM cards
- SD cards
- microSD cards
- USB storage
- external drives

These may contain information independently of the main device.

EcoShield should evaluate:

`sim_memory_card_removed`

where relevant.

A device should not be considered fully prepared if personal removable
media has unintentionally been left inside it.

---

# SIM Cards

A SIM card may be associated with:

- a mobile subscription
- contact information
- service identity
- authentication-related functions

If the SIM card is not intended to be transferred, it should be
removed before giving the device to another person.

---

# Memory Cards

Memory cards may contain:

- photographs
- videos
- documents
- application files
- downloaded content
- backups

Resetting the primary device does not necessarily mean that removable
media has been appropriately handled.

Relevant guidance should be retrieved from:

`removable_media_security.md`

---

# Step 5 — Determine Data Sensitivity

EcoShield should evaluate:

`contains_personal_data`

and:

`contains_sensitive_data`

before determining transfer readiness.

A device containing sensitive information requires careful preparation
before permanent transfer.

---

# Personal Data

Personal information may include:

- photographs
- documents
- browser history
- messages
- contact information
- saved application data
- downloaded files
- account-related information

If personal data remains accessible, the device should not simply be
given to another person.

---

# Sensitive Data

Sensitive information may include:

- financial information
- identity documents
- confidential work files
- authentication information
- private communications
- sensitive photographs
- organizational information

The presence of sensitive data can increase the importance of
appropriate sanitization.

---

# Step 6 — Consider Encryption

Encryption protects stored information against unauthorized access
under appropriate conditions.

EcoShield evaluates:

`encryption_enabled`

However:

Encryption Enabled
        ≠
Transfer Ready

Encryption is a protection mechanism during device ownership and use.

Permanent transfer still requires appropriate preparation.

EcoShield should therefore distinguish:

Encryption
        ↓
Protect Stored Data

from:

Sanitization
        ↓
Prepare Storage for Transfer

---

# Step 7 — Apply Appropriate Data Sanitization

Before permanent ownership transfer, stored information should be
handled using a method appropriate for the device and storage
technology.

The correct approach may depend on:

- device type
- storage type
- operating system
- encryption state
- accessibility
- device condition
- ability to power on

EcoShield should not assume that one sanitization method works
identically for every device.

Relevant guidance should be retrieved from:

`secure_data_erasure.md`

and:

`storage_media_sanitization.md`

---

# Secure Erasure

EcoShield evaluates:

`secure_erase_performed`

when determining whether unresolved sanitization risks remain.

If secure sanitization is required but has not been completed,
EcoShield should not present the device as fully transfer-ready.

However, the exact sanitization method should depend on the device and
storage technology.

---

# Step 8 — Factory Reset

A platform-supported factory reset may be part of the transfer
preparation process.

EcoShield evaluates:

`factory_reset_performed`

However:

Factory Reset
        ≠
Universal Proof of Secure Erasure

The effectiveness of a factory reset depends on the platform,
implementation, encryption state, and storage technology.

Relevant guidance should therefore be retrieved from:

`factory_reset_and_sanitization.md`

---

# Factory Reset vs Secure Erasure

These concepts should not be treated as identical.

## Factory Reset

Typically restores a device toward its default user state.

## Secure Erasure / Sanitization

Focuses on reducing the possibility of recovering previous user data.

Depending on the platform, these processes may overlap.

EcoShield should rely on platform-appropriate guidance rather than
claiming they are universally equivalent.

---

# Step 9 — Verify Before Transfer

After preparation, the user should verify that the device no longer
exposes previous personal information.

Verification may include confirming that:

- previous user accounts are no longer available
- personal files are not visible
- removable media has been removed
- the device presents the expected setup state
- previous account sessions are no longer accessible

EcoShield should not claim that sanitization has succeeded merely
because the user clicked a reset option.

---

# Device Accessibility

If:

`device_accessible = Yes`

the user may be able to perform normal preparation steps.

If:

`device_accessible = No`

some security operations may not be possible through the normal user
interface.

EcoShield should acknowledge this limitation.

It should not instruct the user to complete an impossible action and
then treat failure to complete it as user negligence.

---

# Device Cannot Power On

If:

`can_power_on = No`

the device may still contain recoverable information.

Therefore:

Cannot Power On
        ≠
No Data Risk

For example, internal storage may remain physically present even if
the device itself is not operational.

If donation or resale is being considered, repair or professional
handling may be necessary before secure transfer.

---

# Donation of a Nonfunctional Device

A nonfunctional device should not automatically be donated as though
it were safely reusable.

EcoShield should consider:

- repairability
- stored data
- storage accessibility
- security risk
- intended recipient
- responsible recycling alternatives

If the device cannot be securely prepared for another owner, donation
may not currently be appropriate.

---

# Resale of a Nonfunctional Device

Some users may sell nonfunctional electronics for:

- repair
- refurbishment
- parts recovery

This still represents a transfer of physical possession.

If storage containing user data remains in the device, cybersecurity
risks may remain.

Therefore, "sold for parts" should not be treated as automatically
safe.

---

# Storage Drives and Ownership Transfer

Storage devices deserve special attention during donation or resale.

Examples include:

- HDDs
- SSDs
- flash storage
- removable storage

If a storage device cannot be appropriately sanitized, the user may
need to reconsider whether that storage should be transferred.

EcoShield should retrieve:

`storage_media_sanitization.md`

for storage-specific recommendations.

---

# Donation After Repair

Repair can enable a device to receive a second useful life.

Example:

Damaged Laptop
      ↓
Repair
      ↓
Functional Laptop
      ↓
Security Preparation
      ↓
Donation
      ↓
Second User

This can combine:

- repair
- reuse
- secure transfer
- lifecycle extension

---

# Resale After Repair

Similarly:

Damaged Device
      ↓
Repair
      ↓
Restore Useful Function
      ↓
Security Preparation
      ↓
Resale
      ↓
Continued Use

Repair does not eliminate the need for data sanitization before
ownership transfer.

---

# Donation vs Recycling

If a device remains functional and suitable for another user,
donation may extend its useful life.

Conceptually:

Functional Device
      ↓
Still Useful?
   ↙       ↘
 Yes       No
  ↓         ↓
Secure    Repair /
Donation  Recycling Evaluation

However, EcoShield should not recommend donation if the device is:

- unsafe
- unsuitable for continued use
- incapable of being securely prepared
- severely damaged without realistic reuse value

---

# Resale vs Recycling

Resale may similarly extend device life when the device remains useful.

The recommendation should consider:

Device Condition
        +
Functionality
        +
Security Preparation
        +
Platform Support
        +
Reuse Potential
        ↓
Resale Suitability

EcoShield should not base resale suitability solely on potential
financial value.

---

# Platform-Specific Preparation

Different operating systems may have different:

- account-removal processes
- encryption systems
- reset mechanisms
- activation relationships
- device-management settings
- sanitization capabilities

Therefore, EcoShield should retrieve:

`platform_security_guidance.md`

when giving detailed preparation instructions.

---

# Ownership Transfer Readiness

EcoShield can conceptually determine transfer readiness using:

Backup Status
      +
Personal Data
      +
Sensitive Data
      +
Sanitization Status
      +
Account Status
      +
Removable Media Status
      +
Accessibility
      +
Platform Context
      ↓
Transfer Readiness

Possible outcomes may include:

- Ready
- Conditional
- Not Ready

---

# Ready for Transfer

A device may be considered ready when required preparation steps have
been completed and no blocking security issue remains.

This does not mean EcoShield guarantees that no data can ever be
recovered.

It means the assessed preparation requirements have been addressed.

---

# Conditional Transfer

A conditional result may be appropriate when:

- some relevant information is uncertain
- platform-specific verification is still required
- the user is unsure about a security control
- the device condition limits normal preparation

The recommendation should clearly explain what must be verified.

---

# Not Ready for Transfer

A device may be considered not ready when significant unresolved
security conditions remain.

Examples may include:

- sensitive data remains
- sanitization has not been performed where required
- important accounts remain connected
- removable media remains inserted
- required preparation cannot yet be completed

EcoShield should clearly explain the blocking conditions.

---

# Example — Laptop Ready for Donation

## Assessment

Device:
Laptop

Condition:
Good

Power On:
Yes

Accessible:
Yes

Personal Data:
Yes

Sensitive Data:
No

Backup:
Yes

Secure Erase:
Yes

Factory Reset:
Yes

Accounts Signed Out:
Yes

Removable Media Removed:
Yes

Intended Action:
Donate

## Reasoning

Functional Device
        +
Security Preparation Completed
        +
Ownership Transfer Planned
        ↓
Donation Can Extend Device Life

## Recommendation

The laptop may be suitable for donation after final verification that
previous user information and account access are no longer available.

Donation can provide the device with a second useful life.

---

# Example — Smartphone Not Ready for Resale

## Assessment

Device:
Smartphone

Condition:
Good

Power On:
Yes

Accessible:
Yes

Personal Data:
Yes

Sensitive Data:
Yes

Backup:
Yes

Factory Reset:
No

Secure Erase:
No

Accounts Signed Out:
No

SIM / Memory Card Removed:
No

Intended Action:
Sell

## Reasoning

Device Suitable for Reuse
        BUT
Sensitive Data Present
        +
Accounts Remain
        +
Removable Media Remains
        +
Sanitization Incomplete
        ↓
Not Ready for Resale

## Recommendation

Do not transfer the smartphone yet.

Complete the appropriate account, removable-media, sanitization, and
platform-reset preparation before resale.

---

# Example — Laptop Has Not Been Backed Up

## Assessment

Device:
Laptop

Power On:
Yes

Accessible:
Yes

Personal Data:
Yes

Backup:
No

Intended Action:
Donate

## Reasoning

Ownership Transfer Planned
        +
Required Data May Still Exist
        +
Backup Not Completed
        ↓
Backup Should Precede Destructive Preparation

## Recommendation

Back up any information that needs to be retained before performing
sanitization or reset operations.

After verifying the backup, continue with the appropriate transfer
preparation.

---

# Example — Broken Laptop Sold for Parts

## Assessment

Device:
Laptop

Condition:
Severely Damaged

Power On:
No

Accessible:
No

Storage:
SSD

Sensitive Data:
Yes

Intended Action:
Sell

## Reasoning

Device Nonfunctional
        BUT
Storage Still Present
        +
Sensitive Data May Remain
        ↓
Data Risk Continues

## Recommendation

Do not assume that selling the laptop for parts eliminates the data
risk.

Consider how the internal storage will be handled before transferring
the device.

Retrieve storage-specific sanitization guidance where appropriate.

---

# Example — Functional Tablet Considered for Recycling

## Assessment

Device:
Tablet

Age:
3 Years

Condition:
Good

Power On:
Yes

Accessible:
Yes

Intended Action:
Recycle

## Reasoning

Functional
    +
Good Condition
    +
Potential Remaining Useful Life
        ↓
Reuse May Be Preferable

## Recommendation

Before recycling, consider whether the tablet could be securely
prepared for donation or resale.

If another useful life is practical, reuse may delay entry into the
e-waste stream.

---

# Sustainability Principle

Donation and resale can contribute to sustainability by extending
device life.

Conceptually:

First Owner
     ↓
Secure Transfer
     ↓
Second Owner
     ↓
Continued Use
     ↓
Delayed End-of-Life Processing

However, EcoShield should avoid assigning exact environmental savings
unless supported by reliable lifecycle evidence.

---

# Circular Device Lifecycle

Donation and resale support a more circular device lifecycle:

Purchase
    ↓
Use
    ↓
Maintain
    ↓
Repair
    ↓
Reuse / Donate / Resell
    ↓
Further Use
    ↓
Responsible Recycling at End of Life

This is preferable to unnecessarily shortening the useful life of
functional electronics.

---

# What EcoShield Should Avoid

EcoShield should avoid statements such as:

- factory reset always guarantees complete data removal
- encryption alone makes a device safe to sell
- donation is safe because no money is exchanged
- a device that cannot power on contains no recoverable information
- selling a device for parts removes all data risk
- every functional device should be donated
- every old device should be recycled
- accounts automatically disappear after ownership transfer
- removable media is always erased during factory reset
- all devices use the same sanitization process

Recommendations must depend on the actual device context.

---

# RAG Retrieval Guidance

This document should receive high retrieval relevance for queries
involving:

- donate device
- sell device
- resale device
- donate laptop
- sell laptop
- donate smartphone
- sell smartphone
- used electronics
- prepare device for sale
- prepare device for donation
- secure device transfer
- second-hand electronics
- remove personal data before selling
- factory reset before selling
- secure erase before donation
- transfer ownership
- second life electronics

It should receive especially strong relevance when:

`intended_disposal_method = Donate`

or:

`intended_disposal_method = Sell`

---

# Related Knowledge Retrieval

For ownership transfer security:

Donation and Resale
+
Secure Device Transfer
+
Account and Identity Security

For sanitization:

Donation and Resale
+
Secure Data Erasure
+
Storage Media Sanitization
+
Factory Reset and Sanitization

For platform-specific instructions:

Donation and Resale
+
Platform Security Guidance

For removable media:

Donation and Resale
+
Removable Media Security

For lifecycle reasoning:

Donation and Resale
+
Device Reuse
+
Sustainable Device Lifecycle

For a damaged device:

Donation and Resale
+
Device Repair
+
Device Reuse

---

# EcoShield Recommendation Principle

EcoShield should follow:

Functional Device
        ↓
Can It Have Another Useful Life?
        ↓
       Yes
        ↓
Prepare Securely
        ↓
Donate / Resell
        ↓
Second Useful Life

The key rule is:

**Sustainability should never require sacrificing cybersecurity.**

Therefore:

Reuse Potential
        +
Secure Data Preparation
        +
Account Protection
        +
Responsible Transfer
        ↓
Secure and Sustainable Device Transfer

---

# Privacy-by-Design Principle

EcoShield does not need the user's actual personal data to determine
whether a device requires security preparation.

EcoShield should never request:

- passwords
- PINs
- private files
- photographs
- banking information
- confidential documents
- authentication tokens
- encryption keys
- recovery codes

The system should assess only the security state of the device.

---

# Important Limitation

EcoShield is a decision-support system.

It cannot guarantee:

- that all data is unrecoverable
- the physical condition of the device
- the honesty of a buyer or recipient
- the security of a resale marketplace
- the reliability of a donation organization
- the future lifespan of the device
- the exact environmental benefit of donation or resale

Users should follow appropriate platform-specific and storage-specific
procedures when preparing devices for permanent ownership transfer.

---

# Keywords

device donation, device resale, sell laptop, donate laptop, sell
smartphone, donate smartphone, used electronics, second-hand
electronics, secure device transfer, ownership transfer, data removal
before sale, factory reset before sale, secure erase before donation,
device sanitization, account removal, removable media, device reuse,
second life electronics, sustainable electronics, e-waste prevention