# Account and Identity Security

## Purpose

Account and identity security focuses on protecting user accounts, cloud services, browser sessions, application logins, and other identity-related information before an electronic device is sold, donated, repaired, recycled, or otherwise transferred.

A device may no longer contain obvious personal files but can still remain linked to online accounts. These account connections can expose personal information or allow unintended access if they are not removed correctly.

---

## Why Account Security Matters

Modern electronic devices are often connected to multiple user accounts.

Examples include:

- Microsoft accounts
- Google accounts
- Apple accounts
- Browser profiles
- Email accounts
- Cloud storage accounts
- Social media accounts
- Banking or payment applications
- Work or educational accounts
- Password managers
- Application-specific accounts

If these accounts remain signed in, the next person who receives the device may be able to access personal information or services associated with the previous owner.

Account security should therefore be treated as an important part of device preparation.

---

## Accounts Signed Out

Before transferring a device, users should verify whether relevant accounts have been signed out or removed.

EcoShield tracks this through the assessment field:

`accounts_signed_out`

Possible values are:

- Yes
- No
- Not Applicable
- Unsure

### Yes

A value of **Yes** indicates that the user believes relevant accounts have been signed out or removed from the device.

This reduces the risk of account access after ownership transfer.

### No

A value of **No** means that one or more accounts may still remain signed in.

This creates a security risk because the new owner or another person with access to the device may be able to open applications, cloud services, browser sessions, or stored account information.

### Unsure

A value of **Unsure** means the user cannot confirm whether all accounts were signed out.

EcoShield should treat this as an uncertainty that requires verification before the device leaves the user's control.

### Not Applicable

A value of **Not Applicable** may be appropriate for devices that do not support user accounts or account-linked services.

For example, some external storage devices may not have an operating system or user-account functionality.

---

## Types of Accounts to Review

### Operating System Accounts

Devices may be connected to an operating-system account.

Examples include:

- Microsoft account on Windows
- Apple account on macOS, iPhone, or iPad
- Google account on Android or ChromeOS

These accounts may connect the device to cloud services, synchronization features, device-management functions, and identity information.

---

## Browser Accounts

Web browsers may store or synchronize:

- browsing history
- saved passwords
- bookmarks
- autofill information
- payment information
- logged-in websites
- browser extensions

Users should review browser profiles and sign out of synchronized browser accounts before transferring the device.

---

## Email and Communication Accounts

Email applications and communication platforms may provide access to:

- personal messages
- contacts
- attachments
- account recovery information
- work or educational communication

These accounts should be removed or signed out before device transfer.

---

## Cloud Storage Accounts

Cloud services may expose files even when those files are not stored permanently on the device.

Examples include:

- OneDrive
- Google Drive
- iCloud
- Dropbox
- other cloud-storage services

Signing out of these services helps prevent the next user from gaining access to synchronized information.

---

## Work and Educational Accounts

Devices may contain accounts connected to:

- organizations
- universities
- schools
- workplaces
- enterprise applications
- virtual private networks
- collaboration platforms

These accounts may provide access to confidential or restricted information.

Users should remove or sign out of such accounts according to organizational policies before transferring a device.

---

## Account Removal and Factory Reset

Signing out of accounts and performing a factory reset are related but separate security actions.

A factory reset may remove many local settings and accounts, but EcoShield should not assume that a factory reset automatically proves that every identity-related connection has been handled correctly.

Account review should therefore occur as a separate preparation step.

EcoShield tracks both:

`accounts_signed_out`

and

`factory_reset_performed`

as separate assessment fields.

---

## Account Security and Data Sanitization

Account sign-out also differs from secure data erasure.

Signing out prevents normal access to an account, while secure erasure focuses on removing residual information from storage.

A secure device-transfer process may require both.

For example:

1. Back up important information.
2. Sign out of accounts.
3. Review encryption.
4. Perform appropriate data sanitization.
5. Perform a factory reset where applicable.
6. Verify the device no longer provides access to personal accounts.

---

## Device Transfer Scenarios

### Selling

Before selling a device, users should remove all relevant personal and cloud-linked accounts.

The buyer should not be able to access the previous owner's identity or services.

### Donating

A donated device may pass to an unknown future user.

Account sign-out and data sanitization should therefore be completed before donation.

### Repairing

A repair technician may require physical or temporary access to the device.

Users should reduce unnecessary exposure by signing out of sensitive services and following appropriate backup and security procedures before repair where practical.

### Recycling

Even when a device will be recycled, account and identity information should still be protected before it leaves the owner's control.

### Reusing

If the same owner continues using the device, signing out of accounts may not be necessary unless the device is being reassigned to another user.

---

## Identity-Related Security Risks

Failure to remove accounts can create risks such as:

- unauthorized access to cloud services
- exposure of email and messages
- access to stored browser sessions
- access to synchronized files
- disclosure of contact information
- exposure of work or academic information
- unintended access to subscription services
- account-recovery abuse
- identity-related privacy loss

The severity of these risks increases when the device contains personal or sensitive data.

---

## Recommended Actions

Before transferring a device:

1. Identify the accounts currently linked to the device.
2. Back up information that must be retained.
3. Sign out of operating-system accounts where appropriate.
4. Sign out of browsers and synchronized profiles.
5. Remove email and communication accounts.
6. Sign out of cloud-storage services.
7. Remove work or educational accounts when permitted.
8. Review applications that may still contain active sessions.
9. Perform appropriate data sanitization.
10. Perform a factory reset where applicable.
11. Verify that personal accounts are no longer accessible.

---

## Important Considerations

Account-removal procedures vary by:

- operating system
- device type
- manufacturer
- application
- organization
- cloud provider

EcoShield should provide general decision support rather than assuming that one account-removal procedure applies to every device.

Users should follow current manufacturer or organizational guidance when detailed account-removal instructions are required.

---

## EcoShield Decision Context

Account and identity security is primarily associated with the following EcoShield assessment fields:

- `accounts_signed_out`
- `contains_personal_data`
- `contains_sensitive_data`
- `device_accessible`
- `can_power_on`
- `factory_reset_performed`
- `secure_erase_performed`
- `intended_disposal_method`

A device that contains personal or sensitive information and still has active accounts may require additional security preparation before transfer.

If the device cannot be accessed or powered on, normal account-removal procedures may be difficult or impossible. In such situations, EcoShield should highlight the limitation and recommend an appropriate cautious handling path.

---

## EcoShield Recommendation Principle

A device should not be considered ready for transfer solely because files appear to be deleted.

For devices that support user accounts, account sign-out should be considered together with:

- backup status
- encryption status
- secure erasure
- factory reset
- removable-media removal
- intended disposal method

This helps reduce the risk of residual identity and account exposure.

---

## Keywords

account security, identity security, account sign-out, device transfer, cloud account, browser session, Microsoft account, Google account, Apple account, email account, cloud storage, personal data, sensitive data, factory reset, secure erase, donation, resale, repair, recycling