# Gumroad Product Setup Guide

## Account Setup

1. **Create Gumroad Account**
   - Go to https://gumroad.com
   - Sign up with email
   - Complete profile (name, bio, social links)

2. **Connect Payment Method**
   - Settings → Payments
   - Add bank account or PayPal
   - Set payout schedule

---

## Product Creation

### Step 1: Create Product

1. Dashboard → Products → New Product
2. Product Type: **Digital Product**
3. Product Name: **CloudPad Pro**
4. URL: `gumroad.com/l/cloudpad-pro`

### Step 2: Pricing

- Price: **$14.99**
- "Pay what you want": ❌ (disabled)
- Currency: USD (or your local currency)

### Step 3: Files

Upload all platform builds:

```
cloudpad-windows.zip
  └─ CloudPad_Setup.exe
  └─ README.txt

cloudpad-macos.zip
  └─ CloudPad.dmg
  └─ README.txt

cloudpad-linux.zip
  └─ CloudPad-x86_64.AppImage
  └─ README.txt

cloudpad-extension.zip
  └─ extension/ (folder with all files)
  └─ INSTALL.txt
```

**File Preparation:**
```bash
# Create distribution packages
cd /Users/kutay/Projects/xboxControllerEmulator

# Windows (after building on Windows)
zip -r cloudpad-windows.zip dist/CloudPad.exe extension/ README.md

# macOS
zip -r cloudpad-macos.zip dist/CloudPad.dmg extension/ README.md

# Linux (after building on Linux)
zip -r cloudpad-linux.zip CloudPad-x86_64.AppImage extension/ README.md

# Extension only
zip -r cloudpad-extension.zip extension/
```

### Step 4: Description

**Title:**
```
CloudPad Pro - Universal Controller Emulator for Cloud Gaming
```

**Description:** (Use from marketing_ai_prompts.md)
```markdown
# CloudPad Pro - Use ANY Controller with Cloud Gaming

Works with Xbox Cloud Gaming, GeForce NOW, Amazon Luna, and more!

## What You Get

✅ CloudPad Desktop App (Windows, macOS, Linux)
✅ Browser Extension (Chrome, Edge, Brave)
✅ Lifetime License (one-time payment)
✅ Unlimited Devices
✅ Priority Email Support

## Features

- **Universal Compatibility**: Works with ANY controller, joystick, HOTAS, racing wheel
- **Auto-Calibration**: Automatically maps your device in seconds
- **Cross-Platform**: Single purchase unlocks all platforms
- **Zero Latency**: Direct input, no middleman
- **Easy Setup**: 5-minute installation

## System Requirements

- **Windows**: 10/11 (64-bit)
- **macOS**: 10.13 or later
- **Linux**: Ubuntu 20.04+, Fedora 35+, or any modern distro

## Installation

1. Download for your platform
2. Install CloudPad desktop app
3. Install browser extension
4. Connect your controller
5. Start playing!

Full installation guide included with purchase.

## License

- One-time purchase
- Lifetime updates
- Use on all your computers
- Commercial use allowed

## Support

Email support: your-email@example.com
Response time: Within 24 hours
```

### Step 5: Content

- Cover Image: 1200x630px (create with AI or Canva)
- Thumbnail: 400x400px
- Preview Images: Add 3-5 screenshots

### Step 6: After Purchase

**License Key Delivery:**

Option A: Manual (Start Here)
- Email each customer their license key
- Use format: `XXXX-XXXX-XXXX-XXXX`
- Generate with: `python3 license_validator.py generate <customer-email>`

Option B: Automated (Later)
- Use Gumroad's License Key system
- Or integrate with third-party key generator

**Email Template:**
```
Subject: Your CloudPad Pro License Key

Hi there!

Thank you for purchasing CloudPad Pro! 🎮

Your license key: XXXX-XXXX-XXXX-XXXX

To activate:
1. Open CloudPad desktop app
2. Click "🔑 License" button
3. Enter your license key
4. Restart the app

Downloads:
- Windows: [attached]
- macOS: [attached]
- Linux: [attached]
- Browser Extension: [attached]

Installation Guide: [link to docs]

Need help? Email me at your-email@example.com

Best,
Your Name
```

---

## Marketing Setup

### Gumroad Settings

1. **Workflows** (Settings → Workflows)
   - After Purchase → Send email with license key
   - After Purchase → Add to mailing list (for updates)

2. **Discover** (Make product discoverable)
   - Enable "Show on Gumroad Discover"
   - Categories: Software, Games, Productivity
   - Tags: controller, gaming, cloud gaming, emulator

3. **Affiliates** (Optional)
   - Enable affiliate program
   - Commission: 10-20%
   - Recruit gaming YouTubers/streamers

---

## Launch Checklist

### Pre-Launch
- [ ] Build all platform packages
- [ ] Test on Windows, macOS, Linux
- [ ] Create screenshots
- [ ] Write product description
- [ ] Set up Gumroad product page
- [ ] Create license key system
- [ ] Write email templates
- [ ] Set up support email

### Launch Day
- [ ] Make product live on Gumroad
- [ ] Post on Twitter/X
- [ ] Post on Reddit (r/cloudgaming, r/HOTAS, r/simracing)
- [ ] Submit to Product Hunt
- [ ] Email to any existing wait list
- [ ] Post in relevant Discord servers

### Post-Launch
- [ ] Monitor support emails
- [ ] Track sales/downloads
- [ ] Gather user feedback
- [ ] Plan updates based on feedback

---

## Pricing Experiments

Once you have some sales, try:

1. **Limited-Time Discount**
   - Sale price: $9.99
   - Duration: First 100 customers or 1 week

2. **Bundle Deals**
   - CloudPad + Custom Configs: $19.99
   - CloudPad + 1-on-1 Setup Call: $29.99

3. **Upgrade Path**
   - Free tier converts at ~5-10%
   - Pro tier should be clear value upgrade

---

## Alternative Platforms

If Gumroad doesn't work for your region:

1. **Paddle**: Like Gumroad, handles VAT
2. **Lemon Squeezy**: Good for EU sellers
3. **Stripe + Custom Site**: More complex but full control
4. **Itch.io**: Gaming-focused, 10% fee (or 0% with revenue share)

---

## Tax & Legal

- **VAT/Sales Tax**: Gumroad handles this automatically in most regions
- **Privacy Policy**: Required if collecting emails - use template generator
- **Terms of Service**: Basic "as-is" software license is fine
- **Refunds**: Gumroad default is 30 days - you can adjust

---

## Success Metrics

Track these:

- **Conversion rate**: Free downloads → Pro purchases
- **Average time to purchase**: How long before free users upgrade
- **Support tickets**: Should be < 5% of customers
- **Churn/Refunds**: Should be < 2%

Good first month target: 10-50 sales ($150-750)

After that, aim for 20% month-over-month growth.

---

## Next Steps

1. Build all platform packages (see BUILD.md)
2. Create Gumroad account
3. Set up product page (use description above)
4. Do soft launch (share with friends for feedback)
5. Full launch when ready!
